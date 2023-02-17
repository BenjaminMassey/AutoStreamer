# Libraries
from chatgpt_wrapper import ChatGPT
import time, os, random

# Project Files
import speech, chat

key_file = open("google_key_path.txt", 'r')
key_data = key_file.read()
key_file.close()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_data

ai_bot = ChatGPT()

print("ChatGPT AI Bot is set up!")

while True:
    options = ["!fun", "!story", "!twitch"]
    message = options[random.randint(0, len(options) - 1)]
    print("Bot chose:", message)
    
    #message = input("Input: ")
    
    response = None
    
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
        twitchfile = open("latest.txt", "r")
        data = twitchfile.read().split(" ::: ")
        twitchfile.close()
        if len(data) == 2:
            response = chat.respond(ai_bot, data[0], data[1])
        else:
            print("Broken data from twitch file 'latest.txt'")
            continue
    else:
        response = ai_bot.ask(message)
        
    if response is not None:
        filename = speech.text_to_wav("en-US-News-M", response, True)
        print("Response:", response, "(" + filename + ")")
    
    time.sleep(3)

speech.text_to_wav("en-US-News-M", "Goodbye!", True)

print("Goodbye!")

time.sleep(2)
