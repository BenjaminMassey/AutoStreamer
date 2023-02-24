
def respond(username, message, bot, app_settings):
    response = bot.ask(app_settings.get("respond") + message)
    return username + " said " + message + ". " + response

def sub(username, bot, app_settings):
    return bot.ask(app_settings.get("sub") + username)

def direct(key, bot, app_settings):
    return bot.ask(app_settings.get(key))