from aiogram import Bot,Dispatcher,F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message,File,Video,PhotoSize,LabeledPrice
import aiogram
import keyboards as kb
from backend.database.core import create_deafault_user_data,remove_free_zapros,check_free_zapros_amount,get_amount_of_zaproses,subscribe,set_sub_bac_to_false,get_me,unsub_all_users_whos_sub_is_ending_today,is_user_subbed,buy_zaproses
from main import bot

import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir) 

sys.path.insert(0, project_root)

router = Router()




@router.message(CommandStart())
async def start_messsage(message:Message):
    user_name = message.from_user.username
    user_id = message.from_user.id
    await create_deafault_user_data(str(user_id))
    await message.answer("Welcome")# вставить сюда норм текст

@router.message(F.text == "Profile")
async def profile_handler(message:Message):
    user_name = message.from_user.username
    user_id = message.from_user.id
    user_data = get_me(str(user_id))
    user_data[str(user_id)] = user_name
    user_subbed:bool = await  is_user_subbed(str(user_id))
    if not user_subbed:
        await message.answer(
        user_data,
        reply_markup=kb.profile_key_borad        
        )
    else:
        await message.answer(
        user_data        
    )

@router.message(F.text == "Subscribe")
async def subscribe_handler(message:Message):
    user_id = message.from_user.id
    buy_sub_text = "" # вставить норм текст для подписки
    await message.answer(buy_sub_text)



#сделать  норм invoice
@router.message(F.text == "Buy subscribtion")
async def buy_sub_handler(message:Message):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Название товара",
        description="Описание товара",
        payload="test_payload", 
        provider_token="YOUR_PROVIDER_TOKEN", 
        currency="RUB",
        prices=[
            LabeledPrice(label="Товар 1", amount=10000),  # 100.00 RUB
            LabeledPrice(label="Скидка", amount=-2000),   # -20.00 RUB
        ],
        start_parameter="test",
        need_email=True, 
        need_phone_number=False,
        is_flexible=False, 
    )
    
    
    
    
       