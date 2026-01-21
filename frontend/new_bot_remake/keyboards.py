from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup


main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = "Chat"),KeyboardButton(text = "Profile")]
])

profile_key_borad = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Subscribe")]
])

buy_sub_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = "Buy subscribtion")]
])