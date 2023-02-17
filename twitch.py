from twitchio.ext import commands

class TwitchBot(commands.Bot):

    filename = ""

    def __init__(self, auth, channel, filename):
        super().__init__(
            token=auth,
            prefix='?',
            initial_channels=[channel]
        )
        self.filename = filename

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return
        
        user = str(message.author.name)
        msg = str(message.content)
        
        file = open(self.filename, "w")
        file.write(user + " ::: " + msg)
        file.close()
        
        print(user + " says '" + msg + "'.")
        
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')


twitch_data_file = open("./twitch_data.txt", "r")
auth = twitch_data_file.readline().replace("\n","").replace(" ", "")
channel = twitch_data_file.readline().replace("\n","").replace(" ", "")
twitch_data_file.close()

filename = "latest.txt"

bot = TwitchBot(auth, channel, filename)

print("Twitch Bot is set up!")

bot.run()