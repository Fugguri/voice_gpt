from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.handler import ctx_data
from aiogram.dispatcher import FSMContext

from utils import speech_to_text,create_responce,text_to_speech
from config.config import Config
from db import Database
from keyboards.keyboards import Keyboards

import os

async def start(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']

    user = db.get_user(message.from_user.id)
    
    if not user:
        db.add_user(message.from_user)
    
    characters = db.get_all_characters()
    markup = await kb.start_kb(characters)
    await message.answer(cfg.misc.messages.start)
    await state.finish()



async def receive(message: types.Message, state: FSMContext):
    
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    openai  = ctx_data.get()['openai']
    wait = await message.answer("Форматируется ответ…")
    voice_id = cfg.tg_bot.voice_id
    if message.content_type ==types.ContentType.VOICE :
        path = f"voice/{message.voice.file_id}.ogg"
        await message.voice.download(path)
        text = speech_to_text(path)
        
    elif message.content_type ==types.ContentType.TEXT :
        text = message.text
    responce = await create_responce(message,openai,text)
    path = text_to_speech(responce,voice_id)
    voice = types.InputFile(path)
    await message.answer_voice(voice)
    os.remove(path)
    # await message.answer(responce)
    await wait.delete()

async def mailing(message: types.Message):
    db: Database = ctx_data.get()['db']
    bot = ctx_data.get()['bot']
    result = message.get_args()
    users = db.get_all_users()
    for user in users:
        await bot.send_message(chat_id=user[2], text=result)    




async def client_add_profile(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    db: Database = ctx_data.get()['db']
    kb: Keyboards = ctx_data.get()['keyboards']
    
    

def register_user_handlers(dp: Dispatcher,kb: Keyboards):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(mailing, commands=["mailing"], state="*")

    dp.register_message_handler(receive,content_types=[types.ContentType.TEXT,types.ContentType.VOICE],state="*")
    
    dp.register_callback_query_handler(start, kb.back_cd.filter(), state="*")

