
def respond(bot, username, message):
    base = base("respond")
    response = bot.ask(base + message)
    return username + " said " + message + ". " + response

def fun(bot):
    message = base("fun")
    return bot.ask(message)

def story(bot):
    message = base("story")
    return bot.ask(message)
    
def base(key):
    result = ""
    file = open("bases.txt", "r")
    for line in file:
        data = line.split(" ::: ")
        if len(data) == 2 and data[0] == key:
            result = data[1]
    return result