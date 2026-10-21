import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from practice_db import init_db, add_user

load_dotenv

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

init_db()

class Form(StatesGroup):
	name = State()
	age = State()
	lang = State()

@dp.message(Command("start"))
async def start(message: types.Message):
	add_user(message.from_user.id, message.from_user.first_name)
	kb = ReplyKeyboardMarkup(
		keyboard=[
			[KeyboardButton(text="Помощь")],
			[KeyboardButton(text="Меню")]
		],
		resize_keyboard=True
		)
	await message.answer(f"Привет, {message.from_user.first_name}!",
	reply_markup=kb)

@dp.message(lambda m: m.text == "Помощь")
async def help_btn(message: types.Message):
	await message.answer("Я умею: \n"
	"/start и эхо")
	
@dp.message(lambda m: m.text == "Меню")
async def menu_btn(message: types.Message):
	ikb = InlineKeyboardMarkup(
		inline_keyboard=[
			[InlineKeyboardButton(text="Нажми на меня", callback_data="press_me")]
		]
	)
	await message.answer("Вот inline-menu",
	reply_markup=ikb)
		
@dp.callback_query(F.data == "press_me")
async def press_me(callback: types.CallbackQuery):
	await callback.answer("Ты нажал!", show_alert=True)

@dp.message(Command("cancel"))
async def cancel(message: types.Message, state: FSMContext):
	await state.clear()
	await message.answer("Действие отменено")

@dp.message(Command("form"))
async def form_start(message: types.Message, state: FSMContext):
	await message.answer("Как зовут?")
	await state.set_state(Form.name)
	
@dp.message(Form.name)
async def form_name(message: types.Message, state: FSMContext): 
	await state.update_data(name=message.text)
	await message.answer(f"Приятно познакомиться, {message.text}. Сколько тебе лет?")
	await state.set_state(Form.age)
	
@dp.message(Form.age)
async def form_age(message: types.Message, state: FSMContext):
	if not message.text.isdigit():
		await message.answer("Возраст числом!")
		return
	await state.update_data(age=message.text)
	await message.answer(f"Отлично, что тебе {message.text} лет. Какой твой любимый язык?")
	await state.set_state(Form.lang)

@dp.message(Form.lang)
async def form_lang(message: types.Message, state: FSMContext):
	data = await state.get_data()
	name = data.get("name")
	age = data.get("age")
	await message.answer(f"Записал: {name}, {age} лет, любимый язык программирования — {message.text}")
	await state.clear()
	
@dp.message()
async def echo(message: types.Message):
	await message.answer(f"Ты написал: {message.text}")
	
	
async def main():
	print("imkol — Junior")
	await dp.start_polling(bot)
	
	
if __name__ == "__main__":
	asyncio.run(main())
