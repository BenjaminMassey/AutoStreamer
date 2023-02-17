import google.cloud.texttospeech as tts
import os
from datetime import datetime
from playsound import playsound
from chatgpt_wrapper import ChatGPT
from twitchio.ext import commands
import threading
import asyncio
import time

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
    base = "You are a Twitch streamer, responding to a chat message. Keep it to two sentences or less. The message reads: "
    response = ai_bot.ask(base + message)
    return username + " said " + message + ". " + response

def randomFun():
    message = "You are Twitch streamer, trying to kill time. Say something interesting and unique in two sentences or less."
    return ai_bot.ask(message)

def randomStory():
    message = "You are a Twitch streamer, telling a story. Keep it to two sentences or less, and make it relatable."
    return ai_bot.ask(message)

class TwitchBot(commands.Bot):

    latest = ("", "")

    def __init__(self, auth, channel):
        super().__init__(
            token=auth,
            prefix='?',
            initial_channels=[channel]
        )

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return
        
        user = str(message.author.name)
        msg = str(message.content)

        self.latest = (user, msg)
        
        print(user + " says '" + msg + "'.")
        
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')

ai_bot = ChatGPT()

print("ChatGPT AI Bot is set up!")

twitch_data_file = open("./twitch_data.txt", "r")
auth = twitch_data_file.readline().replace("\n","").replace(" ", "")
channel = twitch_data_file.readline().replace("\n","").replace(" ", "")
twitch_data_file.close()

class TwitchThread(threading.Thread):
    
    def __init__(self, auth, channel):
        threading.Thread.__init__(self)
        self.bot = TwitchBot(auth, channel)
        
    def run(self):
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.bot.run())
        except:
            pass


twitch_thread = TwitchThread(auth, channel)
twitch_thread.start()

print ("Twitch Bot is set up!")

while True:
    response = None
    message = input("Message: ")
    
    if message == "!exit":
        break
    elif message == "!fun":
        response = randomFun()
    elif message == "!story":
        response = randomStory()
    elif message[:6] == "!chat ":
        response = chatRespond("Developer", message[6:])
    elif message == "!twitch":
        response = chatRespond(twitch_thread.bot.latest[0],\
                               twitch_thread.bot.latest[1])
    else:
        response = ai_bot.ask(message)
        
    if response is not None:
        filename = text_to_wav("en-US-News-M", response, True)
        print("Response:", response, "(" + filename + ")")

text_to_wav("en-US-News-M", "Goodbye!", True)

print("Goodbye!")

time.sleep(1)
