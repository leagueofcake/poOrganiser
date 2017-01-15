#!/usr/bin/env python3.5
import re
"""
NB: Interface is currently broken - redesigning application structure
"""
from Event import *
from User import *

events = {}

def help():
    print("Usage: event_name action arguments")
    print("Examples:")
    print("\tevent_name create location date")
    print("\tevent_name add user user_name")
    print("\tevent_name get location")
    print("\tevent_name edit location ")
    print("EXIT: enter nothing to exit")
    print("DEBUGGING COMMANDS:")
    print("\tprint: prints all events")

def debug_print():
    first = True
    for key in events:
        event = events[key]
        event.debug_print()
        if first:
            first = False
        else:
            print("*" * 20)

while True:
    userInput = input()
    if not userInput or userInput.lower() == "exit":
        print("Goodbye.")
        break
    elif userInput == "help" or userInput == "?":
        help()
        continue
    elif userInput == "print":
        debug_print()
        continue
    splits = userInput.split(' ')
    event_name = splits[0]
    if len(splits) == 1:
        print("Not enough arguments")
        continue
    cmd = splits[1].lower()
    if cmd == "create":
        found = False
        if event_name in events:
            print("Event already exists")
        else:
            if len(splits) != 6:
                print("Incorrect number of arguments, correct usage: event_name create location time")
            location = splits[2]
            year = splits[3]
            month = splits[4]
            day = splits[5]
            new_event = Event(event_name, location, time)
            events[event_name] = add_event(event_name, location, year, month, day)   #CHANGE ARGUMENTS FOR THIS LINE AND THE LINE ABOVE (put all into add event)
            print("New event %s created, at %s on %s/%s/%s" % (event_name, location, day, month, year))
    elif event_name in events:
        curr_event = events[event_name]
        if cmd == "add":
            new_type = splits[2].lower()
            if new_type == "user":
                user_name = splits[3]
                if not user_name:
                    print("Incorrect number of arguments, correct usage: event_name add type name")
                elif not curr_event.get_attendee(user_name):
                    curr_event.add_attendee(user_name)
                    print("Added new attendee %s to %s" % (user_name, event_name))
            else:
                print("Unknown type")
        elif cmd == "get":
            get_type = splits[2].lower()
            if get_type == "location":
                print(curr_event.get_location())
            elif get_type == "time":
                print(curr_event.get_time())
            else:
                print("Unknown type")
        elif cmd == "edit":
            set_type = splits[2].lower()
            edit_value = splits[3].lower()
            if not edit_value:
                print("Incorrect number of arguments, correct usage: event_name edit type value")
            else:
                if get_type == "location":
                    curr_event.set_location(edit_value)
                    print("%s's location updated to %s" % (event_name, edit_value))
                elif get_type == "time":
                    curr_event.set_time(edit_value)
                    print("%s's time updated to %s" % (event_name, edit_value))
                else:
                    print("Unknown type")
    else:
        print("Event not found")
