# Libraries
from chatgpt_wrapper import ChatGPT
from datetime import datetime
import time, os, random, livesplit

# Project Files
import speech, chat, mupen, settings

app_settings = settings.Settings()

do_mupen = bool(eval(app_settings.get("mupen")))

key_data = app_settings.get("google_path")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_data

print("Loading ChatGPT...")

ai_bot = ChatGPT()

print("ChatGPT AI Bot is set up!")

if do_mupen:

    ls = livesplit.Livesplit()

    def setResetTime():
        global reset_time
        time_range = (1 * 60, 46 * 60) # from 1 minute to 46 minutes (in seconds)
        #time_range = (2 * 60, 3 * 60) # from 2 minutes to 3 minutes (in seconds) (debug)
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

    mupen.start_tas(app_settings)
    
    ls.startTimer()

print("Started!")

while True:
    options = ["!fun", "!story", "!joke", "!mario"]
    message = options[random.randint(0, len(options) - 1)]
    if random.random() < float(eval(app_settings.get("twitch_chance"))):
        message = "!twitch"
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
        response = chat.direct("fun", ai_bot, app_settings)
    elif message == "!story":
        response = chat.direct("story", ai_bot, app_settings)
    elif message == "!joke":
        response = chat.direct("joke", ai_bot, app_settings)
    elif message == "!mario":
        response = chat.direct("mario", ai_bot, app_settings)
    elif message[:6] == "!chat ":
        response = chat.respond(ai_bot, "Developer", message[6:], app_settings)
    elif message[:6] == "!test ":
        response = message[6:]
    elif message == "!twitch":
        twitchfile = open("latest.txt", "r")
        data = twitchfile.read().split(" ::: ")
        twitchfile.close()
        if len(data) == 2:
            response = chat.respond(ai_bot, data[0], data[1], app_settings)
        else:
            print("Broken data from twitch file 'latest.txt'")
            continue
    elif do_mupen and message == "!reset":
        time.sleep(2)
        mupen.end_run()
        response = chat.direct("reset", ai_bot, app_settings)
        reset = True
    else:
        response = ai_bot.ask(message)
        
    if response is not None:
        filename = speech.text_to_wav("en-US-News-M", response, True)
        print("Response:", response, "(" + filename + ")")
    
    if do_mupen and reset:
        ls.reset()
        mupen.start_tas(app_settings)
        ls.startTimer()
        setResetTime()
        start_time = datetime.now()
        
    time.sleep(1)

speech.text_to_wav("en-US-News-M", "Goodbye!", True)

print("Goodbye!")

time.sleep(2)
