import asyncio

users_message = {}


async def create_responce(message, role_settings, openai, text):
    try:
        try:
            users_message[message.from_user.id]
        except:
            users_message[message.from_user.id] = [{"role": "user", "content": "Твои ответы не должны быть больше 1000 символов", }, {
                "role": "user", "content": role_settings, }]
        print(users_message[message.from_user.id][1]["content"])
        if role_settings != users_message[message.from_user.id][1]["content"]:
            users_message[message.from_user.id] = [{"role": "user", "content": "Твои ответы не должны быть больше 1000 символов", }, {
                "role": "user", "content": role_settings, }]
        print(users_message[message.from_user.id])
        users_message[message.from_user.id].append(
            {"role": "user", "content": text})
        responce = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=users_message[message.from_user.id]
        )
        answer = responce['choices'][0]['message']['content']
        users_message[message.from_user.id].append(
            {"role": "assistant", "content": answer})
    except openai.error.RateLimitError as ex:
        print(ex)
        await asyncio.sleep(20)
        await create_responce(message, openai)

    except Exception as ex:
        print(ex)
        users_message[message.from_user.id] = []
        await message.reply("Не понимаю, сформулируйте подругому")

    return responce['choices'][0]['message']['content']
