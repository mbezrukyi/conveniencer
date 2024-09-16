from enum import Enum

from aiogram.types import InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_data import (
    CallbackCategory,
    CallbackCategoryAction,
    CallbackDataType,
    Category,
    CategoryAction,
)


def build_keyboard(
    items: Enum,
    callback_cls: CallbackData,
    callback_data_type: CallbackDataType,
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    for item in items:
        builder.button(
            text=item.value.title(),
            callback_data=callback_cls(**{callback_data_type.value: item}),
        )

    return builder


def build_categories_keyboard() -> InlineKeyboardMarkup:
    return (
        build_keyboard(
            Category,
            CallbackCategory,
            CallbackDataType.CATEGORY,
        )
        .adjust(1, repeat=True)
        .as_markup()
    )


def build_add_remove_keyboard() -> InlineKeyboardMarkup:
    return build_keyboard(
        CategoryAction,
        CallbackCategoryAction,
        CallbackDataType.CATEGORY_ACTION,
    ).as_markup()
