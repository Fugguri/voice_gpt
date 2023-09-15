from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.handler import ctx_data
from aiogram.dispatcher import FSMContext

from utils import *
from config.config import Config
from db import Database
from keyboards.keyboards import Keyboards

import os
from .admin import admin


async def start(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    try:
        db.get_user(message.from_user.id)
    except:
        db.add_user(message.from_user)

    characters = db.get_all_characters()
    markup = await kb.start_kb(characters)
    try:
        await message.answer(cfg.misc.messages.start, reply_markup=markup)
    except:
        await message.message.answer(cfg.misc.messages.start, reply_markup=markup)

    await state.finish()


async def check(callback: types.CallbackQuery):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    channels_text = "Чтобы пользоваться сервисом сначала подпишитесь на канал.\nВы не подписаны на:\n"
    all_joined = True
    markup = types.InlineKeyboardMarkup()
    for channel in db.get_channels():

        member = await get_channel_member(channel.channel_id, callback)
        if not is_member_in_channel(member):
            markup.add(types.InlineKeyboardButton(
                text=channel.name, url=channel.link))
            all_joined = False
            channels_text += "\n"+channel.name
        # markup.add(types.InlineKeyboardButton(
        #     text="Проверить подписку", callback_data="check"))
    if not all_joined:
        try:
            await callback.message.answer(channels_text, reply_markup=markup)
        except:
            await callback.answer(channels_text, reply_markup=markup)

    return all_joined


async def set_caracter(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    character = db.update_character_count(callback_data["character_id"])
    await state.set_data({"character_id": character.id, "role_settings": character.role_settings, "voice_id": character.voice_id})

    await callback.message.answer(character.description)


async def receive(message: types.Message, state: FSMContext):
    cfg: Config = ctx_data.get()['config']
    kb: Keyboards = ctx_data.get()['keyboards']
    db: Database = ctx_data.get()['db']
    openai = ctx_data.get()['openai']
    if not await check(message):
        return
    data = await state.get_data()
    try:
        role_settings = data['role_settings']
        voice_id = data['voice_id']
    except:
        role_settings = cfg.tg_bot.role_settings
        voice_id = cfg.tg_bot.voice_id
    wait = await message.answer("Форматируется ответ…")

    if message.content_type == types.ContentType.VOICE:
        path = f"voice/{message.voice.file_id}.ogg"
        await message.voice.download(path)
        text = await speech_to_text(path)

    elif message.content_type == types.ContentType.TEXT:
        text = message.text

    responce = await create_responce(message, role_settings, openai, text)
    path = await text_to_speech(responce, voice_id)
    voice = types.InputFile(path)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text="Меню"))
    await message.answer_voice(voice, reply_markup=markup)
    os.remove(path)

    await wait.delete()


async def mailing(message: types.Message):
    db: Database = ctx_data.get()['db']
    bot = ctx_data.get()['bot']
    result = message.get_args()
    users = db.get_all_users()
    for user in users:
        await bot.send_message(chat_id=user[2], text=result)


async def back(callback: types.CallbackQuery, state: FSMContext, callback_data: dict):
    db: Database = ctx_data.get()['db']
    kb: Keyboards = ctx_data.get()['keyboards']

    if callback_data['role'] == "admin":
        await admin(callback.message)
    if callback_data['role'] == "user":
        await start(callback.message, state)

    await callback.message.delete()


def register_user_handlers(dp: Dispatcher, kb: Keyboards):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(mailing, commands=["mailing"], state="*")
    dp.register_message_handler(start, lambda x: x.text == "Меню", state="*")

    dp.register_message_handler(receive, content_types=[
                                types.ContentType.TEXT, types.ContentType.VOICE], state="*")
    dp.register_callback_query_handler(
        set_caracter, kb.start_cd.filter(), state="*")
    dp.register_callback_query_handler(
        check, lambda x: x.data == "check", state="*")
    dp.register_callback_query_handler(back, kb.back_cd.filter(), state="*")
