from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callbacks import (
    Category,
    CategoryAction,
    CategoryCB,
    CategoryActionCB,
)


def build_categories_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for category in Category:
        builder.button(
            text=category.value.title(),
            callback_data=CategoryCB(category=category),
        )

    return builder.adjust(1, repeat=True).as_markup()


def build_actions_keyboard(
    add: CategoryAction,
    remove: CategoryAction,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Add",
        callback_data=CategoryActionCB(category_action=add),
    )
    builder.button(
        text="Remove",
        callback_data=CategoryActionCB(category_action=remove),
    )
    builder.button(
        text="Back",
        callback_data=CategoryActionCB(category_action=CategoryAction.BACK),
    )

    return builder.adjust(2, 1).as_markup()
