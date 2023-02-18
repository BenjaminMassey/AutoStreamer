
def respond(bot, username, message, app_settings):
    response = bot.ask(app_settings.get("respond") + message)
    return username + " said " + message + ". " + response

def fun(bot, app_settings):
    return bot.ask(app_settings.get("fun"))

def story(bot, app_settings):
    return bot.ask(app_settings.get("story"))

def reset(bot, app_settings):
    return bot.ask(app_settings.get("reset"))