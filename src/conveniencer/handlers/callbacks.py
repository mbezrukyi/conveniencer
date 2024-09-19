from enum import Enum

from aiogram.filters.callback_data import CallbackData


class Category(Enum):
    ARCHIVES = "archives"
    BOOKS = "books"
    LINKS = "links"
    PHOTOS = "photos"


class CategoryCB(CallbackData, prefix="ctg"):
    category: Category


class CategoryAction(Enum):
    ADD_ARCHIVE = "add_archive"
    REMOVE_ARCHIVE = "remove_archive"

    ADD_BOOK = "add_book"
    REMOVE_BOOK = "remove_book"

    ADD_LINK = "add_link"
    REMOVE_LINK = "remove_link"

    ADD_PHOTO = "add_photo"
    REMOVE_PHOTO = "remove_photo"

    BACK = "back"


class CategoryActionCB(CallbackData, prefix="can"):
    category_action: CategoryAction
