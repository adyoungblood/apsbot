import json

# Just a note, this is from cacobot's base.py. I'm bad at Python, but need to clean up my code.

# This dictionary will be filled with key-function pairs. The key will be the
# invoker of the function, and the object will be the function to call.
functions = {}

# This decorator is placed on all functions we want to add to CacoBot. It
# automagically makes the function's name the invoker, and adds it to the
# functions dictionary.
def apsfunc(func):
    functions[func.__name__] = func
    return func

# These next dictionaries and decorators work the same way, but "precommand"
# holds functions that are automatically called *after* successfully
# determining if we have a command, but *before* actually moving on to the
# command, and *postcommand* holds commands that are automatically called *after*
# checking the message.

# Precommands are for things like making sure someone has proper permissions to
# send messages, or logging specific commands to a file or something.

# **WARNINGS**:
# PRECOMMANDS *MUST* RETURN TRUE TO CONTINUE TO THE MESSAGE.
# If you would like a precommand to not continue to the message, return false.
# BOTH PRECOMMANDS AND POSTCOMMANDS MUST BE ASYNC. Else you will
# cause a slew of NoneType error messages.

pres = {}

def prefunc(func):
    pres[func.__name__] = func
    return func

posts = {}

def postfunc(func):
    posts[func.__name__] = func
    return func

# This is a global reference to your configuration file.
with open('configs/config.json') as data:
    config = json.load(data)
