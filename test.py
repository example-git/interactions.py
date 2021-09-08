# This is a written example used to test and debug the state of v4.0
import interactions

TOKEN = "ODgzNzg4ODkzNTEyNjgzNTIw.YTPCjA.n2feSiJeyxO_TspHRYyjdwd5pew"

client = interactions.Client(token=TOKEN)


@client.event
async def on_ready():
    print("Bot is online!")


@client.event
async def on_guild_create(guild):
    print(guild)


@client.event
async def on_message_create(message):
    print(message)


client.start()
