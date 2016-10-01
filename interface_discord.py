#!/usr/bin/env python3.5
from config import discord_config
import discord, asyncio
import Event, User, EventUser

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
    if content.startswith('!hello'):
        await client.send_message(message.channel, 'Hello {}!'.format(message.author.mention))
    elif content.strip() == '!register':
        user_exists = User.get_user(message.author.id)
        if not user_exists:
            User.add_user(message.author.id)
            await client.send_message(message.channel, 'Registered user {} with id {}.'.format(message.author.display_name, message.author.id))
        else: # User already exists
            await client.send_message(message.channel, 'You have already registered!')
    # TODO parse input

client.run(discord_config.token)
