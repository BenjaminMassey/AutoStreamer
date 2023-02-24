# Libraries
from chatgpt_wrapper import ChatGPT
from datetime import datetime
from profanity_check import predict_prob
import time, os, random, livesplit, numpy

# Project Files
import speech, chat, mupen, settings, twitch_api

app_settings = settings.Settings()

do_mupen = bool(eval(app_settings.get("mupen")))

predict = bool(eval(app_settings.get("predictions")))

key_data = app_settings.get("google_path")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_data

print("Loading ChatGPT...")

ai_bot = ChatGPT()

print("ChatGPT AI Bot is set up!")

print("Loading Twitch API...")

tapi = twitch_api.TwitchAPI(\
    app_settings.get("twitch_channel"),\
    app_settings.get("twitch_client_id"),\
    app_settings.get("twitch_client_secret"))

print("Twitch API is set up!")

predict_time = None

if do_mupen:
    
    ls = livesplit.Livesplit()

    def setResetTime():
        global reset_time
        time_range = (1 * 60, 46 * 60) # from 1 minute to 46 minutes (in seconds)
        #time_range = (1 * 60, 2 * 60) # from 1 minutes to 2 minutes (in seconds) (debug)
        run_rng = random.randint(1, 100)
        if run_rng != 100:
            reset_time = ((time_range[1] - time_range[0]) * (run_rng / 100)) + time_range[0]
        else:
            reset_time = None
        reset_time = round(reset_time)
        print("Reset time set to", reset_time)

    reset_time = None
    setResetTime()
    start_time = datetime.now()

    print("Click into mupen64 now")

    time.sleep(3)

    print("Starting run and program...")

    mupen.start_tas(app_settings)
    
    ls.startTimer()
    
    if predict is not None:
        details = tapi.generatePrediction()
        tapi.createPrediction(details[0], details[1])
        predict_time = round(details[2])
        print("predict_time", predict_time)

print("Started!")

overrides = []

while True:
    options = ["!fun", "!story", "!joke", "!mario"]
    message = options[random.randint(0, len(options) - 1)]
    if random.random() < float(eval(app_settings.get("twitch_chance"))):
        message = "!twitch"
    
    subs = tapi.newSubscribers()
    
    if len(subs) > 0:
        for sub in subs:
            overrides.append("!sub " + sub)
            continue
    
    if do_mupen and reset_time is not None and \
        (datetime.now() - start_time).total_seconds() > reset_time:
        message = "!reset"
        print("Actually, RESET")
            
    if len(overrides) > 0:
        message = overrides.pop(0)
    
    #message = input("Input: ")
    
    print("Bot chose:", message)
    
    response = None
    reset = False
    
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
        response = chat.respond("Developer", message[6:], ai_bot, app_settings)
    elif message[:6] == "!test ":
        response = message[6:]
    elif message == "!twitch":
        twitchfile = open("latest.txt", "r")
        data = twitchfile.read().split(" ::: ")
        twitchfile.close()
        if len(data) == 2:
            profanity = float(predict_prob([data[1]]))
            if profanity > float(app_settings.get("profanity_max")):
                print("Profanity reject:", data[1])
                continue
            response = chat.respond(data[0], data[1], ai_bot, app_settings)
        else:
            print("Broken data from twitch file 'latest.txt'")
            continue
    elif do_mupen and message == "!reset":
        time.sleep(2)
        mupen.end_run()
        response = chat.direct("reset", ai_bot, app_settings)
        reset = True
    elif message[:5] == "!sub ":
        response = chat.sub(message[5:], ai_bot, app_settings)
    else:
        response = ai_bot.ask(message)
        
    if response is not None:
        filename = speech.text_to_wav("en-US-News-M", response, True)
        print("Response:", response, "(" + filename + ")")
    
    if do_mupen and reset:
        ls.reset()
        if predict is not None:
            win = predict_time <= (datetime.now() - start_time).total_seconds()
            tapi.endPrediction(0 if win else 1)
        mupen.start_tas(app_settings)
        ls.startTimer()
        setResetTime()
        start_time = datetime.now()
        if predict is not None:
            details = tapi.generatePrediction()
            tapi.createPrediction(details[0], details[1])
            predict_time = round(details[2])
            print("predict_time", predict_time)
        
    time.sleep(1)

speech.text_to_wav("en-US-News-M", "Goodbye!", True)

print("Goodbye!")

time.sleep(2)
