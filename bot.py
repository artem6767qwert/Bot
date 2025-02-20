import telebot
import requests
from telebot import types
import os

TOKEN = os.getenv("TOKEN")
OZON_API_KEY = os.getenv("OZON_API_KEY")
WB_API_KEY = os.getenv("WB_API_KEY")
PARTNER_ID = os.getenv("PARTNER_ID")

bot = telebot.TeleBot(TOKEN)

def get_ozon_discounts():
    url = "https://api-seller.ozon.ru/v1/product/list"
    headers = {"Client-Id": "YOUR_CLIENT_ID", "Api-Key": OZON_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        products = data.get('result', [])[:5]
        return "\n".join([f"{p['name']} - {p['price']['discount_price']} руб.\nСсылка: https://www.ozon.ru/context/detail/id/{p['id']}/?partner={PARTNER_ID}" for p in products])
    return "Не удалось получить данные с Ozon."

def get_wb_discounts():
    url = "https://suppliers-api.wildberries.ru/api/v1/supplier/stocks"
    headers = {"Authorization": WB_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        products = data.get('stocks', [])[:5]
        return "\n".join([f"{p['name']} - {p['discount_price']} руб.\nСсылка: https://www.wildberries.ru/catalog/{p['nm_id']}/detail.aspx?partner={PARTNER_ID}" for p in products])
    return "Не удалось получить данные с Wildberries."

def get_discounts(marketplace):
    if marketplace == "Ozon":
        return get_ozon_discounts()
    elif marketplace == "Wildberries":
        return get_wb_discounts()
    elif marketplace == "Яндекс Маркет":
        return "Яндекс Маркет API пока не подключен."
    return "Нет данных о скидках."

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Ozon")
    btn2 = types.KeyboardButton("Wildberries")
    btn3 = types.KeyboardButton("Яндекс Маркет")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Привет! Выберите маркетплейс для поиска скидок:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Ozon", "Wildberries", "Яндекс Маркет"])
def search_discounts(message):
    marketplace = message.text
    discounts = get_discounts(marketplace)
    bot.send_message(message.chat.id, f"Скидки на {marketplace}:\n{discounts}")

if __name__ == "__main__":
    print("Бот запущен")
    bot.polling(none_stop=True)
