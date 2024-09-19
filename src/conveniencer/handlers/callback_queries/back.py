from aiogram import F, Router
from aiogram.types import CallbackQuery

from ..callbacks import CategoryAction, CategoryActionCB
from ..keyboards import build_categories_keyboard

router = Router(name=__name__)


@router.callback_query(
    CategoryActionCB.filter(F.category_action == CategoryAction.BACK)
)
async def handle_back(query: CallbackQuery) -> None:
    await query.message.edit_text(
        text="Categories list:",
        reply_markup=build_categories_keyboard(),
    )
