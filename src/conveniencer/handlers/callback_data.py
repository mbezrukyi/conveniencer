from enum import Enum

from aiogram.filters.callback_data import CallbackData


class Category(Enum):
    AUDIOS = "audios"
    BOOKS = "books"
    PHOTOS = "photos"
    OTHER = "other"


class CallbackCategory(CallbackData, prefix="ctg"):
    category: Category


class CategoryAction(Enum):
    ADD = "add"
    REMOVE = "remove"


class CallbackCategoryAction(CallbackData, prefix="can"):
    category_action: CategoryAction
