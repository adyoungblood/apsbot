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
import traceback
import re

client = discord.Client()

config = open('config.json', 'r')
config = json.load(config)

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
			return(False)

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
	global undertale_server, apsbot,shushed
	if message.author != apsbot:
		if message.server == undertale_server:
			if message.author == shushed:
				await client.delete_message(message)
			elif message.content.startswith('!shush'):
				try:
					shushuser = message.content.split(' ')[1]
				except:
					await client.send_message(message.channel, 'That user is invalid. Try again.')
					return
				for user in message.server.members:
					if shushuser in user.name:
						shushuser = user.name
				print('User {} used shush command on user {}'.format(message.author, shushuser))
				await client.send_typing(message.channel)
				await asyncio.sleep(1)
				await client.send_message(message.channel, "Starting a vote to shush {}. Respond with either 'aye' or 'nae' within the next 45 seconds to cast your vote.".format(shushuser))
				await asyncio.sleep(7)
				final_votes = {}
				async for vote in client.logs_from(message.channel, limit=50, after=vote_start):
					print(message.content)
					if message.author in final_votes:
						pass
					else:
						final_votes.update({message.author : check_vote(message.content)})
						await client.send_message(message.channel, 'User {} has voted aye.'.format(message.author))
				ayes = 0
				for choice in final_votes:
					print(final_votes[choice])
					if final_votes[choice]:
						ayes += 1
				if ayes >= math.ceil(len(message.server.members) / 2):
					shushed = shushuser
					config[shushed] = shushed
					open('config.json', 'wb').write(config)
					await client.send_typing(message.channel)
					await asyncio.sleep(1)
					await client.send_message(message.channel, 'The vote has passed. The user {} has been shushed. Use !unshush (user) to undo this.')
				else:
					await client.send_typing(message.channel)
					await asyncio.sleep(1)
					await client.send_message(message.channel, 'The vote has failed.')
				for vote in final_votes:
					print('votes: ' + str(final_votes[vote]))
				print('ayes: ' + str(ayes))
				print('shushed: ' + shushed)
			elif message.content.startswith('!unshush'):
				print('User {} used unshush command.'.format(message.author))
				await client.send_typing(message.channel)
				await asyncio.sleep(1)
				await client.send_message(message.channel, "Starting a vote to unshush {}. Respond with either 'aye' or 'nae' within the next 45 seconds to cast your vote.".format(shushuser))
				vote_start = datetime.utcnow()
				await asyncio.sleep(7)
				final_votes = {}
				async for vote in client.logs_from(message.channel, limit=100, after=vote_start):
					if message.author in final_votes:
						pass
					else:
						final_votes.append({message.author : check_vote(message.content)})
				ayes = 0
				for choice in final_votes:
					if final_votes[choice]:
						ayes += 1
				if ayes >= math.ceil(len(message.server.members) / 2):
					shushed = ''
					config[shushed] = shushed
					open('config.json', 'wb').write(config)
					await client.send_typing(message.channel)
					await asyncio.sleep(1)
					await client.send_message(message.channel, 'The vote has passed. The user {} has been unshushed.')
				else:
					await client.send_typing(message.channel)
					await asyncio.sleep(1)
					await client.send_message(message.channel, 'The vote has failed.')
				for vote in final_votes:
					print('votes: ' + str(final_votes[vote]))
				print('ayes: ' + str(ayes))
				print('shushed: ' + shushed)


			if '🅱' in message.content:
				await client.send_typing(message.channel)
				await asyncio.sleep(1)
				await client.send_message(message.channel, 'No b emojis vegena')
				print('Kicking: ' + message.server.get_member(message.author.id).name)
				await asyncio.sleep(3)
				await client.kick(message.server.get_member(message.author.id))

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
                            choice(config['error_messages']),
                            args[1].author.name,
                            aan(sys.exc_info()[0].__name__),
                            sys.exc_info()[0].__name__)
                        )

client.run('MzM5NDgwNTI1OTUxNTk4NTky.DGPPvg._plVK_0NUbsdBPSy4pPdu_WxTnw')
