from config.config import Config
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup,\
    ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton

class Keyboards:
    def __init__(self,cfg:Config) -> None:
        self.text = cfg.misc.buttons_texts
        self.start_cd = CallbackData("start","character_id")
        
        self.back_cd = CallbackData("back")
    
    
    async def start_kb(self,characters:tuple):
    
        kb = InlineKeyboardMarkup()
        for character in characters:
            kb.add(InlineKeyboardButton(text=character.name, callback_data=self.start_cd.new(character_id=character.id)))
    
        return kb
    
    async def admin_kb(self):
        kb = InlineKeyboardMarkup()
    
        kb.add(InlineKeyboardButton(text="Дать доступ",callback_data="access grand"))
        kb.add(InlineKeyboardButton(text="Прекратить доступ",callback_data="access denied"))
        kb.add(InlineKeyboardButton(text="Назад",callback_data=self.back_cd.new()))
        
        return kb
        
    
    async def back_kb(self):
        kb = InlineKeyboardMarkup()

        kb.add(InlineKeyboardButton(text="Назад",callback_data=self.back_cd.new()))

        return kb