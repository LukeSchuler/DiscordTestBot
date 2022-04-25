import discord
import asyncio
import json
import discord.ext
from discord.ext import commands
from discord.ext.commands import CommandNotFound

client = commands.Bot(command_prefix = '!')
client.cmdList = {}

@client.event
async def on_ready():
    print('Logged on as {0.user}!'.format(client))
    #Load command list
    with open("usrcmd.json", "r") as f:
        try:
            client.cmdList = json.load(f)
        except json.JSONDecodeError:
            pass

#Configure a new command from the chat input
@client.command(name='addcom')
async def addcom(ctx, arg1, arg2):
    input = [arg1, arg2]
    #Update with new entry
    client.cmdList[input[0]] = input[1]
    updateCmds()

    await ctx.send('Added command: {}, {}'.format(arg1, arg2))

#Delete existing command
@client.command(name='delcom')
async def delcom(ctx, arg1):
    if arg1.lower() in client.cmdList.keys():
        del client.cmdList[arg1]
        updateCmds()
    else:
        await ctx.send('Command not found')

#Updates command list file
def updateCmds():
    with open("usrcmd.json","w") as f:
        json.dump(client.cmdList,f)

#Command not found error handling--ignores error if "command" is user command dictionary item
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound ):
        if ctx.message.content in client.cmdList:
            pass
        else:
            await ctx.send("Invalid command!")
            return

#Standard on_message event checker
#TODO: Add functionality to tag users via %user% flag in command
@client.event
async def on_message(message):
    client.cmdList
    if message.author == client.user:
        return
    
    #Check against commandlist dictionary
    msgWords = message.content.lower().split(' ')
    for word in msgWords:
        if word in client.cmdList.keys():
            await message.channel.send(client.cmdList[word])
            break

    await client.process_commands(message)
    
client.run('')