from os import getenv
from dotenv import load_dotenv
from io import BytesIO
from telebot import TeleBot
from qrcode import QRCode

load_dotenv()

bot = TeleBot(getenv("TOKEN"))

def generate_qr(data: str, color: str) -> BytesIO:
    qr = QRCode(border=6)
    byte_qr = BytesIO()
    qr.add_data(data)
    qr.make(fit=True)
    qr.make_image(fill_color=color).save(byte_qr, format="PNG")
    byte_qr.seek(0)
    return byte_qr

@bot.message_handler(func=lambda message: message.text != "/start", content_types=["text"])
def qr_generation(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_photo(message.chat.id, generate_qr(message.text, "#2522d4"), caption=message.text)

    except:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "<b>Не удалось сгенерировать QR-код</b> Проверьте входные данные и попробуйте еще раз", parse_mode="html")

@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.send_message(message.chat.id, "<b>Добро пожаловать в QRBot</b>\nДля генерации QR-кода просто отправьте мне текст или ссылку", parse_mode="html")

def main() -> None:
    bot.infinity_polling()

if __name__ == '__main__': main()
