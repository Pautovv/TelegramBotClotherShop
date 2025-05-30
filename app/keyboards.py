from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.data.requests import get_categories, get_items_by_category

kb_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Profile', callback_data='profile_menu')],[InlineKeyboardButton(text='Catalog', callback_data='menu_button')],
    [InlineKeyboardButton(text='Rate', callback_data='menu_rate')], [InlineKeyboardButton(text='FAQ', callback_data='faq')]
])

kb_back_to_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Back', callback_data='back_to_main')]
])

kb_back_to_categories = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Back', callback_data='back_to_categories')]
])


async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name,
                                          callback_data=f'category_{category.id}'))
    keyboard.add(InlineKeyboardButton(text='Back', callback_data='back_to_main'))
    return keyboard.adjust(2).as_markup()

async def items(category_id):
    items = await get_items_by_category(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'item_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='Back',callback_data='back_to_categories'))
    return keyboard.adjust(2).as_markup()
