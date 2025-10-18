import telebot
from telebot import types

# Bot tokenini shu yerga yozing
TOKEN = "8356080557:AAFDW0gRYarLExDrlFAFvkHcUFeaXvu8GQ8"
bot = telebot.TeleBot(TOKEN)

# Dars jadvali
dars_jadvali = {
    "Dushanba": ["Kelajak Soat", "Ingliz tili", "Texnologiya", "Ona tili", "Rus tili", "Geometriya"],
    "Seshanba": ["Algebra", "Kimyo", "J-tar", "Biologiya", "Fizika", "Geometriya"],
    "Chorshanba": ["Algebra", "Chizmachilik", "Huquq", "O'zbekiston Tarixi", "Adabiyot", "Ingliz tili"],
    "Payshanba": ["Rus tili", "Adabiyot", "Ingliz tili", "Fizika", "Biologiya", "Ona tili"],
    "Juma": ["Algebra", "J-tar", "Tarbiya", "Ona tili", "Geometriya", "O'zbekiston Tarixi"],
    "Shanba": ["Geografiya", "Kimyo", "Jahon tarixi", "Informatika"]
}

# Foydalanuvchi tanlagan kunni saqlash
user_day_selection = {}

# /start buyrug‘i
@bot.message_handler(commands=['start'])
def start(message):
    about_text = ("DarsJadvalBot📌\n\n"
                  "Men sizning dars jadvalingizni tez va oson ko‘rsataman. "
                  "Kunlar bo‘yicha jadvalni tanlang va kerakli ma’lumotni darhol oling.\n\n"
                  "Faoliyat: jadvalni aniq, minimal va professional ko‘rsatadi.")
    bot.send_message(message.chat.id, about_text)
    send_days(message)

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, "Qanday yordam kerak?\n\nBuyruqlar:\n/start - Botni ishga tushirish\n/help - Yordam olish\n/about - Bot haqida ma'lumot")

@bot.message_handler(commands=['about'])
def about_message(message):
    bot.reply_to(message, "Bu bot MyJadvalBot nomli loyiha bo‘lib, foydalanuvchilarga dars jadvalini qulay tarzda ko‘rsatish uchun @vnz4x tomonidan yaratilgan.")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Salom! 👋\nMen MyJadvalBotman.\nSizga dars jadvalini ko‘rsatish va eslatmalar berishda yordam beraman.")

# Kunlar inline tugmalar bilan
def send_days(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for kun in dars_jadvali.keys():
        markup.add(types.InlineKeyboardButton(kun, callback_data=kun))
    bot.send_message(message.chat.id, "Kunlardan birini tanlang:", reply_markup=markup)

# Inline tugmalar callback
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.message.chat.id
    kun = call.data

    # Agar foydalanuvchi boshqa kun tanlagan bo‘lsa, eskisini o‘chirish
    if user_id in user_day_selection:
        old_msg_id = user_day_selection[user_id].get("msg_id")
        try:
            bot.delete_message(user_id, old_msg_id)
        except:
            pass

    # Jadvalni chiqarish
    jadval = dars_jadvali.get(kun)
    text = f"📅 {kun} dars jadvali:\n"
    for i, fan in enumerate(jadval, start=1):
        text += f"{i}-soat: {fan}\n"

    # Professional minimal stiker qo‘yish (xohlasa)
    # bot.send_sticker(user_id, "STICKER_FILE_ID")

    sent_msg = bot.send_message(user_id, text)
    user_day_selection[user_id] = {"day": kun, "msg_id": sent_msg.message_id}

# Botni ishga tushurish
bot.infinity_polling()
