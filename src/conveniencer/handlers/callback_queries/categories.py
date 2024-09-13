from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.formatting import Italic, Text
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

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


@router.callback_query(CallbackCategory.filter(F.category == Category.BOOKS))
async def handle_books_category(
    query: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    await state.set_state(Action.book)

    # TODO: Add unique handler for different category

    # processor = CategoryProcessor(mongo.books)

    # processor.add()
    # processor.remove()
    # processor.as_list()

    books = await db.books.find().to_list(length=None)

    chat_id = query.message.chat.id

    if books:
        await bot.send_message(chat_id=chat_id, text="Your books:")

        for book in books:
            await bot.send_document(
                chat_id=chat_id,
                document=book["file_id"],
                caption=book["name"],
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
    name = message.caption
    file_id = message.document.file_id

    try:
        await db.books.insert_one(
            {
                "name": name,
                "file_id": file_id,
            },
        )
    except DuplicateKeyError:
        await db.books.update_one(
            {"name": name},
            {"$set": {"file_id": file_id}},
        )

    await message.answer("You've successfully added a new book!")

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
    name = message.text

    await db.books.delete_one({"name": name})

    await message.answer(f"You've successfully delete the {name} book!")

    await state.clear()
