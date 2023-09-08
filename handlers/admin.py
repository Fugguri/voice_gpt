from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.handler import ctx_data
from aiogram.dispatcher import FSMContext

from config import Config
from db import Database
from keyboards.keyboards import Keyboards

async def admin(message: types.Message):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    
    markup = await kb.admin_kb()
    
    await message.answer("Выберите пункт меню",reply_markup=markup)
    


def register_admin_handlers(dp: Dispatcher, kb: Keyboards ):
    
    dp.register_message_handler(admin,commands="admin",state="*")
    

    
    