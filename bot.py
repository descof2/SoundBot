import os
import discord
import time
from random import randint

client = discord.Client()
TOKEN = os.environ['BOT_TOKEN'] # Discord API token

@client.event  # startup
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# Function that will connect bot to channel, play sound effect and then disconnect once the effect is over
async def play_sound(message, file):
    voice = await message.author.voice.channel.connect()  # bot connects to voice channel ONLY IF the member who called the command is already in the channel
    voice.play(discord.FFmpegOpusAudio(source=f'sounds/{file}'))  # play sound effect
    # If you are running it locally replace the above line with voice.play(discord.FFmpegPCMAudio(executable="C://WhereYouSavedTheExe//ffmpeg.exe",source=file)) 

    while discord.VoiceClient.is_playing(voice):
        time.sleep(.1)

    await message.guild.voice_client.disconnect()  # disconnect bot once audio finishes playing


# Print all the sounds the bot can play
async def print_sounds(message):
    await message.channel.send("!wow - cute uwu anime wow\n"
                               "!jazz - you like jazz? :smirk:\n"
                               "!thot - IF SHE BREATHES SHES A THOOOT\n"
                               "!headshot - MY HANDS ARE SHAKING\n"
                               "!booey - bababooey :smirk:\n")

        
@client.event  # Bot responding to specific strings or commands from users
async def on_message(message):
    if message.author.bot: # Ensure that the bot is not responding to its own messages
        return

    userInput = message.content.split()
    
    if len(userInput) > 1: # Make sure not to check out of index 
        if userInput[0] == "!help" and userInput[1] == "sounds": # List all possible sounds bot can play
            await print_sounds(message)

    # Sound effect commands
    if userInput[0] == "!wow": 
        await play_sound(message, "wow.mp3")

    if userInput[0] == "!jazz": 
        await play_sound(message, "jazz.mp3")

    if userInput[0] == "!headshot": 
        await play_sound(message, "headshot.mp3")

    if userInput[0] == "!thot": 
        await play_sound(message, "thot.mp3")
    
    if userInput[0] == "!booey":
        await play_sound(message, "bababooey.mp3")
        
    if userInput[0] == "!hoes": 
        await play_sound(message, "hoesmad.mp3")
      
    if userInput[0] == "!sad": # Play Juice Wrld's Lucid Dreams clip
        if str(message.author) == "TheeAlbinoTree#7487": # Only allow Tom Mckernan the ability to use the sad command
            await play_sound(message, "juice.mp3")
        else:
            await message.channel.send("You are not sad enough to use this command :( ")
            
    if userInput[0] == "!bunger": # Select from a group of 8 bunger sound files
        bungerFileName = "bunger" + str(randint(1,8)) + ".mp3"
        await play_sound(message, bungerFileName)

    userInput = [] # Clean out the list after use
    
# end
client.run(TOKEN)
