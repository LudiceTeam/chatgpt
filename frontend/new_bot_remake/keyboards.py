from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
import os
import sys
from config import PROJECT_ROOT

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [KeyboardButton(text = "Чат"),KeyboardButton(text = "Профиль"),KeyboardButton(text = "Реферальная программа")],
    [KeyboardButton(text = "Сбросить Контекст"),KeyboardButton(text = "Помощь"),KeyboardButton(text = "Поддержка"),KeyboardButton(text = "Выбрать Модель")]
])

profile_key_borad = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Подписаться",callback_data = "subscribe")],
    [InlineKeyboardButton(text = "Купить Запросы",callback_data = "buy_requests")]
])



back_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [KeyboardButton(text = "Назад")]
])

buy_req_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [KeyboardButton(text = "5 Запросов"),KeyboardButton(text = "10 Запросов")],
    [KeyboardButton(text = "20 Запросов"),KeyboardButton(text = "Назад")]
])

inline_pay = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Заплатить 250 ⭐",pay = True)]
])


subscrition_keyborad = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [KeyboardButton(text = "Premium"),KeyboardButton(text = "Basic")],
    [KeyboardButton(text = "Назад")]
])


inline_pay_basic = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Заплатить 199 ⭐",pay = True)]
])


choose_ai_keyboard = InlineKeyboardMarkup(inline_keyboard =  [
    [InlineKeyboardButton(text = "Gemini 3",callback_data = "google/gemini-3-flash-preview"),InlineKeyboardButton(text = "Gemini 2",callback_data="google/gemini-2.5-flash")]
])