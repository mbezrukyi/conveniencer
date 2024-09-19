from aiogram.fsm.state import State, StatesGroup


class CategoryState(StatesGroup):
    book = State()
    add_book = State()
    remove_book = State()

    link = State()
    add_link = State()
    remove_link = State()

    photo = State()
    add_photo = State()
    remove_photo = State()

    archive = State()
    add_archive = State()
    remove_archive = State()
