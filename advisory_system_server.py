from fastapi import FastAPI, Request
from weather import get_weather
from news_scrapping import get_local_agri_news
from community_reports import generate_community_alert
from voice import generate_voice
from logger import write_log
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from datetime import datetime

app = FastAPI()

# Twilio credentials
ACCOUNT_SID = "YOUR_TWILIO_SID"
AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_NUMBER = "YOUR_TWILIO_NUMBER"

client = Client(ACCOUNT_SID, AUTH_TOKEN)


# ---------------------------------------------------
# SIMPLE FILE LOGGER
# ---------------------------------------------------
def log_server(event, data):

    with open("server_log.txt", "a") as f:
        log_line = f"{datetime.now()} | {event} | {data}\n"
        f.write(log_line)


# ---------------------------------------------------
# FARMER ADVISORY API
# ---------------------------------------------------
@app.get("/farmer-advisory")
def farmer_advisory(city: str, crop: str):

    log_server("API_REQUEST", {"city": city, "crop": crop})

    weather = get_weather(city)
    news = get_local_agri_news(city)
    community_alert = generate_community_alert(city)

    text = f"""
    Weather condition: {weather['condition']}.
    Temperature {weather['temperature']} degree.

    Community alert: {community_alert}

    Latest news: {news[0]}
    """

    audio = generate_voice(text)

    log_server("VOICE_GENERATED", {"city": city})

    return {"audio": audio, "text": text}


# ---------------------------------------------------
# MISSED CALL HANDLER
# ---------------------------------------------------
@app.post("/missed-call")
async def missed_call(request: Request):

    form_data = await request.form()
    farmer_number = form_data.get("From")

    log_server("MISSED_CALL_RECEIVED", farmer_number)

    # Call farmer back automatically
    call = client.calls.create(
        to=farmer_number,
        from_=TWILIO_NUMBER,
        url="https://your-ngrok-url/ivr"
    )

    log_server("CALLBACK_INITIATED", farmer_number)

    return {"status": "callback started"}


# ---------------------------------------------------
# IVR START POINT
# ---------------------------------------------------
@app.post("/ivr")
async def ivr(request: Request):

    response = VoiceResponse()

    gather = Gather(
        input="speech",
        action="/process-speech",
        method="POST",
        speechTimeout="auto"
    )

    gather.say(
        "Welcome to AI Farmer Advisory. Please say your city name after the beep.",
        voice="alice"
    )

    response.append(gather)

    log_server("IVR_STARTED", "waiting for city")

    return str(response)


# ---------------------------------------------------
# PROCESS FARMER SPEECH
# ---------------------------------------------------
@app.post("/process-speech")
async def process_speech(request: Request):

    form_data = await request.form()
    city = form_data.get("SpeechResult", "unknown")

    log_server("CITY_DETECTED", city)

    weather = get_weather(city)
    news = get_local_agri_news(city)
    community_alert = generate_community_alert(city)

    advisory = f"""
    Weather condition in {city} is {weather['condition']}.
    Temperature {weather['temperature']} degree.

    Community alert: {community_alert}

    Latest news: {news[0]}
    """

    log_server("ADVISORY_GENERATED", city)

    response = VoiceResponse()
    response.say(advisory, voice="alice")

    return str(response)