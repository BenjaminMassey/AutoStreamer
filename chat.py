
def respond(bot, username, message):
    base = "You are a Twitch streamer, responding to a chat message. Keep it to two sentences or less. The message reads: "
    response = bot.ask(base + message)
    return username + " said " + message + ". " + response

def fun(bot):
    message = "You are Twitch streamer, trying to kill time. Say something interesting and unique in two sentences or less."
    return bot.ask(message)

def story(bot):
    message = "You are a Twitch streamer, telling a story. Keep it to two sentences or less, and make it relatable."
    return bot.ask(message)
