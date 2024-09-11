from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

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


@router.callback_query(CallbackCategory.filter(F.category == Category.BOOKS))
async def process_books_category(
    query: CallbackQuery,
    state: FSMContext,
    bot: Bot,
) -> None:
    await state.set_state(Action.book)

    await bot.send_message(
        chat_id=query.message.chat.id,
        text="This is `Books` category",
        reply_markup=build_add_remove_keyboard(),
    )


@router.callback_query(
    Action.book,
    CallbackCategoryAction.filter(F.category_action == CategoryAction.ADD),
)
async def process_add_book(
    query: CallbackQuery,
    state: FSMContext,
    bot: Bot,
) -> None:
    await bot.send_message(
        chat_id=query.message.chat.id,
        text="You pressed `Add` button",
    )
