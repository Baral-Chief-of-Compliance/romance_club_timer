from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
import os
import datetime
import redis
from dotenv import load_dotenv


KEYBOARD_STANDARD = Keyboard(one_time=False, inline=False)
KEYBOARD_STANDARD.add(Text("Забрала алмазики"), color=KeyboardButtonColor.POSITIVE)
KEYBOARD_STANDARD.add(Text("Сброс"), color=KeyboardButtonColor.NEGATIVE)


load_dotenv()
API_KEY = os.getenv('API_KEY')

user_db = redis.Redis(host='localhost', port=6379, db=1)

bot = Bot(token=API_KEY)
bot.labeler.vbml_ignore_case = True


@bot.on.private_message(text='начать')
async def send_keyboard(message: Message):
    await message.answer('Я бот таймер клуба романтики'
                         '\nНажвмите на кнопку Забрала алмазики, чтобы запустить таймер на полтора часа'
                         , keyboard=KEYBOARD_STANDARD)


@bot.on.private_message(text='забрала алмазики')
async def send_inf(message: Message):
    user_info = message.peer_id
    now = datetime.datetime.now().strftime('%H:%M')
    time_to_get_diamonds = (datetime.datetime.now() + datetime.timedelta(hours=1, minutes=30)).strftime('%H:%M')
    print(f'\n\n{user_info}')
    print(f'\n\n{now}')
    print(f'\n\n{time_to_get_diamonds}')
    user_db.set(user_info, time_to_get_diamonds)
    await message.answer('Таймер запущен')


@bot.loop_wrapper.interval(seconds=60)
async def notification():

    keys = user_db.keys()
    now = datetime.datetime.now().strftime('%H:%M')
    for k in keys:
        if user_db.get(k).decode('utf-8') == now:
            await bot.api.messages.send(peer_id=k.decode('utf-8'), message="Вы забрали алмазики?",random_id=0)

bot.run_forever()