# -*- coding: utf8 -*-

#import apsbot
import discord
from discord.utils import find
import asyncio
from datetime import datetime
import json
import math
from random import choice
import sys
import os
import traceback
import re
import enchant

d = enchant.Dict("en_US")

client = discord.Client()

config = open('config.json', 'r')
configtxt = json.load(config)

undertale_server = None
apsbot = None

shushed = ''
games = ('mr carrot sim 2017', 'making spaghetti', 'dunking sim 2017', 'reading brit book')

async def random_game():
	while True:
		game = discord.Game(name=choice(games))
		await client.change_presence(game=game)
		await asyncio.sleep(3600)

def check_vote(string):
	string = string.split()
	for word in string:
		if re.fullmatch('aye*?', word):
			return(True)
		elif re.fullmatch('nae*?', word):
			return(False)
		else:
			return(None)

def aan(string):
    '''Returns "a" or "an" depending on a string's first letter.'''
    if string[0].lower() in 'aeiou':
        return 'an'
    else:
        return 'a'

@client.event
async def on_ready():
	global undertale_server, apsbot
	undertale_server = client.get_server(id='330801853455663107')
	apsbot = undertale_server.get_member(client.user.id)
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('--------')
	await random_game()
	#await client.send_message(client.get_channel('344859521157693440'), 'Ready for action!')

@client.event
async def on_message(message):
	global undertale_server, apsbot, shushed
	if message.author != apsbot:
		if message.server == undertale_server:
			if '🅱' in message.content:
				await client.send_typing(message.channel)
				await asyncio.sleep(1)
				await client.send_message(message.channel, 'No b emojis vegena')
				print('Kicking: ' + message.server.get_member(message.author.id).name)
				await asyncio.sleep(3)
				await client.kick(message.server.get_member(message.author.id))
			if message.author.id == configtxt['shushed']:
				await client.delete_message(message)
			elif message.content.startswith('!shush'):
				try:
					shushuser = message.content.split(' ')[1]
					shushuser = discord.utils.find(lambda m: m.name == shushuser, message.server.members)
				except:
					await client.send_message(message.channel, 'That user is invalid. Try again.')
					return
				shushuser = shushuser.id
				print('User {} used shush command on user {}'.format(message.author, message.server.get_member(shushuser)))
				await client.send_typing(message.channel)
				await asyncio.sleep(0.5)
				vote_start = await client.send_message(message.channel, "Starting a vote to shush {}. Respond with either 'aye' or 'nae' within the next 30 seconds to cast your vote.".message.server.get_member(shushuser))
				voted = []
				y = 0
				await asyncio.sleep(15)
				async for vote in client.logs_from(message.channel, limit=100, after=vote_start):
					if vote.author in voted or vote.author == shushed:
						continue
					else:
						if check_vote(vote.content) is None:
							continue
						elif check_vote(vote.content):
							y += 1
							print('User {} voted aye.'.format(vote.author))
							voted.append(vote.author)
						else:
							print('User {} voted nae.'.format(vote.author))
							voted.append(vote.author)
				in_channel = [m for m in message.server.members if m.status == discord.Status.online and message.channel.permissions_for(m).send_messages and not m.bot]
				requirement = 0
				if len(in_channel) == 2 or len(in_channel) == 1:
					requirement = 1
				else:
					requirement = math.ceil(len(in_channel) / 2)
					#requirement = 1
				if y >= requirement:
					await asyncio.sleep(1)
					await client.send_message(message.channel, 'The vote has passed. The user {} has been shushed. Use !unshush (user) to undo this.'.format(message.server.get_member(shushuser)))
					configtxt['shushed'] = str(shushuser)
				else:
					await client.send_typing(message.channel)
					await asyncio.sleep(1)
					await client.send_message(message.channel, 'The vote has failed.')
				with open('config.json', 'w') as outfile:
					json.dump(configtxt, outfile)
				

			elif message.content.startswith('!unshush'):
				shushuser = configtxt['shushed']
				print('User {} used unshush command on user {}'.format(message.author, message.server.get_member(shushuser)))
				await client.send_typing(message.channel)
				await asyncio.sleep(0.5)
				vote_start = await client.send_message(message.channel, "Starting a vote to unshush {}. Respond with either 'aye' or 'nae' within the next 30 seconds to cast your vote.".format(message.server.get_member(shushuser)))
				voted = []
				y = 0
				await asyncio.sleep(15)
				async for vote in client.logs_from(message.channel, limit=100, after=vote_start):
					if vote.author in voted or vote.author.id == shushuser:
						continue
					else:
						if check_vote(vote.content) is None:
							continue
						elif check_vote(vote.content):
							y += 1
							print('User {} voted aye.'.format(vote.author))
							voted.append(vote.author)
						else:
							print('User {} voted nae.'.format(vote.author))
							voted.append(vote.author)
				in_channel = [m for m in message.server.members if m.status == discord.Status.online and message.channel.permissions_for(m).send_messages and not m.bot]
				requirement = 0
				if len(in_channel) == 2 or len(in_channel) == 1:
					requirement = 1
				else:
					requirement = math.ceil(len(in_channel) / 2)
					#requirement = 1
				if y >= requirement:
					await asyncio.sleep(1)
					await client.send_message(message.channel, 'The vote has passed. The user {} has been unshushed. Use !shush (user) to redo this.'.format(message.server.get_member(shushuser)))
					configtxt['shushed'] = ''
				else:
					await client.send_typing(message.channel)
					await asyncio.sleep(1)
					await client.send_message(message.channel, 'The vote has failed.')
				with open('config.json', 'w') as outfile:
					json.dump(configtxt, outfile)

			elif message.content.startswith('!isshushed'):
				if configtxt['shushed'] == '':
					await client.send_message(message.channel, 'No one is currently shushed.')
				else:
					await client.send_message(message.channel, 'The user {} is currently shushed.'.format(message.server.get_member(configtxt['shushed'])))

			elif message.content.lower() == 'apsbot are you there':
				await client.send_message(message.channel, 'Yes.')
			
			elif message.content.lower() == '!udpate' and message.author == message.server.get_member('283414992752082945'):
				await client.send_message(message.channel, 'Closing to update')
				os.system('gitpull.bat')
				sys.exit()

			elif message.author == message.server.get_member('283414992752082945') and message.content.startswith('!off'):
				await client.close()
			
			"""
			else:
				for word in message.content:
					if d.check(word):
						pass
					else:
						await client.send_message(message.channel, 'The word {} is misspelled.'.format('word'))
			"""


			


@client.event
async def on_error(*args):
    print('An error has been caught.')
    print(traceback.format_exc())
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
                            choice(configtxt['error_messages']),
                            args[1].author.name,
                            aan(sys.exc_info()[0].__name__),
                            sys.exc_info()[0].__name__)
                        )

client.run(configtxt['token'])

config.close()

with open('config.json', 'w') as outfile:
	json.dump(configtxt, outfile)
client.logout()
