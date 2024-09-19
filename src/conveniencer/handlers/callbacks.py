from enum import Enum

from aiogram.filters.callback_data import CallbackData


class Category(Enum):
    BOOKS = "books"
    LINKS = "links"
    PHOTOS = "photos"
    ARCHIVES = "archives"


class CategoryCB(CallbackData, prefix="ctg"):
    category: Category


class CategoryAction(Enum):
    ADD = "add"
    REMOVE = "remove"


class CategoryActionCB(CallbackData, prefix="can"):
    category_action: CategoryAction


class CallbackDataType(Enum):
    CATEGORY = "category"
    CATEGORY_ACTION = "category_action"
