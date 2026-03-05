from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from weather import get_weather
from news_scrapping import get_local_agri_news
from community_reports import generate_community_alert

BOT_TOKEN = "8740019482:AAFDmiWQ2kYmiwWQHRtkMA-TYNOAhe4eKVg"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to AI Farmer Advisor 🌾\nSend your city name to get farming advisory."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    city = update.message.text

    weather = get_weather(city)
    news = get_local_agri_news(city)
    community = generate_community_alert(city)

    text = f"""
Weather in {city}: {weather['condition']}
Temperature: {weather['temperature']}°C

Community alert:
{community}

Latest agriculture news:
{news[0]}
"""

    await update.message.reply_text(text)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

print("Bot running...")
app.run_polling()