import discord
import asyncio

import apsbot
from apsbot import base
from apsbot.base import pres, functions, posts

@base.apsfunc
async def help(client, message):
	await client.send_message(message.channel, 'These are my commands: ')
	for func in apsbot.base.pres:
		await client.send_message(message.channel, func)
	for func in apsbot.base.functions:
		await client.send_message(message.channel, func)
	for func in apsbot.base.posts:
		await client.send_message(message.channel, func)
