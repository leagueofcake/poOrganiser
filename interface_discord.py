#!/usr/bin/env python3.5
import discord, asyncio
import discord_config

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    content = message.content
    # TODO parse input

client.run(discord_config.token)
