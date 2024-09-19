from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Bold, Italic, Text
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

from conveniencer.filters import DocumentTypeFilter
from conveniencer.database import Book, CollectionProcessor
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


@router.callback_query(CategoryCB.filter(F.category == Category.BOOKS))
async def handle_books_category(
    query: CallbackQuery,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    await state.set_state(CategoryState.book)

    processor = CollectionProcessor(query.from_user.id, db.books, Book)

    books = await processor.to_list()

    if books:
        await query.message.answer(text="Your books:")

        for book in books:
            await query.message.answer_document(
                document=book.file_id,
                caption=book.name,
            )

        await query.message.answer(
            text="What do you want to do?",
            reply_markup=build_add_remove_keyboard(),
        )
    else:
        await query.message.answer(
            text="Add your first book",
            reply_markup=build_add_remove_keyboard(),
        )


@router.callback_query(
    CategoryState.book,
    CategoryActionCB.filter(F.category_action == CategoryAction.ADD),
)
async def handle_add_book(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(CategoryState.add_book)

    content = Text(
        "Specify a book name and attach a file (",
        Italic(".pdf"),
        ")",
    )

    await query.message.answer(**content.as_kwargs())


@router.message(
    CategoryState.add_book,
    F.caption,
    F.document,
    DocumentTypeFilter(".pdf"),
)
async def add_book(
    message: Message,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    book = Book(name=message.caption, file_id=message.document.file_id)

    processor = CollectionProcessor(message.from_user.id, db.books, Book)

    try:
        await processor.add(book)

        content = Text(
            "You've successfully added the ",
            Bold(book.name),
            " book!",
        )
    except DuplicateKeyError:
        await processor.replace(book)

        content = Text(
            "You've successfully updated the ",
            Bold(book.name),
            " book!",
        )

    await message.answer(**content.as_kwargs())

    await state.clear()


@router.callback_query(
    CategoryState.book,
    CategoryActionCB.filter(F.category_action == CategoryAction.REMOVE),
)
async def handle_remove_book(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(CategoryState.remove_book)

    await query.message.answer(text="Specify a book name to delete")


@router.message(CategoryState.remove_book, F.text)
async def remove_book(
    message: Message,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    book = Book(name=message.text)

    processor = CollectionProcessor(message.from_user.id, db.books, Book)

    try:
        await processor.remove(book)

        content = Text(
            "You've successfully deleted the ",
            Bold(book.name),
            " book!",
        )

    except NoDocumentError:
        content = Text(
            "No book with name ",
            Bold(book.name),
            " was found.",
        )

    await message.answer(**content.as_kwargs())

    await state.clear()
