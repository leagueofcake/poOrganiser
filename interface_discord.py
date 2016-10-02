#!/usr/bin/env python3.5
from config import discord_config
import discord, asyncio
from Poorganiser import Poorganiser
import shlex, datetime

client = discord.Client()
porg = Poorganiser()

def idToUsername(members, userID):
    for member in members:
        if int(member.id) == int(userID):
            return member.name
    return None

def shortEventInfo(event):
    eventID = event.get_id()
    event_name = event.get_name()
    event_location = event.get_location()
    event_time = event.get_time()
    return ("{}\t{}\t{}\t{}".format(eventID, event_name, event_location, event_time))


def fullEventInfo(event):
    fullInfo = ""
    eventID = event.get_id()
    event_name = event.get_name()
    fullInfo += "**Event** {}: {}\n".format(eventID, event_name)
    event_location = event.get_location()
    fullInfo += "**Location:** {}\n".format(event_location)
    event_time = event.get_time()
    fullInfo += "**Date:** {}\n".format(event_time)
    fullInfo += "**People:**\n"
    fullInfo += "*Name\tGoing\tResponsibilities*\n"
    eus = porg.get_eventusers(eventID)
    for eu in eus:
        eu_name = idToUsername(eu.get_userid)
        eu_going = eu.get_isgoing()
        eu_roles = eu.get_roles()
        fullInfo += "{}\t{}\t{}\n".format(eu_name, eu_going, ' '.join(eu_roles))
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
        user_exists = porg.get_user(message.author.id)
        if not user_exists:
            porg.add_user(message.author.id)
            await client.send_message(message.channel, 'Registered user {} with id {}.'.format(message.author.display_name, message.author.id))
        else: # User already exists
            await client.send_message(message.channel, 'You have already registered!')
    elif content.strip() == '!unregister':
        user_exists = porg.get_user(message.author.id)
        if not user_exists:
            await client.send_message(message.channel, 'User not registered')
        else:
            porg.remove_user(message.author.id)
            await client.send_message(message.channel, 'User removed. Goodbye!')
    elif content.startswith('!help'):
        helpOutput = ""
        helpOutput += "         ヽ༼ຈل͜ຈ༽ﾉ Welcome to the Discord 'Poor Organizer' poOrganiser bot! ヽ༼ຈل͜ຈ༽ﾉ\n\n"
        helpOutput += "                            (>´･ω･`)> Yeeeeeeeboizzz <(´･ω･`<)\n\n"
        helpOutput += "（ ° ʖ °)つ━☆・\*。\n"
        helpOutput += " ⊂　　 ノ 　　　・゜+.\n"
        helpOutput += "　しーＪ　　　°。+ ´¨)\n"
        helpOutput += "　　　　　　　　　.· ´¸.·\*´¨) ¸.·\*¨)\n"
        helpOutput += "　　　　　　　　　　(¸.·´ (¸.·' ☆ User commands...\n"
        helpOutput += "!register = Registers the user in the database.\n"
        helpOutput += "!curr = View a list of all current events.\n"
        helpOutput += "!past = View a list of all past events.\n"
        helpOutput += "!paster = View a list of all past event\n"
        helpOutput += "!mystatus = Brings up your current role for all events.\n"
        helpOutput += "!survey <event ID> = Brings up a list of questions associated with event <ID>\n"
        helpOutput += "!event <event ID> = View details for the associated event.\n"
        helpOutput += "!question <question ID> <event ID> = View question text and options for the event<ID>\n"
        helpOutput += "!vote <question ID> <option ID> = Votes the selected option for the selected question.\n"
        helpOutput += "!results <question ID> <event ID> = View results for the associated question in the event.\n"
        helpOutput += "\n"
        helpOutput += "（ ° ʖ °)つ━☆・\*。\n"
        helpOutput += " ⊂　　 ノ 　　　・゜+.\n"
        helpOutput += "　しーＪ　　　°。+ ´¨)\n"
        helpOutput += "　　　　　　　　　.· ´¸.·\*´¨) ¸.·\*¨)\n"
        helpOutput += "　　　　　　　　　　(¸.·´ (¸.·' ☆ Admin commands...\n"
        helpOutput += "!create event '<name>, <place>, <time>' = Creates an event with the given details.\n"
        helpOutput += "!edit event <ID> '<name>, <place>, <time>' = Edits an event with the given details.\n"
        helpOutput += "!delete event <ID> = Deletes the event.\n"
        helpOutput += "!add role <user ID> <role> = Assigns the user with given role.\n"
        helpOutput += "!remove role <user ID> <role> = Removes the given role from the user.\n"
        helpOutput += "!add question <event ID> '<Insert here>' = Adds a question to the list of questions.\n"
        helpOutput += "!remove question <event ID> <question ID> = Removes the associated question from the event.\n\n"
        helpOutput += "NOTE: When typing commands, ignore the <>. E.g. !event 69, NOT !event <69>\n\n"

        await client.send_message(message.channel, helpOutput)
    elif content.strip() == "!curr":
        events = porg.get_curr_events()
        out = ''
        for event in events:
            out += shortEventInfo(event) + '\n'
        await client.send_message(message.channel, 'Current events:\n{}'.format(out))
    elif content.strip() == "!past":
        await client.send_message(message.channel, 'Not implemented yet!')
    elif content.strip() == "!pastall":
        await client.send_message(message.channel, 'Not implemented yet!')
    elif content.strip() == "!mystatus":
        user = porg.get_user(message.author.id)
        status_message = ""
        if not user:
            status_message += 'Not registered! Use !register'
        else:
            status_message += 'Registered user {} with id {}.\n'.format(message.author.display_name, message.author.id)
            #status_message += 'Test: ID to username = {}\n'.format(idToUsername(message.server.members, message.author.id))
            status_message += "Your events:\n"
            user_events = porg.get_events_by_user(message.author.id)
            status_message += "ID\tNAME\tLOCATION\tDATE\tGOING\tRESPONSIBILITIES\n"
            for event in user_events:
                if event:
                    event_details = shortEventInfo(event)
                    eu = porg.get_eventuser(event.get_id(), message.author.id)
                    event_details += "\t{}\t{}".format(eu.get_isgoing(), '/'.join(eu.get_roles()))
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
            await client.send_message(message.channel, 'Not implemented yet!')
        elif cmd == "!ans":
            await client.send_message(message.channel, 'Not implemented yet!')
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
                    out += '\t{}\n'.format(choice.get_choicetext())
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
                    out += question.get_text() + '\n'
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
                        except IndexError:
                            year, month, day = None, None, None #if error occured somewhere above, set date back to none
                        new_event = porg.add_event(userID, event_name, location, year, month, day)
                        newID = new_event.get_id()
                        porg.update(new_event)
                        await client.send_message(message.channel, 'New event {}, with ID {} created'.format(event_name, newID))
                        members = message.server.members
                        for member in members:
                            if porg.get_user(member.id): #only invite registered users
                                eu = porg.add_eventuser(newID, member.id, "Invited")
                                porg.update(eu)
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
                #    await client.send_message(message.channel, 'Not implemented yet!')
                    if len(splits) != 2:
                        await client.send_message(message.channel, 'Incorrect number of arguments. Correct usage: !delete <eventID>')
                    else:
                        if porg.remove_event(splits[1]):
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
                                msg += '<user id> <role text>'

                            if len(splits) < 4:
                                await client.send_message(message.channel, 'Incorrect number of arguments. Correct usage: !add {} {}'.format(cmd_type, msg))
                            else:
                                if cmd_type == 'question':
                                    eventid = splits[2]
                                    text = splits[3]
                                    yettovote = porg.get_eventusers(int(eventid))
                                    q = porg.add_question(eventid, text, yettovote)
                                    await client.send_message(message.channel, 'Added question with id {}'.format(q.get_questionid()))
                                elif cmd_type == 'choice':
                                    questionid = splits[2]
                                    choicetext = splits[3]
                        elif len(splits) < 4:
                            await client.send_message(message.channel, 'Correct usage: !add {} <command text>'.format(cmd_type))
                elif cmd == "!remove":
                    await client.send_message(message.channel, 'Not implemented yet!')
            else:
                await client.send_message(message.channel, 'You do not have permission to do that')


client.run(discord_config.token)
