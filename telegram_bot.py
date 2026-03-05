from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import speech_recognition as sr
from pydub import AudioSegment

from weather import get_weather
from news_scrapping import get_local_agri_news
from community_reports import generate_community_alert

BOT_TOKEN = "8740019482:AAFDmiWQ2kYmiwWQHRtkMA-TYNOAhe4eKVg"


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    city = update.message.text

    weather = get_weather(city)
    news = get_local_agri_news(city)
    community = generate_community_alert(city)

    reply = f"""
Weather in {city}: {weather['condition']}
Temperature: {weather['temperature']}°C

Community alert:
{community}

Latest agriculture news:
{news[0]}
"""

    await update.message.reply_text(reply)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    voice = await update.message.voice.get_file()
    await voice.download_to_drive("voice.ogg")

    sound = AudioSegment.from_ogg("voice.ogg")
    sound.export("voice.wav", format="wav")

    recognizer = sr.Recognizer()

    with sr.AudioFile("voice.wav") as source:
        audio = recognizer.record(source)

    city = recognizer.recognize_google(audio)

    weather = get_weather(city)
    news = get_local_agri_news(city)
    community = generate_community_alert(city)

    reply = f"""
Detected city: {city}

Weather: {weather['condition']}
Temperature: {weather['temperature']}°C

Community alert:
{community}

News:
{news[0]}
"""

    await update.message.reply_text(reply)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.VOICE, handle_voice))

print("Telegram bot running...")

app.run_polling()