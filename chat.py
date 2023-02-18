
def respond(bot, username, message):
    response = bot.ask(base("respond") + message)
    return username + " said " + message + ". " + response

def fun(bot):
    return bot.ask(base("fun"))

def story(bot):
    return bot.ask(base("story"))

def reset(bot):
    return bot.ask(base("reset"))
    
def base(key):
    result = ""
    file = open("bases.txt", "r")
    for line in file:
        data = line.split(" ::: ")
        if len(data) == 2 and data[0] == key:
            result = data[1]
    return result