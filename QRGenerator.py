from os import getenv
from dotenv import load_dotenv
from io import BytesIO
from qrcode import QRCode
from redis import Redis
from telebot import TeleBot

load_dotenv()

bot = TeleBot(getenv("TOKEN"))



def get_user_color(user_id: int) -> str:
    color = Redis(host=getenv("REDIS_HOST"), port=getenv("REDIS_PORT"), decode_responses=True).get(user_id)
    return color if color else "#000000"

def set_user_color(user_id: int, color: str) -> bool: 
    return True if Redis(host=getenv("REDIS_HOST"), port=getenv("REDIS_PORT"), decode_responses=True).set(user_id, color) else False


def generate_qr(data: str, color="#000000") -> BytesIO:
    byte_qr = BytesIO()

    qr = QRCode(border=6)
    qr.add_data(data)
    qr.make(fit=True)
    qr.make_image(fill_color=color).save(byte_qr, format="PNG")

    byte_qr.seek(0)
    return byte_qr



@bot.message_handler(func=lambda message: message.text.startswith("#") and len(message.text) == 7)
def set_color(message):
    bot.send_message(message.chat.id, f"<b>Персональный цвет QR кода был изменен</b>\n Текущий цвет: <code>{message.text}</code>" if set_user_color(message.from_user.id, message.text) else f"<b>Ошибка выбора цвета QR кода</b>\n Персональный цвет QR кода не был изменен, попробуйте ещe раз", parse_mode="html")

@bot.message_handler(func=lambda message: message.text not in ["/start", "/color"])
def qr_generation(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_photo(message.chat.id, generate_qr(message.text, get_user_color(message.from_user.id)),caption=message.text)
    except:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "<b>Не удалось сгенерировать QR-код</b> Проверьте входные данные и попробуйте еще раз", parse_mode="html")

@bot.message_handler(commands=["color"])
def start_handler(message):
    bot.send_message(message.chat.id, f"<b>Выбрать цвет QR кода</b>\n\nДля выбора цвета QR кода отправьте HEX-код желаемого цвета в формате: <code>#000000</code>\n\nВаш текущий цвет: <code>{get_user_color(message.from_user.id)}</code>", parse_mode="html")

@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.send_message(message.chat.id, "<b>Добро пожаловать в QRBot</b>\n\nДля генерации QR-кода просто отправьте мне текст или ссылку, которую вы желаете преобразовать", parse_mode="html")



def main() -> None:
    bot.infinity_polling()

if __name__ == '__main__': main()
