
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

import os
TOKEN = os.getenv("TOKEN")

OWNER_ID = -1003585110947

SERVICE, DATE, TIME, NAME, PHONE = range(5)

services = [["Маникюр","Стрижка"],["Консультация"]]
dates = [["Сегодня","Завтра"],["Через 2 дня"]]
times = [["10:00","12:00"],["14:00","16:00"],["18:00"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выберите услугу:",
        reply_markup=ReplyKeyboardMarkup(services, resize_keyboard=True)
    )
    return SERVICE

async def service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["service"] = update.message.text
    await update.message.reply_text(
        "Выберите дату:",
        reply_markup=ReplyKeyboardMarkup(dates, resize_keyboard=True)
    )
    return DATE

async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text
    await update.message.reply_text(
        "Выберите время:",
        reply_markup=ReplyKeyboardMarkup(times, resize_keyboard=True)
    )
    return TIME

async def time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["time"] = update.message.text
    await update.message.reply_text("Введите имя:")
    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Введите телефон:")
    return PHONE

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = context.user_data
    phone = update.message.text

    text = f"""
🔥 Новая запись!

Услуга: {data['service']}
Дата: {data['date']}
Время: {data['time']}
Имя: {data['name']}
Телефон: {phone}
"""

    await context.bot.send_message(chat_id=OWNER_ID, text=text)
    await update.message.reply_text("✅ Вы записаны!")
    return ConversationHandler.END


app = ApplicationBuilder().token(TOKEN).build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        SERVICE: [MessageHandler(filters.TEXT, service)],
        DATE: [MessageHandler(filters.TEXT, date)],
        TIME: [MessageHandler(filters.TEXT, time)],
        NAME: [MessageHandler(filters.TEXT, name)],
        PHONE: [MessageHandler(filters.TEXT, phone)],
    },
    fallbacks=[]
)

app.add_handler(conv)
app.run_polling()
