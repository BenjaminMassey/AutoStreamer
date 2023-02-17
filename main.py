# Libraries
from chatgpt_wrapper import ChatGPT
import threading, time

# Project Files
import speech, twitch, chat, os

key_file = open("google_key_path.txt", 'r')
key_data = key_file.read()
key_file.close()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_data

ai_bot = ChatGPT()

print("ChatGPT AI Bot is set up!")

twitch_data_file = open("./twitch_data.txt", "r")
auth = twitch_data_file.readline().replace("\n","").replace(" ", "")
channel = twitch_data_file.readline().replace("\n","").replace(" ", "")
twitch_data_file.close()

twitch_thread = twitch.TwitchThread(auth, channel)
twitch_thread.start()

print ("Twitch Bot is set up!")

while True:
    response = None
    message = input("Input: ")
    
    if message == "!exit":
        break
    elif message == "!fun":
        response = chat.fun(ai_bot)
    elif message == "!story":
        response = chat.story(ai_bot)
    elif message[:6] == "!chat ":
        response = chat.respond(ai_bot,"Developer", message[6:])
    elif message[:6] == "!test ":
        response = message[6:]
    elif message == "!twitch":
        response = chat.respond(ai_bot,\
                                twitch_thread.bot.latest[0],\
                                twitch_thread.bot.latest[1])
    else:
        response = ai_bot.ask(message)
        
    if response is not None:
        filename = speech.text_to_wav("en-US-News-M", response, True)
        print("Response:", response, "(" + filename + ")")

speech.text_to_wav("en-US-News-M", "Goodbye!", True)

print("Goodbye!")

time.sleep(1)
