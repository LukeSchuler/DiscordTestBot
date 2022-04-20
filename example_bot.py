import discord
import asyncio
import json
import discord.ext
from discord.ext import commands
from discord.ext.commands import CommandNotFound

client = commands.Bot(command_prefix = '!')
cmdList = {}

@client.event
async def on_ready():
    print('Logged on as {0.user}!'.format(client))
    #Load command list
    with open("usrcmd.json", "r") as f:
        try:
            global cmdList
            cmdList = json.load(f)
        except json.JSONDecodeError:
            pass

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    
    #Check against commandlist dictionary
    msgWords = message.content.lower().split(' ')
    for word in msgWords:
        if word in cmdList.keys():
            await message.channel.send(cmdList[word])
            break

    await client.process_commands(message)

#Configure a new command from the chat input
@client.command(name='addcom')
async def addcom(ctx, arg1, arg2):
    input = [arg1, arg2]
    global cmdList
    #Create dictionary from file
    with open("usrcmd.json", "r") as f:
        try:
            cmdList = json.load(f)
        except json.JSONDecodeError:
            pass

    #Update with new entry
    cmdList[input[0]] = input[1]

    #Save new entry to file
    with open("usrcmd.json", "w") as f:
        json.dump(cmdList, f)

    await ctx.send('Added command: {}, {}'.format(arg1, arg2))

#Command not found error handling--ignores error if "command" is user command dictionary item
@client.event
async def on_command_error(ctx, error):
    global cmdList
    if isinstance(error, CommandNotFound ):
        if ctx.message.content in cmdList:
            pass
        else:
            await ctx.send("Invalid command!")
            return
    
client.run('')