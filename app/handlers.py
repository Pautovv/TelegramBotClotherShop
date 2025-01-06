from aiogram import Router, F
import app.keyboards as kb
from app.data.requests import (set_user, get_items_by_id)
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def cmd_start(message : Message):
    await set_user(message.from_user.id)
    await message.answer(f'Hello, i am bot for the JaneShop.\nYou can find all clothes in me.', reply_markup=kb.kb_main)

@router.callback_query(F.data=='profile_menu')
async def cmd_menu(callback : CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        f'ID: {callback.from_user.id}\nName: {callback.from_user.full_name}',reply_markup=kb.kb_back_to_main
    )

@router.callback_query(F.data=='back_to_main')
async def cmd_back_to_main(callback : CallbackQuery):
    await callback.answer()
    await callback.message.answer(f'Hello, i am bot for the JaneShop.\nYou can find all clothes in me.', reply_markup=kb.kb_main)

@router.callback_query(F.data=='back_to_categories')
async def cmd_back_to_categories(callback : CallbackQuery):
    await callback.answer()
    await callback.message.answer(f'Chouse the category:', reply_markup=await kb.categories())




@router.callback_query(F.data=='menu_button')
async def cmd_menu_button(callback : CallbackQuery):
    await callback.answer()
    await callback.message.answer(f'Chouse the category: ', reply_markup=await kb.categories())

@router.callback_query(F.data.startswith('category_'))
async def cmd_select_category(callback : CallbackQuery):
    await callback.answer()
    await callback.message.answer(f'Chouse the item:',reply_markup=await kb.items(int(callback.data.split('_')[1])))

@router.callback_query(F.data.startswith('item_'))
async def cmd_select_item(callback : CallbackQuery):
    item = await get_items_by_id(int(callback.data.split('_')[1]))
    await callback.answer()
    await callback.message.answer_photo(photo=item.photo, caption=f'{item.name}\n\nSize: {item.size}\n\n{item.description}\n\nPrice: {item.price} rubles\n\n',reply_markup=kb.kb_back_to_categories)








@router.callback_query(F.data=='faq')
async def cmd_menu_button(callback : CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        f'If you find the error, please write to the admin\'s mail\nAlso if you find violation write to the mail too.\nmail_adress@mail.ru', reply_markup=kb.kb_back_to_main)

@router.callback_query(F.data=='menu_rate')
async def cmd_rate_menu(callback : CallbackQuery):
    await callback.answer()
    await callback.message.answer(f'In the process of development...',reply_markup=kb.kb_back_to_main)

@router.message(lambda message: not message.text.startswith('/'))
async def cmd_spam(message : Message):
    await message.answer(f'Please, send correct command or choose the buttom.',reply_markup=kb.kb_back_to_main)