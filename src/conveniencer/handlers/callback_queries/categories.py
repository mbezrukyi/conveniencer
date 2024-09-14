from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.formatting import Bold, Italic, Text
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

from conveniencer.database.processor import CollectionProcessor
from conveniencer.database.entities import Book, Link
from conveniencer.database.errors import NoDocumentError
from conveniencer.filters.document_type import DocumentTypeFilter
from ..callback_data import (
    CallbackCategory,
    CallbackCategoryAction,
    Category,
    CategoryAction,
)
from ..keyboards import build_add_remove_keyboard

router = Router(name=__name__)


class Action(StatesGroup):
    book = State()
    add_book = State()
    remove_book = State()

    link = State()
    add_link = State()
    remove_link = State()


@router.callback_query(CallbackCategory.filter(F.category == Category.BOOKS))
async def handle_books_category(
    query: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    await state.set_state(Action.book)

    chat_id = query.message.chat.id

    processor = CollectionProcessor(db.books, Book)

    books = await processor.to_list()

    if books:
        await bot.send_message(chat_id=chat_id, text="Your books:")

        for book in books:
            await bot.send_document(
                chat_id=chat_id,
                document=book.file_id,
                caption=book.name,
            )

        await bot.send_message(
            chat_id=chat_id,
            text="What do you want to do?",
            reply_markup=build_add_remove_keyboard(),
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text="Add your first book",
            reply_markup=build_add_remove_keyboard(),
        )


@router.callback_query(
    Action.book,
    CallbackCategoryAction.filter(F.category_action == CategoryAction.ADD),
)
async def handle_add_book(
    query: CallbackQuery,
    bot: Bot,
    state: FSMContext,
) -> None:
    await state.set_state(Action.add_book)

    content = Text(
        "Specify a book name and attach a book (",
        Italic(".pdf"),
        ")",
    )

    await bot.send_message(
        chat_id=query.message.chat.id,
        **content.as_kwargs(),
    )


@router.message(
    Action.add_book,
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

    processor = CollectionProcessor(db.books, Book)

    try:
        await processor.add(book)

        content = Text(
            "You've successfully added the ",
            Bold(book.name),
            " book!",
        )
    except DuplicateKeyError:
        await processor.update(book)

        content = Text(
            "You've successfully updated the ",
            Bold(book.name),
            " book!",
        )

    await message.answer(**content.as_kwargs())

    await state.clear()


@router.callback_query(
    Action.book,
    CallbackCategoryAction.filter(F.category_action == CategoryAction.REMOVE),
)
async def handle_remove_book(
    query: CallbackQuery,
    bot: Bot,
    state: FSMContext,
) -> None:
    await state.set_state(Action.remove_book)

    await bot.send_message(
        chat_id=query.message.chat.id,
        text="Specify a book name to delete",
    )


@router.message(Action.remove_book, F.text)
async def remove_book(
    message: Message,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    book = Book(name=message.text)

    processor = CollectionProcessor(db.books, Book)

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


@router.callback_query(CallbackCategory.filter(F.category == Category.LINKS))
async def handle_links_category(
    query: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    await state.set_state(Action.link)

    chat_id = query.message.chat.id

    processor = CollectionProcessor(db.links, Link)

    links = await processor.to_list()

    if links:
        await bot.send_message(chat_id=chat_id, text="Your links:")

        for link in links:
            content = Text(Bold(link.name), ": ", Italic(link.url))

            await bot.send_message(chat_id=chat_id, **content.as_kwargs())

        await bot.send_message(
            chat_id=chat_id,
            text="What do you want to do?",
            reply_markup=build_add_remove_keyboard(),
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text="Add your first link",
            reply_markup=build_add_remove_keyboard(),
        )


@router.callback_query(
    Action.link,
    CallbackCategoryAction.filter(F.category_action == CategoryAction.ADD),
)
async def handle_add_link(
    query: CallbackQuery,
    bot: Bot,
    state: FSMContext,
) -> None:
    await state.set_state(Action.add_link)

    content = Text(
        "Specify a link in the format ",
        Italic("{name: (https|http)://...}"),
    )

    await bot.send_message(
        chat_id=query.message.chat.id,
        **content.as_kwargs(),
    )


@router.message(
    Action.add_link,
    F.text.regexp(r"^\w+:\s*?(http|https):\/\/[a-zA-Z0-9]+?\.[a-zA-Z]\S*?$"),
)
async def add_link(
    message: Message,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    name, url = message.text.split(":", 1)

    link = Link(name=name, url=url)

    processor = CollectionProcessor(db.links, Link)

    try:
        await processor.add(link)

        content = Text(
            "You've successfully added the ",
            Bold(link.name),
            " link!",
        )
    except DuplicateKeyError:
        await processor.update(link)

        content = Text(
            "You've successfully updated the ",
            Bold(link.name),
            " link!",
        )

    await message.answer(**content.as_kwargs())

    await state.clear()


@router.callback_query(
    Action.link,
    CallbackCategoryAction.filter(F.category_action == CategoryAction.REMOVE),
)
async def handle_remove_link(
    query: CallbackQuery,
    bot: Bot,
    state: FSMContext,
) -> None:
    await state.set_state(Action.remove_link)

    await bot.send_message(
        chat_id=query.message.chat.id,
        text="Specify a link name to delete",
    )


@router.message(Action.remove_link, F.text)
async def remove_link(
    message: Message,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    link = Link(name=message.text)

    processor = CollectionProcessor(db.links, Link)

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
