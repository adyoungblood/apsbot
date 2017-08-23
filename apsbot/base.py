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
# some gun facts from louie
facts = ("The first ever self loading pistol ever made was the Borshardt C93 pistol made in 1893. Rejected by both America and Germany, the creator, Hugo Borshardt claimed his pistol was flawless. Eventually he was kicked off the team after mediocre sales and a new person worked on the C93's design, George Luger who eventually made the P08 Luger pistol off the C93's design.", "While the C93 Borshardt was the first self loading pistol, it was not the first successful one. The Mauser C96 was the first commercially successful pistol, made by two brothers and sponsored by Paul Mauser (who didn't really like the gun), the C96 was a 10 round semi automatic pistol which was reloading by stripper clips from the top of the gun, an off mechanic now for a pistol but simple enough for when it was made. It saw great commercial success with sales across the globe,in particular by the central powers of WW1 and even the Nazis. It's even recognizable in eyes of the uninformed public due to it being a basis of Han Solo's blaster in the Star Wars movies.", "The most common LMG of World War One was the French 1915 Chauchat and it was a particularly spectacular weapon. In fact it's highly regarded as the worst designed lmg ever made, some even saying its the worst designed gun ever. For one, it fired at a sluggish 230 rpm. For point of reference most revolvers shot at that speed, much less a suppressive fire machine gun. But probably the biggest problem was its magazines. Not only did they only have 20 bullets, a small number for lmgs, but they also had two big holes cut into the gun so the shooter could see how many bullets he had left. Well the effects of trench warfare really took its toll as dirt and mud would get in these holes, causing the gun to jam. But despite these glaring issues, due to cheap price of mass producing the weapons, it was an ideal weapon for countries, just not soldiers.")
