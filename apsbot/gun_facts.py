from random import choice

from apsbot import base

@base.apsfunc
async def gunfact(client, message):
	'''**{0}gunfact**
	Provides a helpful fact about a random gun, usually from the WW1/2 era.
	Facts courtesy of from Louis Leon.
	*Example: '{0}gunfact'*'''
	await client.send_message(message.channel, "Here's a little fact: {}".format(choice(base.facts)))
