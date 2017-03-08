#!/usr/bin/env python3.5
"""
NB: Interface is currently broken - redesigning application structure
"""
import discord
import shlex
from config import discord_config
from Poorganiser import User, Event, Attendance
from PorgWrapper import PorgWrapper
from PorgExceptions import *


client = discord.Client()
porg = PorgWrapper()


def id_to_username(members, user_id):
    for member in members:
        if int(member.id) == int(user_id):
            return member.name + '#' + member.discriminator
    return None


def user_to_id(username):
    members = client.get_all_members()
    for member in members:
        if (member.name) == username:
            return int(member.id)


def generate_events_summary(event, members):
    attendee_names = []
    attendees = event.get_attendance_ids()
    for attendee_id in attendees:
        u = porg.db_interface.get_obj(attendee_id, User)
        attendee_names.append(id_to_username(members, u.get_username()))

    out = "**id**: {}\n".format(event.get_id()) + \
           "**name**: {}\n".format(event.get_name())

    if event.get_location():
        out += "**location**: {}\n".format(event.get_location())

    if event.get_time():
        "**time**: {}\n".format(event.get_time())

    out += "**attendees**: {}\n".format(attendee_names)
    return out


def short_event_info(event):
    return "{:<5}{}".format(event.get_id(), event.get_name())


def short_survey_info(survey):
    return "{:<5}{}".format(survey.get_id(), survey.get_name())


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    shlexed_message = shlex.split(message.content)
    command = shlexed_message[0].strip()

    if command == '!hello':
        await client.send_message(message.channel, 'Hello {}!'.format(message.author.mention))
    elif command == '!register':
        try:
            porg.register_user(message.author.id)
            await client.send_message(message.channel, 'Registered user {} with id {}.'.format(
                message.author.display_name, message.author.id))
        except UserRegisteredError:
            await client.send_message(message.channel, 'You have already registered!')
    elif command == '!unregister':
        try:
            porg.unregister_user(message.author.id)
            await client.send_message(message.channel, 'You have unregistered. Goodbye!')
        except UserNotFoundError:
            await client.send_message(message.channel, 'You have not registered yet!')
    elif command.startswith('!help'):
        await client.send_message(message.channel, porg.get_help())
    elif command == "!curr":
        events = porg.get_curr_events()
        if events:
            out = "**Current events**\n"
            for event in events:
                out += generate_events_summary(event, message.server.members) + '\n'
        else:
            out = "There are no current events!"
        await client.send_message(message.channel, out)
    elif command == '!my':
        status_message = ''

        user = porg.get_user_by_username(message.author.id)
        my_events = porg.get_events_by_user(user)
        my_surveys = porg.get_surveys(user)

        if not user:
            status_message = 'Not registered! Use !register'
        elif shlexed_message[1] == 'status':
            status_message = 'Registered user {} with id {}.\n'.format(message.author.display_name, message.author.id)
            status_message += 'You have {} events and {} surveys.\n'.format(len(my_events), len(my_surveys))
            status_message += 'Use !my events and !my surveys to view.'
        elif shlexed_message[1] == 'events':
            status_message = 'Displaying events for user {} with id {}.\n'.format(message.author.display_name, message.author.id)

            if my_events:
                status_message += "Your events:\n```"
                status_message += "{:<5}{}\n".format("ID", "NAME")

                for event in my_events:
                    if event:
                        event_details = short_event_info(event)
                        status_message += event_details + "\n"
                status_message += "```"
            else:
                status_message += 'You have no events!'
        elif shlexed_message == 'surveys':
            status_message = 'Displaying surveys for user {} with id {}.\n'.format(message.author.display_name, message.author.id)

            if my_surveys:
                status_message += "Your surveys:\n```"
                status_message += "{:<5}{}\n".format("ID", "NAME")

                for survey in my_surveys:
                    if survey:
                        survey_details = short_survey_info(survey)
                        status_message += survey_details + "\n"
            else:
                status_message += 'You have no surveys!'
        else:
            status_message += '**Available commands:**\n'
            status_message += '!my status\n'
            status_message += '!my events\n'
            status_message += '!my surveys'
        await client.send_message(message.channel, status_message)
    elif command == "!create":
        await client.delete_message(message)
        create_types = 'Select a type of object to create:\n' \
                       '-event\n' \
                       '-survey\n' \
                       '-question\n'

        def check_type(msg):
            return msg.content.strip() in ['event', 'survey', 'question']

        types_prompt = await client.send_message(message.channel, create_types)
        selected_type = await client.wait_for_message(author=message.author, check=check_type)

        await client.delete_message(types_prompt)

        if selected_type:
            await client.delete_message(selected_type)
            if selected_type.content == 'event':
                await client.send_message(message.channel, "Creating event...")
                event_name_prompt = await client.send_message(message.channel, "Event name:")
                event_name = await client.wait_for_message(author=message.author)
                await client.delete_message(event_name_prompt)
                await client.delete_message(event_name)

                u = porg.get_user_by_username(message.author.id)
                e = porg.create_event(event_name.content, u)

                await client.send_message(message.channel, generate_events_summary(e, message.server.members))
            elif selected_type.content == 'survey':
                await client.send_message(message.channel, "Creating survey...")
                survey_name_prompt = await client.send_message(message.channel, "Survey name:")
                survey_name = await client.wait_for_message(author=message.author)
                await client.delete_message(survey_name_prompt)
                await client.delete_message(survey_name)

                u = porg.get_user_by_username(message.author.id)
                s = porg.create_survey(survey_name.content, u)

                await client.send_message(message.channel, "Created survey {} with id {}".format(s.get_name(), s.get_id()))
            elif selected_type.content == 'question':
                await client.send_message(message.channel, "Creating question...")

client.run(discord_config.token)
