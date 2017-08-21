import discord
import asyncio
import time
import json

from apsbot import base

@base.prefunc
async def no_b(client, message):
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
	with open('configs/config.json') as data:
		config = json.load(data)
		if message.author == config['shushed']:
			client.delete_message(message)
			return False
		else:
			return True

@base.apsfunc
async def shush(client, message):
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

@base.apsfunc
async def unshush(client, message):
	shushuser = configtxt['shushed']
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

@base.apsfunc
async def isshushed(client, message):
	if configtxt['shushed'] == '':
		await client.send_message(message.channel, 'No one is currently shushed.')
	else:
		await client.send_message(message.channel, 'The user {} is currently shushed.'.format(message.server.get_member(configtxt['shushed'])))

@base.apsfunc
async def youthere(client, message):
	await client.send_message(message.channel, 'Yes.')
	
@base.apsfunc
async def update(client, message):
	if message.author == message.server.get_member('283414992752082945'):
		print('Closing to update')
		os.system('gitpull.bat')
		sys.exit()
		
@base.apsfunc
async def off(client, message):
	if message.author == message.server.get_member('283414992752082945'):
		await client.close()

		
