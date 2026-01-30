from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
import os
import sys
from config import PROJECT_ROOT

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [KeyboardButton(text = "Chat"),KeyboardButton(text = "Profile")],
    [KeyboardButton(text = "Reset Context"),KeyboardButton(text = "Help")]
])

profile_key_borad = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [KeyboardButton(text = "Subscribe"),KeyboardButton(text = "Back")]
])

buy_sub_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [KeyboardButton(text = "Buy subscribtion"),KeyboardButton(text = "Back")]
])

back_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [KeyboardButton(text = "Back")]
])
