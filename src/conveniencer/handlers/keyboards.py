from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_data import (
    CallbackCategory,
    CallbackCategoryAction,
    Category,
    CategoryAction,
)


def build_categories_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for category in Category:
        builder.button(
            text=category.value.title(),
            callback_data=CallbackCategory(category=category),
        )

    return builder.as_markup()


def build_add_remove_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for category_action in CategoryAction:
        builder.button(
            text=category_action.value.title(),
            callback_data=CallbackCategoryAction(category_action=category_action),
        )

    return builder.as_markup()
