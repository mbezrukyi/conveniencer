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
from ..keyboards import build_add_remove_keyboard
from .states import CategoryState

router = Router(name=__name__)


@router.callback_query(CategoryCB.filter(F.category == Category.LINKS))
async def handle_links_category(
    query: CallbackQuery,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    await state.set_state(CategoryState.link)

    processor = CollectionProcessor(query.from_user.id, db.links, Link)

    links = await processor.to_list()

    if links:
        await query.message.answer(text="Your links:")

        for link in links:
            content = Text(Bold(link.name), ": ", Italic(link.url))

            await query.message.answer(**content.as_kwargs())

        await query.message.answer(
            text="What do you want to do?",
            reply_markup=build_add_remove_keyboard(),
        )
    else:
        await query.message.answer(
            text="Add your first link",
            reply_markup=build_add_remove_keyboard(),
        )


@router.callback_query(
    CategoryState.link,
    CategoryActionCB.filter(F.category_action == CategoryAction.ADD),
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

    await query.message.answer(**content.as_kwargs())


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
    CategoryState.link,
    CategoryActionCB.filter(F.category_action == CategoryAction.REMOVE),
)
async def handle_remove_link(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(CategoryState.remove_link)

    await query.message.answer(text="Specify a link name to delete")


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
