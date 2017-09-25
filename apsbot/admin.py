from apsbot import base
from apsbot.base import config

from discord.ext.commands import ColourConverter

@base.apsfunc
async def changecolor(client, message):
	'''**{0}changecolor>**
	Allows you to change the color of the specified role.
	I can't change roles higher than my own,
	nor roles higher than yours.
	When picking roles, if a search matches two or more roles, 
	it will choose the first one that is returned.
	*Example: '{0}changecolor myrole green'*'''
	await client.send_message(message.channel, "Choose a role to edit:")
	for role in message.author.roles:
		if role.name == '@everyone':
			continue
		else:
			await client.send_message(message.channel, role.name)
	while True:
		choice = await client.wait_for_message(author=message.author, timeout=30)
		rolechoice = [s for s in message.author.roles if choice.content.lower() in s.name.lower()]
		if rolechoice:
			break
	rolechoice = rolechoice[0]
	if rolechoice.position >= message.author.top_role.position + 1:
		await client.send_message(message.channel, "I can't let you do that.")
		return
	else:
		await client.send_message(message.channel, "Choose color to change {}'s color to.".format(rolechoice.name))
		while True:
			newcolor = await client.wait_for_message(author=message.author, timeout=30)
			newcolor = newcolor.content
			converter = ColourConverter(None, newcolor)
			newcolorval = converter.convert()
			await client.edit_role(message.server, rolechoice, color=newcolorval)
			break
	await client.send_message(message.channel, "It is done.")
				
