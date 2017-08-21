import discord
import asyncio

from apsbot import base

@base.apsfunc
async def help(client, message):
	await client.send_message(message.channel, 'These are my commands: ')
	for func in apsbot.base.pres:
		await client.send_message(message.channel, func)
	for func in apsbot.base.functions:
		await client.send_message(message.channel, func)
	for func in apsbot.base.posts:
		await client.send_message(message.channel, func)