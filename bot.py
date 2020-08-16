import os
import discord
import time

TOKEN = os.environ['BOT_TOKEN']
client = discord.Client()


@client.event  # startup
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# Function that will connect bot to channel, play sound effect and then disconnect according to the sleep timer provided
async def play_sound(message, file, sleepTime):
    voice = await message.author.voice.channel.connect()  # bot connects to voice channel ONLY IF the member who called the command is already in the channel
    voice.play(discord.FFmpegOpusAudio(source=f'sounds/{file}'))  # play sound effect

    # if (message.guild.voice_client.is_playing() == False): #PLEASE GET THIS SHIT TO WORK #TODO - REMOVE THE NEED FOR A SLEEP TIMER
        # await.message.guild.voice_client.disconect()
    time.sleep(sleepTime)  # wait 5 seconds
    await message.guild.voice_client.disconnect()  # disconnect bot once audio finishes playing


# print all the commands the bot can do
async def print_commands(message):
    await message.channel.send("!help - list all usable commands \n"
                               "!help sounds - list all usable sounds \n"
                               "!jackboxtime - Move everyone to jackbox channel. Include names after the command to exclude moving those users [COMING SOON]\n"
                               "!generaltime - Move everyone from jackbox back to general")


# print all the sounds the bot can do
async def print_sounds(message):
    await message.channel.send("!wow - cute uwu anime wow\n"
                              "!jazz - you like jazz? :smirk:\n"
                              "!hello - :frowning:\n"
                              "!headshot - MY HANDS ARE SHAKING\n")


# Function that takes a list of members to move and their destination. Assumes that all members in the list are going to the same place
async def move_member(movingMembers, destination):
    for i in movingMembers:
        await i.edit(voice_channel=destination)


@client.event  # Bot responding to specific strings or commands from users
async def on_message(message):
    if message.content == "!hello":  # Basic printing
        await message.channel.send(str(message.author) + " why did she leave me...")

    if message.content == "!jackboxtime":  # TODO - REFACTOR THIS
        jackboxChannel = discord.utils.get(client.get_all_channels(), name='jackbox')  # return voice channel object
        generalChannel = discord.utils.get(client.get_all_channels(), name='General')  # return voice channel object

        currentMembers = []

        for member in generalChannel.members:
            currentMembers.append(member)

        await move_member(currentMembers, jackboxChannel)

    if message.content == "!generaltime":  # TODO - FIX THIS
        generalChannel = discord.utils.get(client.get_all_channels(), name='General')  # return voice channel object
        jackboxChannel = discord.utils.get(client.get_all_channels(), name='jackbox')  # return voice channel object

        currentMembers = []

        for member in jackboxChannel.members:
            currentMembers.append(member)

        await move_member(currentMembers, generalChannel)

    if message.content == "!help":  # List all possible commands the bot will respond to
        await print_commands(message)

    if message.content == "!help sounds":
        await print_sounds(message)

    # Sound effect commands
    if message.content == "!wow":  # play anime wow sound effect
        await play_sound(message, "wow.mp3", 2)

    if message.content == "!jazz":  # play jazz sound effect
        await play_sound(message, "jazz.mp3", 1)

    if message.content == "!headshot":  # play BOOM HEADSHOT effect
        await play_sound(message, "headshot.mp3", 9)

    if message.content == "!test":  # play BOOM HEADSHOT effect
        await play_sound(message, "this_is_where_mp3s_go.mp3", 9)

# end
client.run(TOKEN)
