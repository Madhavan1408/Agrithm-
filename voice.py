from gtts import gTTS

def generate_voice(text):

    speech = gTTS(text)

    speech.save("response.mp3")

    return "response.mp3"