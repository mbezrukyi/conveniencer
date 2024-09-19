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
from ..keyboards import build_add_remove_keyboard
from .states import CategoryState

router = Router(name=__name__)


@router.callback_query(CategoryCB.filter(F.category == Category.ARCHIVES))
async def handle_archives_category(
    query: CallbackQuery,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    await state.set_state(CategoryState.archive)

    processor = CollectionProcessor(query.from_user.id, db.archives, Archive)

    archives = await processor.to_list()

    if archives:
        await query.message.answer(text="Your archives:")

        for archive in archives:
            await query.message.answer_document(
                document=archive.file_id,
                caption=archive.name,
            )

        await query.message.answer(
            text="What do you want to do?",
            reply_markup=build_add_remove_keyboard(),
        )
    else:
        await query.message.answer(
            text="Add your first archive",
            reply_markup=build_add_remove_keyboard(),
        )


@router.callback_query(
    CategoryState.archive,
    CategoryActionCB.filter(F.category_action == CategoryAction.ADD),
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

    await query.message.answer(**content.as_kwargs())


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
    archive = Archive(
        name=message.caption,
        file_id=message.document.file_id,
    )

    processor = CollectionProcessor(message.from_user.id, db.archives, Archive)

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
    CategoryState.archive,
    CategoryActionCB.filter(F.category_action == CategoryAction.REMOVE),
)
async def handle_remove_archive(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(CategoryState.remove_archive)

    await query.message.answer(text="Specify an archive name to delete")


@router.message(CategoryState.remove_archive, F.text)
async def remove_archive(
    message: Message,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    archive = Archive(name=message.text)

    processor = CollectionProcessor(message.from_user.id, db.archives, Archive)

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
