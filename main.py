# Again, this is all from cacobot, because I'm bad. Sorry.

# standard imports
import sys # for tracebaks in on_error.
import json # to load the config file.
import traceback # also used to print tracebacks. I'm a lazy ass.
import asyncio # because we're using the async branch of discord.py.
from random import choice # for choosing game ids

import discord # obvious.
# https://github.com/Rapptz/discord.py/tree/async

import apsbot # imports all plugins in the apsbot folder.

# A sample configs/config.json should be supplied.
with open('configs/config.json') as data:
    config = json.load(data)

# log in
client = discord.Client()

def aan(string):
    '''Returns "a" or "an" depending on a string's first letter.'''
    if string[0].lower() in 'aeiou':
        return 'an'
    else:
        return 'a'

@client.event
async def on_ready():
    ''' Executed when the bot successfully connects to Discord. '''
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# random game status
async def random_game():
    ''' Changes the game in the bot's status. '''
    await client.wait_until_ready()
    while True:
        name = choice(config['games'])
        game = discord.Game(name=name)
        await client.change_presence(game=game, afk=False)
        await asyncio.sleep(3600)

# poll yui balance thing
async def yui_balance():
	await client.wait_until_ready()
	await asyncio.sleep(1)
	await client.send_message(client.get_server('330801853455663107').get_channel('344859521157693440'), 'yui balance')
	
	msg = await client.wait_for_message(author=client.get_server('330801853455663107').get_member('280497242714931202'), channel=client.get_server('330801853455663107').get_channel('344859521157693440'))
	
	daily = []
	for word in msg.content.split():
		word = word.strip('**')
		word = word.replace(',', '')
		if word.isdigit():
			daily.append(word)

	with open('bronze_data', 'a+') as bronze_data:
		bronze_data.write("{}, ".format(daily[2]))
	
	await asyncio.sleep(3600)
	
# get mo' money
async def yui_daily():
	await client.wait_until_ready()
	await asyncio.sleep(5)
	await client.send_message(client.get_server('330801853455663107').get_channel('344859521157693440'), 'yui daily')
	await asyncio.sleep(2)
	await client.send_message(client.get_server('330801853455663107').get_channel('344859521157693440'), 'yui exchange')
	await asyncio.sleep(43201)
	

@client.event
async def on_message(message):
    '''
    Executed when the bot recieves a message.
    [message] is a discord.Message object, representing the sent message.
    '''
    cont = True

    # execute Precommands
    for func in apsbot.base.pres:
        cont = await apsbot.base.pres[func](client, message)
        if not cont:
            return

    if message.content.startswith(config['invoker']) and \
     message.author.id != client.user.id and \
     len(message.content) > 1:
        command = message.content.split()[0][len(apsbot.base.config['invoker']):].lower()
        # So basically if the message was ".Repeat Butt talker!!!" this
        # would be "repeat"
        if command in apsbot.base.functions:
            if message.channel.is_private or\
            message.channel.permissions_for(message.server.me).send_messages:
                await client.send_typing(message.channel)
                await apsbot.base.functions[command](client, message)
            else:
                print('\n===========\nThe bot cannot send messages to #{} in the server "{}"!\n===========\n\nThis message is only showing up because I *tried* to send a message but it didn\'t go through. This probably means the mod team has tried to disable this bot, but someone is still trying to use it!\n\nHere is the command in question:\n\n{}\n\nThis was sent by {}.\n\nIf this message shows up a lot, the bot might be disabled in that server. You should just make it leave if the mod team isn\'t going to just kick it!'.format(
                    message.channel.name,
                    message.server.name,
                    message.content,
                    message.author.name
                    )
                ) # pylint: disable=c0330

    for func in apsbot.base.posts:
        await apsbot.base.posts[func](client, message)

@client.event
async def on_error(*args):
    '''
    This event is basically a script-spanning `except` statement.
    '''
    # args[0] is the message that was recieved prior to the error. At least,
    # it should be. We check it first in case the cause of the error wasn't a
    # message.
    print('An error has been caught.')
    print(traceback.format_exc())
    await client.send_message(client.get_server('330801853455663107').get_member('283414992752082945'), traceback.format_exc())
    if len(args) > 1:
        print(args[0], args[1])
        if isinstance(args[1], discord.Message):
            if args[1].author.id != client.user.id:
                if args[1].channel.is_private:
                    print('This error was caused by a DM with {}.\n'.format(args[1].author))
                else:
                    print(
                        'This error was caused by a message.\nServer: {}. Channel: #{}.\n'.format(
                            args[1].server.name,
                            args[1].channel.name
                            )
                        )

                if sys.exc_info()[0].__name__ == 'Forbidden':
                    await client.send_message(
                        args[1].channel,
                        'You told me to do something that requires permissions I currently do not have. Ask an administrator to give me a proper role or something!')
                elif sys.exc_info()[0].__name__ == 'ClientOSError' or sys.exc_info()[0].__name__ == 'ClientResponseError' or sys.exc_info()[0].__name__ == 'HTTPException':
                    await client.send_message(
                        args[1].channel,
                        'Sorry, I am under heavy load right now! This is probably due to a poor internet connection. Please submit your command again later.'
                        )
                else:
                    await client.send_message(
                        args[1].channel,
                        '{}\n{}: You caused {} **{}** with your command.'.format(
                            choice(config['error_messages']),
                            args[1].author.name,
                            aan(sys.exc_info()[0].__name__),
                            sys.exc_info()[0].__name__)
                        )

client.loop.create_task(random_game())
client.loop.create_task(yui_balance())
client.loop.create_task(yui_daily())
#client.run(config['token'])
client.run('arghalexander3000@gmail.com', 'D@vid0614')

config.close()

with open('config.json', 'w') as outfile:
	json.dump(configtxt, outfile)
client.logout()
