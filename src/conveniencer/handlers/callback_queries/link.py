from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Bold, Italic, Text
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

from conveniencer.filters import LinkFilter
from conveniencer.database import CollectionProcessor, Link
from conveniencer.database.errors import NoDocumentError
from ..callbacks import (
    Category,
    CategoryAction,
    CategoryCB,
    CategoryActionCB,
)
from ..keyboards import build_actions_keyboard
from .states import CategoryState

router = Router(name=__name__)


@router.callback_query(CategoryCB.filter(F.category == Category.LINKS))
async def handle_links_category(
    query: CallbackQuery,
    db: AsyncIOMotorDatabase,
) -> None:
    processor = CollectionProcessor(query.from_user.id, db.links, Link)

    links = await processor.to_list()

    keyboard = build_actions_keyboard(
        add=CategoryAction.ADD_LINK,
        remove=CategoryAction.REMOVE_LINK,
    )

    if links:
        await query.message.answer(text="Your links:")

        for link in links:
            content = Text(Bold(link.name), ": ", Italic(link.url))

            await query.message.answer(**content.as_kwargs())

        await query.message.edit_text(
            text="What do you want to do?",
            reply_markup=keyboard,
        )
    else:
        await query.message.edit_text(
            text="Add your first link",
            reply_markup=keyboard,
        )


@router.callback_query(
    CategoryActionCB.filter(F.category_action == CategoryAction.ADD_LINK)
)
async def handle_add_link(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(CategoryState.add_link)

    content = Text(
        "Specify a link in the format ",
        Italic("{name: (https|http)://...}"),
    )

    await query.answer(**content.as_kwargs())


@router.message(CategoryState.add_link, LinkFilter())
async def add_link(
    message: Message,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    name, url = message.text.split(":", 1)

    link = Link(name=name, url=url)

    processor = CollectionProcessor(message.from_user.id, db.links, Link)

    try:
        await processor.add(link)

        content = Text(
            "You've successfully added the ",
            Bold(link.name),
            " link!",
        )
    except DuplicateKeyError:
        await processor.replace(link)

        content = Text(
            "You've successfully updated the ",
            Bold(link.name),
            " link!",
        )

    await message.answer(**content.as_kwargs())

    await state.clear()


@router.callback_query(
    CategoryActionCB.filter(F.category_action == CategoryAction.REMOVE_LINK)
)
async def handle_remove_link(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(CategoryState.remove_link)

    await query.answer(text="Specify a link name to delete")


@router.message(CategoryState.remove_link, F.text)
async def remove_link(
    message: Message,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    link = Link(name=message.text)

    processor = CollectionProcessor(message.from_user.id, db.links, Link)

    try:
        await processor.remove(link)

        content = Text(
            "You've successfully deleted the ",
            Bold(link.name),
            " link!",
        )

    except NoDocumentError:
        content = Text(
            "No link with name ",
            Bold(link.name),
            " was found.",
        )

    await message.answer(**content.as_kwargs())

    await state.clear()
