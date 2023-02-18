
def respond(bot, username, message, app_settings):
    response = bot.ask(app_settings.get("respond") + message)
    return username + " said " + message + ". " + response

def direct(key, bot, app_settings):
    return bot.ask(app_settings.get(key))