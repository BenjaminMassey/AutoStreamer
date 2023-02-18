# Libraries
from chatgpt_wrapper import ChatGPT
from datetime import datetime
import time, os, random

# Project Files
import speech, chat, mupen

key_file = open("google_key_path.txt", 'r')
key_data = key_file.read()
key_file.close()

config_file = open("config.txt", 'r')
config_data = config_file.read().split(" ::: ")
config_file.close()

do_mupen = False
if config_data[0] == "mupen":
    do_mupen = bool(eval(config_data[1]))

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_data

print("Loading ChatGPT...")

ai_bot = ChatGPT()

print("ChatGPT AI Bot is set up!")

if do_mupen:

    def setResetTime():
        global reset_time
        time_range = (1 * 60, 46 * 60) # from 1 minute to 46 minutes (in seconds)
        run_rng = random.randint(1, 100)
        if run_rng != 100:
            reset_time = ((time_range[1] - time_range[0]) * (run_rng / 100)) + time_range[0]
        else:
            reset_time = None
        print("Reset time set to", reset_time)

    reset_time = None
    setResetTime()
    start_time = datetime.now()

    print("Click into mupen64 now")

    time.sleep(3)

    print("Starting run and program...")

    mupen.start_tas()

print("Started!")

while True:
    options = ["!fun", "!story", "!twitch"]
    message = options[random.randint(0, len(options) - 1)]
    print("Bot chose:", message)
    
    #message = input("Input: ")
    
    response = None
    reset = False
    
    if do_mupen and reset_time is not None and \
        (datetime.now() - start_time).total_seconds() > reset_time:
        message = "!reset"
        print("Actually, RESET")
    
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
    elif do_mupen and message == "!reset":
        time.sleep(2)
        mupen.end_run()
        response = chat.reset(ai_bot)
        reset = True
    else:
        response = ai_bot.ask(message)
        
    if response is not None:
        filename = speech.text_to_wav("en-US-News-M", response, True)
        print("Response:", response, "(" + filename + ")")
    
    if do_mupen and reset:
        mupen.start_tas()
        setResetTime()
        start_time = datetime.now()
        
    time.sleep(1)

speech.text_to_wav("en-US-News-M", "Goodbye!", True)

print("Goodbye!")

time.sleep(2)
