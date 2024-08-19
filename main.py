import telebot
from telebot import types

TOKEN = '7475404155:AAEg5k0LbjEcQoQDwSH8BtijWCMDC1ep8bY'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
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
    if call.data.startswith('standart'):
        if 'uz' in call.data:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Standart obunasini sotib olish uchun mana shu karta raqamiga: 9860 5555 6666 7777 15$ to'lov qilishingiz lozim. "
                     "To'lov o'tganidan so'ng chekni skrin qilib va o'zingizni ID raqamingiz bilan tashlashingiz lozim!"
            )
        elif 'ru' in call.data:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Чтобы приобрести стандартную подписку, вам нужно оплатить 15 долларов на этот номер карты: 9860 5555 6666 7777. "
                     "После оплаты сделайте скриншот чека и отправьте его вместе со своим ID!"
            )
    elif call.data.startswith('pro'):
        if 'uz' in call.data:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Pro obunasini sotib olish uchun mana shu karta raqamiga: 9860 5555 6666 7777 30$ to'lov qilishingiz lozim. "
                     "To'lov o'tganidan so'ng chekni skrin qilib va o'zingizni ID raqamingiz bilan tashlashingiz lozim!"
            )
        elif 'ru' in call.data:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Чтобы приобрести про подписку, вам нужно оплатить 30 долларов на этот номер карты: 9860 5555 6666 7777. "
                     "После оплаты сделайте скриншот чека и отправьте его вместе со своим ID!"
            )


@bot.message_handler(content_types=['photo'])
def handle_image(message):
    language = 'uz'

    if language == 'uz':
        bot.send_message(
            message.chat.id,
            "To'lovingiz uchun rahmat, adminlar tomonidan tasdiqlangandan so'ng sizga avtomatik tarzda obuna beriladi!"
        )
    elif language == 'ru':
        bot.send_message(
            message.chat.id,
            "Спасибо за ваш платеж, после подтверждения администратором вам будет автоматически предоставлена подписка!"
        )


if __name__ == '__main__':
    bot.polling(none_stop=True)
