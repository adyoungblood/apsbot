import discord
import asyncio
import time
import json
import os
import re
import math

from apsbot import base
from apsbot.base import config

def check_vote(string):
	string = string.split()
	for word in string:
		if re.fullmatch('aye*?', word):
			return(True)
		elif re.fullmatch('nae*?', word):
			return(False)
		else:
			return(None)

@base.prefunc
async def not_self(client, message):
	'''Checks if the message sent is not by the bot itself.'''
	if message.author.id == client.user.id:
		return False
	else:
		return True

@base.prefunc
async def no_b(client, message):
	'''The B emoji is cursed, never use it.'''
	if '🅱' in message.content:
		await client.send_typing(message.channel)
		await asyncio.sleep(1)
		await client.send_message(message.channel, 'No b emojis vegena')
		await asyncio.sleep(3)
		await client.kick(message.server.get_member(message.author.id))
		return False
	else:
		return True

@base.prefunc
async def check_shush(client, message):
	'''Checks to see if the poster is shushed; deletes message if so.'''
	with open('configs/config.json', 'r') as data:
		config = json.load(data)
		if message.author.id == config['shushed']:
			await client.delete_message(message)
			return False
		else:
			return True

@base.apsfunc
async def shush(client, message):
	'''**{0}shush <user>**
	Starts a vote to shush the user called.
	*Example: '{0}shush navid'*'''
	shushuser = message.content.split(' ')[1]
	shushuser = discord.utils.find(lambda m: m.nick.lower() == shushuser.lower(), message.server.members)
	if not shushuser:
		await client.send_message(message.channel, 'That user is invalid. Try again.')
		return
	shushuser = shushuser.id
	print('User {} used shush command on user {}'.format(message.author, message.server.get_member(shushuser)))
	await client.send_typing(message.channel)
	await asyncio.sleep(0.5)
	vote_start = await client.send_message(message.channel, "Starting a vote to shush {}. Respond with either 'aye' or 'nae' within the next 15 seconds to cast your vote.".format(message.server.get_member(shushuser)))
	voted = []
	y = 0
	await asyncio.sleep(15)
	async for vote in client.logs_from(message.channel, limit=100, after=vote_start):
		if vote.author in voted or vote.author == config['shushed']:
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
		await client.send_message(message.channel, 'The vote has passed. The user {} has been shushed. Use {}unshush (user) to undo this.'.format(message.server.get_member(shushuser), config['invoker']))
		config['shushed'] = str(shushuser)
	else:
		await client.send_typing(message.channel)
		await asyncio.sleep(1)
		await client.send_message(message.channel, 'The vote has failed.')
	with open('configs/config.json', 'w') as configfile:
		json.dump(config, configfile)

@base.apsfunc
async def unshush(client, message):
	'''**{0}unshush <user>
	Starts a vote to unshush the currently shushed user.
	*Example: '{0}unshush'*'''
	print('User {} used unshush command on user {}'.format(message.author, config['shushed']))
	await client.send_typing(message.channel)
	await asyncio.sleep(0.5)
	vote_start = await client.send_message(message.channel, "Starting a vote to unshush {}. Respond with either 'aye' or 'nae' within the next 15 seconds to cast your vote.".format(message.server.get_member(config['shushed'])))
	voted = []
	y = 0
	await asyncio.sleep(15)
	async for vote in client.logs_from(message.channel, limit=100, after=vote_start):
		if vote.author in voted or vote.author == config['shushed']:
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
		await client.send_message(message.channel, 'The vote has passed. The user {} has been unshushed. Use {}shush (user) to redo this.'.format(message.server.get_member(config['shushed']), config['invoker']))
		config['shushed'] = ''
	else:
		await client.send_typing(message.channel)
		await asyncio.sleep(1)
		await client.send_message(message.channel, 'The vote has failed.')
	with open('configs/config.json', 'w') as configfile:
		json.dump(config, configfile)

@base.apsfunc
async def isshushed(client, message):
	'''**{0}isshushed**
	Replies with the currently shushed user.'''
	if config['shushed'] == '':
		await client.send_message(message.channel, 'No one is currently shushed.')
	else:
		await client.send_message(message.channel, 'The user {} is currently shushed.'.format(message.server.get_member(config['shushed'])))

@base.apsfunc
async def youthere(client, message):
	'''**{0}youthere**
	A basic check to see if apsbot is online.'''
	await client.send_message(message.channel, 'Yes.')
	
@base.apsfunc
async def update(client, message):
	'''If you are me, then this command tells apsbot to shut down and update from the Github repo.'''
	if message.author == message.server.get_member('283414992752082945'):
		await client.send_message(message.channel, 'Closing to update, brb')
		print('Closing to update')
		os.system('gitpull.bat')
		sys.exit()
		
@base.apsfunc
async def off(client, message):
	'''If you are me, turns the bot off. I will have to manually restart it afterwards.'''
	if message.author == message.server.get_member('283414992752082945'):
		await client.close()

		
