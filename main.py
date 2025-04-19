import telebot
from telebot import types
from datetime import datetime
from dotenv import load_dotenv
import os
import ast

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = ast.literal_eval(os.getenv("ADMIN_IDS"))

bot = telebot.TeleBot(TOKEN)

START_HOUR = 9
END_HOUR = 22

user_data = {}


def is_within_operating_hours():
    current_hour = datetime.now().hour
    return START_HOUR <= current_hour < END_HOUR


def is_admin(user_id):
    return user_id in ADMIN_IDS


@bot.message_handler(commands=['start'])
def start_command(message):
    user_data[message.chat.id] = {'language': None, 'subscription': None, 'collecting_id': False}
    markup = types.InlineKeyboardMarkup()
    btn_uz = types.InlineKeyboardButton("Uzbek", callback_data='lang_uz')
    btn_ru = types.InlineKeyboardButton("Russian", callback_data='lang_ru')
    markup.add(btn_uz, btn_ru)

    bot.send_message(
        message.chat.id,
        'Assalomu aleykum bu cryptoindex saytining rasmiy telegram boti hisoblanadi. Boshlash uchun birinchi navbatda tilni tanlang \n'
        'Здравствуйте, это официальный телеграмм-бот криптоиндекса. Сначала выберите язык, чтобы начать!!',
        reply_markup=markup
    )


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        message.chat.id,
        'Bu bot orqali siz cryptoindex saytidan obuna sotib olishingiz mumkin! \n'
        'Через этого бота вы можете купить подписку на сайте криптоиндекса!'
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def language_selection(call):
    user_data[call.message.chat.id] = {'language': call.data.split('_')[1], 'subscription': None,
                                       'collecting_id': False}

    if call.data == 'lang_uz':
        markup = types.InlineKeyboardMarkup()
        btn_std = types.InlineKeyboardButton("Standart", callback_data='standart_uz')
        btn_pro = types.InlineKeyboardButton("Pro", callback_data='pro_uz')
        markup.add(btn_std, btn_pro)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Cryptoindex saytida 2 xil obuna turi mavjud. Birinchisi bu standart - oyiga 15$, ikkinchisi pro - oyiga 30$. Qaysi birini tanlaysiz?",
            reply_markup=markup
        )
    elif call.data == 'lang_ru':
        markup = types.InlineKeyboardMarkup()
        btn_std = types.InlineKeyboardButton("Standart", callback_data='standart_ru')
        btn_pro = types.InlineKeyboardButton("Pro", callback_data='pro_ru')
        markup.add(btn_std, btn_pro)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="На сайте Cryptoindex есть 2 типа подписки. Первая - стандартная - 15 долларов в месяц, вторая - про - 30 долларов в месяц. Какой из них вы выберете?",
            reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith('standart_') or call.data.startswith('pro_'))
def subscription_selection(call):
    language = user_data[call.message.chat.id]['language']
    user_data[call.message.chat.id]['subscription'] = call.data.split('_')[0]
    user_data[call.message.chat.id]['collecting_id'] = True

    if call.data.startswith('standart'):
        if language == 'uz':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Standart obunasini sotib olish uchun mana shu karta raqamiga: 9860 5555 6666 7777 15$ to'lov qilishingiz lozim. "
                     "To'lov o'tganidan so'ng chekni skrin qilib va o'zingizni ID raqamingiz bilan tashlashingiz lozim!"
            )
        elif language == 'ru':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Чтобы приобрести стандартную подписку, вам нужно оплатить 15 долларов на этот номер карты: 9860 5555 6666 7777. "
                     "После оплаты сделайте скриншот чека и отправьте его вместе со своим ID!"
            )
    elif call.data.startswith('pro'):
        if language == 'uz':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Pro obunasini sotib olish uchun mana shu karta raqamiga: 9860 5555 6666 7777 30$ to'lov qilishingiz lozim. "
                     "To'lov o'tganidan so'ng chekni skrin qilib va o'zingizni ID raqamingiz bilan tashlashingiz lozim!"
            )
        elif language == 'ru':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Чтобы приобрести про подписку, вам нужно оплатить 30 долларов на этот номер карты: 9860 5555 6666 7777. "
                     "После оплаты сделайте скриншот чека и отправьте его вместе со своим ID!"
            )


@bot.message_handler(content_types=['text'])
def handle_user_id(message):
    if user_data.get(message.chat.id, {}).get('collecting_id', False):
        language = user_data.get(message.chat.id, {}).get('language', 'uz')
        if message.text.isdigit() and len(message.text) == 12:
            user_data[message.chat.id]['user_id'] = message.text
            bot.send_message(
                message.chat.id,
                "ID qabul qilindi. Endi to'lovni tasdiqlovchi rasmni yuboring!" if language == 'uz'
                else "Ваш идентификационный номер принят. Отправьте фото подтверждения оплаты прямо сейчас!"
            )
        else:
            bot.send_message(
                message.chat.id,
                "Iltimos, ID raqamini to'g'ri formatda kiriting (12 ta raqam)!" if language == 'uz'
                else "Пожалуйста, введите идентификационный номер в правильном формате (12 цифр)!"
            )
    else:
        language = user_data.get(message.chat.id, {}).get('language')
        if language is None:
            bot.send_message(
                message.chat.id,
                "Birinchi navbatda tilni tanglang                                    Сначала выберите язык!"
            )
        elif user_data.get(message.chat.id, {}).get('subscription') is None:
            bot.send_message(
                message.chat.id,
                "Birinchi navbatda obuna turini tanglang!" if language == 'uz'
                else "Прежде всего выберите тип подписки!"
            )
        else:
            bot.send_message(
                message.chat.id,
                "Obuna tanlang va ID raqamingizni kiriting!" if language == 'uz'
                else "Выберите подписку и введите свой идентификационный номер!"
            )


@bot.message_handler(content_types=['photo'])
def handle_image(message):
    username = message.from_user.username
    full_name = f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip() or "No name"
    user_link = f"@{username}" if username else f"{full_name}"

    user_provided_id = user_data.get(message.chat.id, {}).get('user_id', "No user-provided ID")
    language = user_data.get(message.chat.id, {}).get('language', 'uz')

    if not is_within_operating_hours():
        bot.send_message(
            message.chat.id,
            "Kecharasiz , bot faqat 09:00 dan, 22:00 gacha ishlaydi. Lekin havotir olmang, bot ishga tushishi bilanoq adminlarimiz "
            "sizning to'lovingizni ko'rib chiqishadi va sizga obunani berishadi!" if language == 'uz'
            else "Бот работает только с 09:00 до 22:00. Но не волнуйтесь, как только бот заработает, наши администраторы проверят ваш платеж и оформят вам подписку!"
        )
    else:
        bot.send_message(
            message.chat.id,
            "To'lovingiz uchun rahmat, adminlar tomonidan 1 soat ichida tasdiqlangandan so'ng sizga avtomatik tarzda obuna beriladi!" if language == 'uz'
            else "Спасибо за оплату, вы будете автоматически подписаны после одобрения администраторами в течение 1 часа!"
        )

    for admin_id in ADMIN_IDS:
        bot.send_photo(
            admin_id,
            message.photo[-1].file_id,
            caption=f"New payment received.\nUser ID: {message.chat.id}\nTelegram Username: {user_link}\nUser-Provided ID: {user_provided_id}"
        )


@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if is_admin(message.chat.id):
        bot.send_message(message.chat.id, "Welcome to the admin panel!")
    else:
        bot.send_message(message.chat.id, "You are not authorized to access the admin panel.")


if __name__ == '__main__':
    bot.polling(none_stop=True)
