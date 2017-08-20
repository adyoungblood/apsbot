import discord
import asyncio
import time

@base.prefunc
async def check_shush(client, message):
	with open('config.json', 'r') as config:
		if message.author == config['shushed']:
			client.delete_message(message)

@base.apsfunc
async def shush(client, message, votee):
	await client.send_message(message.channel, "Starting a vote to shush {}. Respond with either 'yae' or 'nae' within the next 30 seconds to cast your vote.".format(votee.name))
	vote_start = time.datetime.now
	await time.sleep(30)
	votes = {}
