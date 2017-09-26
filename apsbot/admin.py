from apsbot import base
from apsbot.base import config

from discord.ext.commands import ColourConverter
from discord.ext.commands.errors import BadArgument

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
	authorroles = []
	for role in message.server.roles:
		if role <= message.author.top_role:
			authorroles.append(role)
	for role in authorroles:
		print(role.name)
		if role.name == '@everyone':
			continue
		else:
			await client.send_message(message.channel, role.name)
			await asyncio.sleep(0.5)
	while True:
		choice = await client.wait_for_message(author=message.author, timeout=30)
		try:
			if choice.content.lower() == 'nevermind':
				await client.send_message(message.channel, "OK.")
				return
			else:
				rolechoice = [s for s in authorroles if choice.content.lower() in s.name.lower()]
				if rolechoice:
					break
				else:
					await client.send_message(message.channel, "That's not a valid role. Choose another or say nevermind to exit.")
		except:
			await client.send_message(message.channel, "You didn't provide a user.")
			return
	rolechoice = rolechoice[0]
	if rolechoice.position >= message.author.top_role.position + 1:
		await client.send_message(message.channel, "I can't let you do that.")
		return
	else:
		await client.send_message(message.channel, "Choose color to change {}'s color to.".format(rolechoice.name))
		while True:
			newcolor = await client.wait_for_message(author=message.author, timeout=30)
			newcolor = newcolor.content
			if newcolor.lower() == 'nevermind':
				await client.send_message(message.channel, "OK.")
				return
			try:
				converter = ColourConverter(None, newcolor)
				newcolorval = converter.convert()
				await client.edit_role(message.server, rolechoice, color=newcolorval)
				break
			except BadArgument:
				await client.send_message(message.channel, "That's not a valid color. Choose another one, or say nevermind to stop.")
	await client.send_message(message.channel, "It is done.")
				
