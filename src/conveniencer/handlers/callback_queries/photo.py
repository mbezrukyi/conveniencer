from typing import List

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Bold, Text
from aiogram.utils.media_group import MediaGroupBuilder
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import DuplicateKeyError

from conveniencer.database import CollectionProcessor, Photo
from conveniencer.database.errors import NoDocumentError
from ..callbacks import (
    Category,
    CategoryAction,
    CategoryCB,
    CategoryActionCB,
)
from ..keyboards import build_add_remove_keyboard
from .states import CategoryState

router = Router(name=__name__)


@router.callback_query(CategoryCB.filter(F.category == Category.PHOTOS))
async def handle_photos_category(
    query: CallbackQuery,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    await state.set_state(CategoryState.photo)

    processor = CollectionProcessor(query.from_user.id, db.photos, Photo)

    photos = await processor.to_list()

    if photos:
        await query.message.answer(text="Your photos:")

        for photo in photos:
            await send_photos(query.message, photo.photo_ids, photo.name)
            await send_documents(query.message, photo.document_ids, photo.name)

        await query.message.answer(
            text="What do you want to do?",
            reply_markup=build_add_remove_keyboard(),
        )
    else:
        await query.message.answer(
            text="Add your first photo",
            reply_markup=build_add_remove_keyboard(),
        )


async def send_photos(
    message: Message,
    photo_ids: List[str],
    caption: str,
) -> None:
    if photo_ids:
        photo_media_group = MediaGroupBuilder()

        for i, photo_id in enumerate(photo_ids):
            if i == 0:
                photo_media_group.add_photo(
                    media=photo_id,
                    caption=caption,
                )
            else:
                photo_media_group.add_photo(media=photo_id)

        await message.answer_media_group(media=photo_media_group.build())


async def send_documents(
    message: Message,
    document_ids: List[str],
    caption: str,
) -> None:
    if document_ids:
        document_media_group = MediaGroupBuilder()

        for i, document_id in enumerate(document_ids):
            if i == len(document_ids) - 1:
                document_media_group.add_document(
                    media=document_id,
                    caption=caption,
                )
            else:
                document_media_group.add_document(media=document_id)

        await message.answer_media_group(media=document_media_group.build())


@router.callback_query(
    CategoryState.photo,
    CategoryActionCB.filter(F.category_action == CategoryAction.ADD),
)
async def handle_add_photo(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(CategoryState.add_photo)

    await query.message.answer(
        text="Paste photos and specify a name explicitly"
    )


@router.message(CategoryState.add_photo, F.photo)
async def collect_photo(message: Message, state: FSMContext) -> None:
    photo_id = message.photo[0].file_id

    data = await state.get_data()

    photo_ids = data.get("photo_ids", [])

    photo_ids.append(photo_id)

    await state.update_data(photo_ids=photo_ids)


@router.message(CategoryState.add_photo, F.document)
async def collect_document(message: Message, state: FSMContext) -> None:
    document_id = message.document.file_id

    data = await state.get_data()

    document_ids = data.get("document_ids", [])

    document_ids.append(document_id)

    await state.update_data(document_ids=document_ids)


@router.message(CategoryState.add_photo, F.text)
async def add_photo(
    message: Message,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    data = await state.get_data()

    photo_ids = data.get("photo_ids", [])
    document_ids = data.get("document_ids", [])

    if not (photo_ids or document_ids):
        await message.answer("You did not paste any images. Try again")

        return None

    processor = CollectionProcessor(message.from_user.id, db.photos, Photo)

    photo = Photo(
        name=message.text,
        photo_ids=photo_ids,
        document_ids=document_ids,
    )

    try:
        await processor.add(photo)

        content = Text(
            "You've successfully added the ",
            Bold(photo.name),
            " photo!",
        )
    except DuplicateKeyError:
        await processor.replace(photo)

        content = Text(
            "You've successfully updated the ",
            Bold(photo.name),
            " photo!",
        )

    await message.answer(**content.as_kwargs())

    await state.clear()


@router.callback_query(
    CategoryState.photo,
    CategoryActionCB.filter(F.category_action == CategoryAction.REMOVE),
)
async def handle_remove_photo(
    query: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(CategoryState.remove_photo)

    await query.message.answer(text="Specify a photo name to delete")


@router.message(CategoryState.remove_photo, F.text)
async def remove_photo(
    message: Message,
    state: FSMContext,
    db: AsyncIOMotorDatabase,
) -> None:
    photo = Photo(name=message.text)

    processor = CollectionProcessor(message.from_user.id, db.photos, Photo)

    try:
        await processor.remove(photo)

        content = Text(
            "You've successfully deleted the ",
            Bold(photo.name),
            " photo!",
        )
    except NoDocumentError:
        content = Text(
            "No photo with name ",
            Bold(photo.name),
            " was found.",
        )

    await message.answer(**content.as_kwargs())

    await state.clear()
