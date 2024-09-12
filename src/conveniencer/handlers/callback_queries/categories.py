from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.formatting import Italic, Text

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


@router.callback_query(CallbackCategory.filter(F.category == Category.BOOKS))
async def handle_books_category(
    query: CallbackQuery,
    state: FSMContext,
    bot: Bot,
) -> None:
    await state.set_state(Action.book)

    # TODO: Add unique handler for different category

    # processor = CategoryProcessor(mongo.books)

    # processor.add()
    # processor.remove()
    # processor.as_list()

    # TODO: Display list of already added books

    # books = await mongo.books.find()

    # chat_id = query.message.chat.id

    # if books:
    #     await bot.send_message(chat_id=chat_id, text="Your books:")
    #
    #     async for book in books:
    #         await bot.send_document(
    #             chat_id=chat_id,
    #             document=book.file_id,
    #             caption=book.name,
    #         )
    #
    #     await bot.send_message(
    #         chat_id=chat_id,
    #         text="What do you want to do?",
    #         reply_markup=build_add_remove_keyboard(),
    #     )
    # else:
    #     await bot.send_message(
    #         chat_id=chat_id,
    #         text="Add your first book",
    #         reply_markup=build_add_remove_keyboard(),
    #     )

    await bot.send_message(
        chat_id=query.message.chat.id,
        text="Your books:",
        reply_markup=build_add_remove_keyboard(),
    )


@router.callback_query(
    Action.book,
    CallbackCategoryAction.filter(F.category_action == CategoryAction.ADD),
)
async def handle_add_book(
    query: CallbackQuery,
    state: FSMContext,
    bot: Bot,
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
async def add_book(message: Message, state: FSMContext) -> None:
    # TODO: Write the logic to add the book

    # name = message.caption
    # file_id = message.document.file_id

    # try:
    #     collection.insert_one(
    #         {
    #             "name": name,
    #             "file_id": file_id,
    #         },
    #     )
    # except SomeError:
    #     collection.update_one(
    #         {"name": name},
    #         {"$set": {"file_id": file_id}},
    #     )

    await message.answer("You've successfully added a new book!")

    await state.clear()
