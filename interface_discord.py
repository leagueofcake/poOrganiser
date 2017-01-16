#!/usr/bin/env python3.5
"""
NB: Interface is currently broken - redesigning application structure
"""
import datetime
import discord
import shlex
from config import discord_config
from Poorganiser import User, Event, Attendance
from PorgWrapper import PorgWrapper
from PorgExceptions import *


client = discord.Client()
porg = PorgWrapper()


def idToUsername(members, userID):
    for member in members:
        if int(member.id) == int(userID):
            return member.name
    return None


def userToID(username):
    members = client.get_all_members()
    for member in members:
        if (member.name) == username:
            return int(member.id)


def shortEventInfo(event):
    return "[{}]\t{}\t{}\t{}".format(event.get_id(), event.get_name(), event.get_location(),
                                     event.get_time())


def fullEventInfo(event):
    fullInfo = ""
    eventID = event.get_id()
    event_name = event.get_name()
    fullInfo += "**Event [{}]:** {}\n".format(eventID, event_name)
    event_location = event.get_location()
    fullInfo += "**Location:** {}\n".format(event_location)
    event_time = event.get_time()
    fullInfo += "**Date:** {}\n".format(event_time)
    fullInfo += "**People:**\n"
    fullInfo += "*Name\t\tGoing\tResponsibilities*\n"
    attendances = porg.get_attendances(eventID)
    for at in attendances:
        username = idToUsername(client.get_all_members(), at.get_user_id())
        going_status = at.get_going_status()
        roles = at.get_roles()

        fullInfo += "{}\t\t{}\t{}\n".format(username, going_status, ' '.join(roles))
    return fullInfo

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
        try:
            porg.register_user(message.author.id)
            await client.send_message(message.channel, 'Registered user {} with id {}.'.format(
                message.author.display_name, message.author.id))
        except UserRegisteredError:
            await client.send_message(message.channel, 'You have already registered!')
    elif content.strip() == '!unregister':
        try:
            porg.unregister_user(message.author.id)
            await client.send_message(message.channel, 'You have unregistered. Goodbye!')
        except UserNotFoundError:
            await client.send_message(message.channel, 'You have not registerd yet!')

    elif content.startswith('!help'):
        await client.send_message(message.channel, porg.get_help())
    elif content.strip() == "!curr":
        events = porg.get_curr_events()
        out = "ID\tNAME\tLOCATION\tDATE\n"
        for event in events:
            out += shortEventInfo(event) + '\n'
        await client.send_message(message.channel, out)
    elif content.strip() == "!past":
        await client.send_message(message.channel, 'Not implemented yet!')
    elif content.strip() == "!allevents":
        events = porg.get_all_events()
        out = "ID\tNAME\tLOCATION\tDATE\n"
        for event in events:
            if event:
                out += shortEventInfo(event) + '\n'
        await client.send_message(message.channel, 'All Events:\n{}'.format(out))
    elif content.strip() == "!mystatus":
        user = porg.get_user_by_username(message.author.id)
        if not user:
            status_message = 'Not registered! Use !register'
        else:
            status_message = 'Registered user {} with id {}.\n'.format(message.author.display_name, message.author.id)
            status_message += "Your events:\n"
            user_events = porg.get_events_by_user(user.get_id())
            status_message += "ID\tNAME\tLOCATION\tDATE\tGOING\tRESPONSIBILITIES\n"
            for event in user_events:
                if event:
                    event_details = shortEventInfo(event)
                    at = porg.get_attendance(event.get_id(), user.get_id())
                    event_details += "\t{}\t{}".format(at.get_going_status(), at.get_roles())
                    status_message += event_details + "\n"

        await client.send_message(message.channel, status_message)

    else: #multi argument commands
        splits = shlex.split(content)
        admin_commands = ["!create", "!edit", "!delete", "!add", "!remove"]
        cmd = splits[0]
        if cmd == "!going" or cmd == "!notgoing":
            if len(splits) != 2:
                await client.send_message(message.channel, 'Incorrect number of arguments. Correct usage: !going <eventid>')
            else:
                if porg.get_event(splits[1]):
                    eu = porg.get_eventuser(splits[1], message.author.id)
                    eu.set_isgoing(cmd[1:])
                    porg.update(eu)
                    await client.send_message(message.channel, "You are now marked as {} to event {}".format(cmd[1:], splits[1]))
                else:
                    await client.send_message(message.channel, 'Event not found')
        elif cmd == "!vote":
            if len(splits) < 2:
                await client.send_message(message.channel, 'Usage: !vote <choieid>')
            else:
                userid = message.author.id
                choiceid = splits[1]
                res = porg.vote(userid, choiceid)
                if res == None:
                    await client.send_message(message.channel, 'You\'ve already voted for this choice!')
                else:
                    await client.send_message(message.channel, 'Successfully voted for choice (id: {})!'.format(choiceid))
        elif cmd == "!ans":
            if len(splits) != 2:
                await client.send_message(message.channel, 'Incorrect number of arguments. Correct usage: !ans <questionID>')
            else:
                questionid = splits[1]
                result = porg.get_result(questionid)
                if result:
                    await client.send_message(message.channel, 'Result: {}: {}'.format(result.get_id(), result.get_choicetext()))
                else:
                    await client.send_message(message.channel, 'No result found')
        elif cmd == "!event":
            if len(splits) != 2:
                await client.send_message(message.channel, 'Incorrect number of arguments. Correct usage: !event <eventid>')
            else:
                event = porg.get_event(splits[1])
                if not event:
                    await client.send_message(message.channel, 'Event not found')
                else:
                    await client.send_message(message.channel, fullEventInfo(event))
        elif cmd == "!question":
            if len(splits) <= 1:
                await client.send_message(message.channel, 'Incorrect number of arguments. Correct usage: !question <question id>')
            elif not splits[1].isdigit(): # Not a number!
                await client.send_message(message.channel, 'Incorrect question id type. Please specify a number.')
            else:
                out = ''
                eventid = int(splits[1])
                question = porg.get_question(eventid)
                choices = porg.get_questionchoices(question.get_questionid())
                for choice in choices:
                    out += '\t[{}]\t{}\n'.format(choice.get_id(), choice.get_choicetext())
                await client.send_message(message.channel, 'Question: {}\nChoices:\n{}'.format(question.get_text(), out))
        elif cmd == "!survey": # Get all questions associated with event
            if len(splits) <= 1:
                await client.send_message(message.channel, 'Incorrect number of arguments. Correct usage: !survey <eventid>')
            elif not splits[1].isdigit(): # Not a number!
                await client.send_message(message.channel, 'Incorrect event id type. Please specify a number.')
            else:
                out = ''
                eventid = int(splits[1])
                questions = porg.get_questions(eventid)
                for question in questions:
                    out += '{} {}\n'.format(question.get_questionid(), question.get_text())
                    choices = porg.get_questionchoices(question.get_questionid())
                    for choice in choices:
                        out += '\t{} {}\n'.format(choice.get_id(), choice.get_choicetext())
                await client.send_message(message.channel, 'Questions:\n{}'.format(out))
        elif cmd in admin_commands:
            userID = message.author.id
            if True: #TODO IF IS ADMIN
                if cmd == "!create":
                    if len(splits) <= 2 or len(splits) > 7:
                        await client.send_message(message.channel, 'Incorrect number of arguments. Correct usage: !create event <name> OPTIONAL: <location> <year> <month> <day>')
                    elif splits[1] != "event":
                        await client.send_message(message.channel, 'Unknown creation type')
                    else:
                        event_name = splits[2]
                        location = "Undecided"
                        year, month, day = None, None, None
                        try:
                            location = splits[3]
                            year = int(splits[4])
                            month = int(splits[5])
                            day = int(splits[6])
                            time = datetime.datetime(year, month, day)
                        except IndexError:
                            year, month, day = None, None, None #if error occured somewhere above, set date back to none

                        u = porg.get_user_by_username(userID)
                        new_event = porg.create_event(u.get_id(), event_name, location, time)
                        event_id = new_event.get_id()
                        await client.send_message(message.channel, 'New event {}, with ID {} created'.format(event_name, event_id))
                        members = message.server.members
                        for member in members:
                            user = porg.get_user_by_username(member.id)
                            if user: #only invite registered users
                                porg.create_attendance(user.get_id(), event_id, going_status="invited")
                        await client.send_message(message.channel, 'All members of channel invited. See !mystatus to check')
                elif cmd == "!edit":
                    if len(splits) < 4:
                        await client.send_message(message.channel, 'Incorrect number of arguments. Correct usage: !edit <eventID> <field> <new_value>')
                    else:
                        eventID = splits[1]
                        edit_event = porg.get_event(eventID)
                        if not edit_event:
                            await client.send_message(message.channel, 'Event not found')
                        elif edit_event.get_ownerid() != int(userID):
                            await client.send_message(message.channel, 'You do not have permission to modify this event')
                        else:
                            edit_field = splits[2].lower()
                            if edit_field == "name":
                                edit_event.set_name(splits[3])
                                porg.update(edit_event)
                                await client.send_message(message.channel, 'Event {}\'s name updated to {}'.format(eventID, splits[3]))
                            elif edit_field == "location":
                                edit_event.set_location(splits[3])
                                porg.update(edit_event)
                                await client.send_message(message.channel, 'Event {}\'s location updated to {}'.format(eventID, splits[3]))
                            elif edit_field == "date":
                                if not len(splits) == 6:
                                    await client.send_message(message.channel, 'Invalid date format. Use <year> <month> <day>')
                                else:
                                    date = datetime.date(int(splits[3]), int(splits[4]), int(splits[5]))
                                    edit_event.set_time(date)
                                    porg.update(edit_event)
                                    await client.send_message(message.channel, 'Event {}\'s date updated to {}'.format(eventID, date))
                            else:
                                await client.send_message(message.channel, 'Invalid field type')
                elif cmd == "!delete":
                    #TODO add confirmation for deletion
                    if len(splits) != 2:
                        await client.send_message(message.channel, 'Incorrect number of arguments. Correct usage: !delete <eventID>')
                    else:
                        eventid = splits[1]
                        res = porg.remove_event(eventid)
                        if res:
                            # Remove associated event users
                            eventusers = porg.get_eventusers(eventid)
                            for eventuser in eventusers:
                                porg.remove_eventuser(eventid, eventuser.get_eventuserid())
                            await client.send_message(message.channel, 'Event {} was removed'.format(splits[1]))
                        else:
                            await client.send_message(message.channel, 'Remove failed, double check your event ID')
                elif cmd == "!add":
                    # Question, choices, roles
                    cmd_type = '<question|choice|role>'
                    if len(splits) >= 2:
                        if splits[1] in ['question', 'choice', 'role']:
                            cmd_type = splits[1]
                            msg = 'Incorrect number of arguments. Correct usage: !add {} '.format(cmd_type)
                            if cmd_type == 'question':
                                msg += '<event id> <question text>'
                            elif cmd_type == 'choice':
                                msg += '<question id> <choice text>'
                            elif cmd_type == 'role':
                                msg += '<event id> <username> <role text>'

                            if len(splits) < 4:
                                await client.send_message(message.channel, 'Incorrect number of arguments. Correct usage: !add {} {}'.format(cmd_type, msg))
                            else:
                                if cmd_type == 'question':
                                    if len(splits) >= 3:
                                        eventid = splits[2]
                                        text = splits[3]
                                        yettovote = porg.get_eventusers(int(eventid))
                                        q = porg.add_question(eventid, text, yettovote)
                                        await client.send_message(message.channel, 'Added question with id {}'.format(q.get_questionid()))
                                elif cmd_type == 'choice':
                                    if len(splits) >= 3:
                                        questionid = splits[2]
                                        choicetext = splits[3]
                                        c = porg.add_questionchoice(questionid, choicetext)
                                        await client.send_message(message.channel, 'Added choice `{}` with id {}'.format(c.get_choicetext(), c.get_id()))
                                elif cmd_type == 'role':
                                    if len(splits) >= 4:
                                        eventid = splits[2]
                                        userid = userToID(splits[3])
                                        #userid = splits[3]
                                        roletext = splits[4]
                                        eu = porg.get_eventuser(eventid, userid)
                                        eu.add_role(roletext)
                                        eu.roles = str(eu.roles)
                                        porg.update(eu)
                                        await client.send_message(message.channel, 'Added role `{}` to user {} for event {}'.format(roletext, userid, eventid))
                        elif len(splits) < 4:
                            await client.send_message(message.channel, 'Correct usage: !add {} <command text>'.format(cmd_type))
                elif cmd == "!remove":
                    await client.send_message(message.channel, 'emented yet!')
            else:
                await client.send_message(message.channel, 'You do not have permission to do that')


client.run(discord_config.token)
