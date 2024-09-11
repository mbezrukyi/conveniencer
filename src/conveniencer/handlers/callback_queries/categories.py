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

    # TODO: Display list of already added books

    await bot.send_message(
        chat_id=query.message.chat.id,
        text="This is `Books` category",
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
        "Write a book name and attach a book (",
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

    await message.answer("You've successfully added a new book!")

    await state.clear()
