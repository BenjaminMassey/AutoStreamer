import google.cloud.texttospeech as tts
import os
from datetime import datetime
from playsound import playsound
from chatgpt_wrapper import ChatGPT

key_file = open("google_key_path.txt", 'r')
key_data = key_file.read()
key_file.close()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_data

def unique_languages_from_voices(voices):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set


def list_languages():
    client = tts.TextToSpeechClient()
    response = client.list_voices()
    languages = unique_languages_from_voices(response.voices)

    print(f" Languages: {len(languages)} ".center(60, "-"))
    for i, language in enumerate(sorted(languages)):
        print(f"{language:>10}", end="\n" if i % 5 == 4 else "")

def list_voices(language_code=None):
    client = tts.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = tts.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")


def text_to_wav(voice_name: str, text: str, play=False):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    now = datetime.now()
    time_str = now.strftime("--%m-%d-%Y--%H-%M-%S")

    directory = "./out/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename = directory + voice_name + time_str + ".wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        
    if play:
        playsound(filename)

    return filename

def chatRespond(username: str, message: str):
    base = "You are a Twitch streamer, responding to a chat message. Keep it to two sentence or less. The message reads: "
    response = bot.ask(base + message)
    return username + " said " + message + ". " + response

def randomFun():
    message = "You are Twitch streamer, trying to kill time. Say something interesting and unique in two sentences or less."
    return bot.ask(message)

def randomStory():
    message = "You are a Twitch streamer, telling a story. Keep it to two sentences or less, and make it relatable."
    return bot.ask(message)

bot = ChatGPT()

print("Bot is set up!")

while True:
    response = None
    message = input("Message: ")
    
    if message == "!exit":
        break
    elif message == "!fun":
        response = randomFun()
    elif message == "!story":
        reponse = randomStory()
    elif message[:6] == "!chat ":
        response = chatRespond("Bean", message[6:])
    else:
        response = bot.ask(message)
        
    if response is not None:
        filename = text_to_wav("en-US-News-M", response, True)
        print("Response:", response, "(" + filename + ")")

print("Goodbye!")
