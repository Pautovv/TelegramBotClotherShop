from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from app.data.requests import set_item, set_categories
from aiogram.filters import Filter, Command
import app.keyboards as kb
admin = Router()

class AdminProtect(Filter):
    async def __call__(self, message : Message):
        return message.from_user.id in [693187782]


class AddCategory(StatesGroup):
    category = State()

@admin.message(AdminProtect(), Command('add_category'))
async def cmd_add_category(message : Message, state : FSMContext):
    await state.set_state(AddCategory.category)
    await message.answer('Please write new category:')

@admin.message(AdminProtect(), AddCategory.category)
async def cmd_add_category_name(message : Message, state : FSMContext):
    await state.update_data(category = message.text)
    data = await state.get_data()
    vect = next(iter(data.items()))
    first_key=vect[0]
    await set_categories(str(data[first_key]))
    await message.answer('New category had been successfully added',reply_markup=kb.kb_back_to_main)
    await state.clear()

class AddItem(StatesGroup):
    name = State()
    category = State()
    size = State()
    description = State()
    photo = State()
    price = State()


@admin.message(AdminProtect(), Command('apanel'))
async def cmd_apanel(message : Message):
    await message.answer(
        f'возможные команды: /newletter\n/add_item\n/add_category'
    )

@admin.message(AdminProtect(), Command('add_item'))
async def cmd_add_item(message : Message, state : FSMContext):
    await state.set_state(AddItem.name)
    await message.answer('Write the item\'s name:')

@admin.message(AdminProtect(), AddItem.name)
async def cmd_add_name(message : Message, state : FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(AddItem.category)
    await message.answer('Select the category:', reply_markup=await kb.categories())

@admin.callback_query(AdminProtect(), AddItem.category)
async def cmd_add_category(callback : CallbackQuery, state : FSMContext):
    await state.update_data(category = int(callback.data.split('_')[1]))
    await state.set_state(AddItem.size)
    await callback.answer()
    await callback.message.answer('Write the item\'s size:')

@admin.message(AdminProtect(), AddItem.size)
async def cmd_add_size(message : Message, state : FSMContext):
    await state.update_data(size = message.text)
    await state.set_state(AddItem.description)
    await message.answer('Write the item\'s description:')

@admin.message(AdminProtect(), AddItem.description)
async def cmd_add_description(message : Message, state : FSMContext):
    await state.update_data(description = message.text)
    await state.set_state(AddItem.photo)
    await message.answer('Send the item\'s photo:')

@admin.message(AdminProtect(), AddItem.photo, F.photo)
async def cmd_add_photo(message : Message, state : FSMContext):
    await state.update_data(photo = message.photo[-1].file_id)
    await state.set_state(AddItem.price)
    await message.answer('Write the item\'s price:')

@admin.message(AdminProtect(), AddItem.price)
async def cmd_add_price(message : Message, state : FSMContext):
    await state.update_data(price = message.text)
    data = await state.get_data()
    await set_item(data)
    await message.answer('The item had been successfully added', reply_markup=kb.kb_back_to_main)
    await state.clear()

    