from aiogram.fsm.state import State, StatesGroup


class CategoryState(StatesGroup):
    add_book = State()
    remove_book = State()

    add_link = State()
    remove_link = State()

    add_photo = State()
    remove_photo = State()

    add_archive = State()
    remove_archive = State()
