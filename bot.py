import os
import discord
import time
from googleapiclient.discovery import build

client = discord.Client()
TOKEN = os.environ['BOT_TOKEN']
YT_TOKEN = os.environ['YT_TOKEN']

@client.event  # startup
async def on_ready():
    print(f'{client.user} has connected to Discord!')


# Function that will take in a youtube channel's ID and randomly print one of their video's URL into channel
# Currently this function only randomly picks from the channel's latest 50 videos. If a channel has thousands 
# of videos, this would lead to a lot of API calls. 
# TODO - Get latest 150~ videos -> 3 api calls 
async def print_random_video(message, channelID):
    youtube = build('youtube', 'v3', developerKey=YT_TOKEN)  # Create youtube object
    request = youtube.channels().list(part='contentDetails', id=channelID)
    response = request.execute()

    playlistID = response['items'][0]['contentDetails']['relatedPlaylists']['uploads'] # All uploads are stored in a single playlist 

    request = youtube.playlistItems().list(part="contentDetails", playlistId=playlistID, maxResults=50)
    response = request.execute()

    uploadList = []  # Hold every uploadID within the upload playlist

    for i in response['items']: # Adding every uploadID to list 
        if i['kind'] == "youtube#playlistItem":
            uploadList.append(i['contentDetails']['videoId']) 

    totalUploads = response['pageInfo']['totalResults'] # Total public uploads on the youtube channel

    await message.channel.send("This channel has " + str(totalUploads) + " uploads. Here's one: \n" "https://www.youtube.com/watch?v=" + random.choice(uploadList))

    
    
# Function that will connect bot to channel, play sound effect and then disconnect according to the sleep timer provided
async def play_sound(message, file, sleepTime):
    voice = await message.author.voice.channel.connect()  # bot connects to voice channel ONLY IF the member who called the command is already in the channel
    voice.play(discord.FFmpegOpusAudio(source=f'sounds/{file}'))  # play sound effect

    # if (message.guild.voice_client.is_playing() == False): #PLEASE GET THIS SHIT TO WORK #TODO - REMOVE THE NEED FOR A SLEEP TIMER
    # await.message.guild.voice_client.disconect()
    time.sleep(sleepTime)  # wait 5 seconds
    await message.guild.voice_client.disconnect()  # disconnect bot once audio finishes playing


# Print all the commands the bot can do
async def print_commands(message):
    await message.channel.send("!help - list all usable commands \n"
                               "!hello - :frowning:\n"
                               "!help sounds - list all usable sounds \n"
                               "!jackboxtime - Move everyone to jackbox channel. Include names after the command to exclude moving those users [COMING SOON]\n"
                               "!generaltime - Move everyone from jackbox back to general\n"
                               "!poll [Question] - Creates a poll for users to vote on")


# Print all the sounds the bot can play
async def print_sounds(message):
    await message.channel.send("!wow - cute uwu anime wow\n"
                               "!jazz - you like jazz? :smirk:\n"
                               "!thot - IF SHE BREATHES SHES A THOOOT\n"
                               "!headshot - MY HANDS ARE SHAKING\n")


# Function that takes a list of members to move and their destination. Assumes that all members in the list are going to the same place
async def move_member(movingMembers, destination):
    for i in movingMembers:
        await i.edit(voice_channel=destination)
        
        
# Function that takes user's message along with associated message object and prints poll question along with a thumbs up and thumbs down reaction	
# allowing users to vote	
async def create_poll(userInput, message):	
    pollText = ""	
    for i in range(1, len(userInput)):	
        pollText += userInput[i] + " "	
        
    pollMessage = await message.channel.send(pollText)	# Bot prints poll question 
    await pollMessage.add_reaction(emoji='👍')	# And then adds reactions to that new poll question 
    await pollMessage.add_reaction(emoji='👎')	

        
@client.event  # Bot responding to specific strings or commands from users
async def on_message(message):
    if message.author.bot: # Ensure that the bot is not responding to its own messages
        return

    userInput = message.content.split()
    
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

    if userInput[0] == "!generaltime":  # TODO - REFACTOR THIS 
        generalChannel = discord.utils.get(client.get_all_channels(), name='General')  # return voice channel object
        jackboxChannel = discord.utils.get(client.get_all_channels(), name='jackbox')  # return voice channel object

        currentMembers = []

        for member in jackboxChannel.members:  # Get all current members connected to the channel
            currentMembers.append(member)

        await move_member(currentMembers, generalChannel)

    if len(userInput) > 1: # Make sure not to check out of index 
        if userInput[0] == "!help" and userInput[1] == "sounds": # List all possible sounds bot can play
            await print_sounds(message)

    elif userInput[0] == "!help":  # List all possible commands bot will respond to
        await print_commands(message)
        
    # Sound effect commands
    if userInput[0] == "!wow":  # Play anime wow sound effect
        await play_sound(message, "wow.mp3", 2)

    if userInput[0] == "!jazz":  # Play jazz sound effect
        await play_sound(message, "jazz.mp3", 1)

    if userInput[0] == "!headshot":  # Play BOOM HEADSHOT effect
        await play_sound(message, "headshot.mp3", 9)

    if userInput[0] == "!thot":  # Play thot sound effect
        await play_sound(message, "thot.mp3", 5)

    if userInput[0] == "!poll": # Create a poll with thumbs up/down reactions
       await create_poll(userInput, message)
    
    if userInput[0] == "!stop": # Force disconnect bot from voice
        await message.guild.voice_client.disconnect()  
        
    if userInput[0] == "!joey": # Post random JoeysWorldTour video
        joeysID = "UCC9uqoIkY8Nd7J9Gnk98W1w"
        await print_random_video(message, joeysID)

    if userInput[0] == "!chugs": # Post random BadlandsChugs video
        chugsID = "UCIvMEZips_QKqajfXGY_C5Q"
        await print_random_video(message, chugsID)

    userInput = [] # Clean out the list after use
    
# end
client.run(TOKEN)
