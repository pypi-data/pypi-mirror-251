import requests
from telebot import types
import uuid

class WhoID:
    def __init__(self, token):
        self.token: str = token

    def check_user(self, mail, password):
        try:
            response = requests.get(
                f'https://whoid.ru/api/get?token={self.token}&mail={mail}&password={password}'
            ).json()
            return response
        except Exception as e:
            return e

    def check_fio(self, fio):
        try:
            response = requests.get(
                f'https://whoid.ru/api/fio?token={self.token}&name={fio}'
            ).json()
            return response
        except Exception as e:
            return e

    def check_auth(self, id):
        try:
            response = requests.get(
                f'https://whoid.ru/api/auth/find?id={id}&token={self.token}'
            ).json()
            return response
        except Exception as e:
            return e

    def check_mail(self, mail):
        try:
            response = requests.get(
                f'https://whoid.ru/api/mail?token={self.token}&mail={mail}'
            ).json()
            return response
        except Exception as e:
            return e

class WhoID_TG:
    def create_button(self, bot_tag):
        keyboard = types.ReplyKeyboardMarkup()
        token = str(uuid.uuid4())
        web = types.WebAppInfo(
            f'https://whoid.ru/auth/login?token={token}&bot=true&link=https://t.me/{bot_tag}'
        )
        button = types.KeyboardButton(text='Войти с WhoID', web_app=web)
        keyboard.add(button)
        return keyboard

    def link_message(self, bot, message):
        message_id = message.text.split()[-1]
        chat_id = message.chat.id
        bot.send_message(chat_id, '🔒Подождите, идет безопасная авторизация через WhoID')
        if message_id != '/start':
            auth = WhoID('c5eb101b-a8fc-4e1e-b39a-050901f2e18d')
            info = auth.check_auth(message_id)
            try:
                if info['mail'] != None:
                    bot.send_message(
                        chat_id,
                        f'✅Успешная авторизация по почте {info["mail"]} через WhoID',
                        reply_markup=types.ReplyKeyboardRemove()
                    )
                    return {"status": "Success", "mail": info['mail']}
                else:
                    bot.send_message(
                        chat_id,
                        '❌Войти не получилось. Пожалуйста, повторите попытку',
                        reply_markup = types.ReplyKeyboardRemove()
                    )
                    return {"status": "Error"}
            except Exception as e:
                bot.send_message(
                    chat_id,
                    '❌Войти не получилось. Пожалуйста, повторите попытку',
                    reply_markup=types.ReplyKeyboardRemove()
                )
                return {"status": "Error"}

