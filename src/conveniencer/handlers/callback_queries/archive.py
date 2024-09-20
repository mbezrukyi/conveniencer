from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Bold, Italic, Text
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

from conveniencer.filters import DocumentTypeFilter
from conveniencer.database import Archive, CollectionProcessor
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


@router.callback_query(CategoryCB.filter(F.category == Category.ARCHIVES))
async def handle_archives_category(
    query: CallbackQuery,
    db: AsyncIOMotorDatabase,
) -> None:
    processor = CollectionProcessor(db.archives, Archive)

    archives = await processor.to_list(query.from_user.id)

    keyboard = build_actions_keyboard(
        add=CategoryAction.ADD_ARCHIVE,
        remove=CategoryAction.REMOVE_ARCHIVE,
    )

    if archives:
        await query.message.answer(text="Your archives:")

        for archive in archives:
            await query.message.answer_document(
                document=archive.file_id,
                caption=archive.name,
            )

        await query.message.edit_text(
            text="What do you want to do?",
            reply_markup=keyboard,
        )
    else:
        await query.message.edit_text(
            text="Add your first archive",
            reply_markup=keyboard,
        )


@router.callback_query(
    CategoryActionCB.filter(F.category_action == CategoryAction.ADD_ARCHIVE)
)
async def handle_add_archive(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(CategoryState.add_archive)

    content = Text(
        "Specify an archive name and attach a file (",
        Italic(".tar, "),
        Italic(".tar.gz, "),
        Italic(".zip, "),
        Italic(".rar"),
        ")",
    )

    await query.answer(**content.as_kwargs())


@router.message(
    CategoryState.add_archive,
    F.caption,
    F.document,
    DocumentTypeFilter(".tar", ".tar.gz", ".zip", ".rar"),
)
async def add_archive(
    message: Message,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    processor = CollectionProcessor(db.archives, Archive)

    archive = Archive(
        user_id=message.from_user.id,
        name=message.caption,
        file_id=message.document.file_id,
    )

    try:
        await processor.add(archive)

        content = Text(
            "You've successfully added the ",
            Bold(archive.name),
            " archive!",
        )
    except DuplicateKeyError:
        await processor.replace(archive)

        content = Text(
            "You've successfully updated the ",
            Bold(archive.name),
            " archive!",
        )

    await message.answer(**content.as_kwargs())

    await state.clear()


@router.callback_query(
    CategoryActionCB.filter(F.category_action == CategoryAction.REMOVE_ARCHIVE)
)
async def handle_remove_archive(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(CategoryState.remove_archive)

    await query.answer(text="Specify an archive name to delete")


@router.message(CategoryState.remove_archive, F.text)
async def remove_archive(
    message: Message,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    processor = CollectionProcessor(db.archives, Archive)

    archive = Archive(user_id=message.from_user.id, name=message.text)

    try:
        await processor.remove(archive)

        content = Text(
            "You've successfully deleted the ",
            Bold(archive.name),
            " archive!",
        )

    except NoDocumentError:
        content = Text(
            "No archive with name ",
            Bold(archive.name),
            " was found.",
        )

    await message.answer(**content.as_kwargs())

    await state.clear()
