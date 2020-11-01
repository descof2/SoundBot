import os
import discord
import time

client = discord.Client()
TOKEN = os.environ['BOT_TOKEN'] # Discord API token

@client.event  # startup
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# Function that will connect bot to channel, play sound effect and then disconnect according to the sleep timer provided
async def play_sound(message, file):
    voice = await message.author.voice.channel.connect()  # bot connects to voice channel ONLY IF the member who called the command is already in the channel
     voice.play(discord.FFmpegOpusAudio(source=f'sounds/{file}'))  # play sound effect

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
    if userInput[0] == "!wow":  # Play anime wow sound effect
        await play_sound(message, "wow.mp3")

    if userInput[0] == "!jazz":  # Play jazz sound effect
        await play_sound(message, "jazz.mp3")

    if userInput[0] == "!headshot":  # Play BOOM HEADSHOT effect
        await play_sound(message, "headshot.mp3")

    if userInput[0] == "!thot":  # Play thot sound effect
        await play_sound(message, "thot.mp3")
    
    if userInput[0] == "!booey": # play bababooey sound effect
        await play_sound(message, "bababooey.mp3")
        
    if userInput[0] == "!hoes": # play hoes mad sound effect
        await play_sound(message, "hoesmad.mp3")
      
    if userInput[0] == "!sad": # Play Juice Wrld's Lucid Dreams clip
        if str(message.author) == "TheeAlbinoTree#7487": # Only allow Tom Mckernan the ability to use the sad command
            await play_sound(message, "juice.mp3")
        else:
            await message.channel.send("You are not sad enough to use this command :( ")

    userInput = [] # Clean out the list after use
    
# end
client.run(TOKEN)
