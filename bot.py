import os
import discord
import time

client = discord.Client()
TOKEN = os.environ['BOT_TOKEN']

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
                               "!hello - :frowning:\n"
                               "!help sounds - list all usable sounds \n"
                               "!jackboxtime - Move everyone to jackbox channel. Include names after the command to exclude moving those users [COMING SOON]\n"
                               "!generaltime - Move everyone from jackbox back to general")


# print all the sounds the bot can do
async def print_sounds(message):
    await message.channel.send("!wow - cute uwu anime wow\n"
                               "!jazz - you like jazz? :smirk:\n"
                               "!thot - IF SHE BREATHES SHES A THOOOT\n"
                               "!headshot - MY HANDS ARE SHAKING\n"
                               "!thot - IF SHE BREATHES SHES A THOOOT\n")


# Function that takes a list of members to move and their destination. Assumes that all members in the list are going to the same place
async def move_member(movingMembers, destination):
    for i in movingMembers:
        await i.edit(voice_channel=destination)

        
@client.event  # Bot responding to specific strings or commands from users
async def on_message(message):
    if message.author.bot:
        return

    userInput = message.content.split()

    print(userInput)
    if userInput[0] == "!hello":  # Basic printing
        await message.channel.send(str(message.author) + " why did she leave me...")

    if userInput[0] == "!jackboxtime":  # TODO - REFACTOR THIS
        jackboxChannel = discord.utils.get(client.get_all_channels(), name='jackbox')  # return voice channel object
        generalChannel = discord.utils.get(client.get_all_channels(), name='General')  # return voice channel object

        currentMembers = []

        for member in generalChannel.members:  # Get all current members connected to the channel
            currentMembers.append(member)

        #for i in range(1, len(userInput)): #TODO
         #   if closeEnough(userInput[i], currentMembers[i]):
          #      currentMembers.remove(i)

        await move_member(currentMembers, jackboxChannel)

    if userInput[0] == "!generaltime":  # TODO - FIX THIS
        generalChannel = discord.utils.get(client.get_all_channels(), name='General')  # return voice channel object
        jackboxChannel = discord.utils.get(client.get_all_channels(), name='jackbox')  # return voice channel object

        currentMembers = []
        currentMembers = []

        for member in jackboxChannel.members:  # Get all current members connected to the channel
            currentMembers.append(member)

        await move_member(currentMembers, generalChannel)

    if userInput[0] == "!help":  # List all possible commands the bot will respond to
        await print_commands(message)

    if userInput[0] == "!help" and userInput[1] == "sounds":
        await print_sounds(message)

    # Sound effect commands
    if userInput[0] == "!wow":  # play anime wow sound effect
        await play_sound(message, "wow.mp3", 2)

    if userInput[0] == "!jazz":  # play jazz sound effect
        await play_sound(message, "jazz.mp3", 1)

    if userInput[0] == "!headshot":  # play BOOM HEADSHOT effect
        await play_sound(message, "headshot.mp3", 9)

    if userInput[0] == "!thot":  # play thot sound effect
        await play_sound(message, "thot.mp3", 5)

    if userInput[0] == "!poll":
        pollQuestion = ""
        for i in range(1, len(userInput)):
            pollQuestion += userInput[i]

        await message.channel.send(pollQuestion)
        await message.add_reaction(emoji='👍')

    if userInput[0] == "!stop":
        await message.guild.voice_client.disconnect()  # disconnect bot


# end
client.run(TOKEN)
