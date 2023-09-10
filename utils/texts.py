from db import Database


class Texts:
    
    @staticmethod
    async def create_statistic(db: Database):
        characters = db.get_all_characters()
        users_count = db.get_users_count()

        text = '<b>Ститистика по персонажам:</b>\n\n'
        for character in characters:
            text += f"<b>Персонаж:</b> {character.name} выбран - {character.use_count}\n"
        text += f'\n<b>Всего пользователей:</b> {users_count}'

        return text
