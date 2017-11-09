#from apsbot import base
#from apsbot.base import config

import asyncio
import sqlite3

movements = {
	'north' : ('y', 1),
	'forwards' : ('y', 1),
	'south' : ('y', -1),
	'backwards' : ('y', -1),
	'left' : ('x', -1),
	'west' : ('x', -1),
	'right' : ('x', 1),
	'east' : ('x', 1),
}

gamedata = sqlite3.connect('gamedata.db')

cursor = gamedata.cursor()

@base.prefunc
async def data_exists(client, message):
	try:
		cursor.execute("SELECT 1 FROM mapdata LIMIT 1;")
	except:
		cursor.execute('''CREATE TABLE mapdata
			       (x real, y real, z real, description text)''')
	try:
		cursor.execute("SELECT 1 FROM playerdata LIMIT 1;")
	except:
		cursor.execute('''CREATE TABLE playerdata
			       (x real, y real, z real, health real)''')
	

@base.apsfunc
async def move(client, message):
	movement = message.lower().strip()[1]
	playerLoc = playerdata[message.server.id][message.author.id]["location"]

	try:
		if movements[movement][0] == 'x':
			newLoc = (playerLoc[0] + movements[movement][1], playerLoc[1], playerLoc[2])
		elif movements[movement][0] == 'y':
			newLoc = (playerLoc[0], playerLoc[1] + movements[movement][1], playerLoc[2])
	except KeyError:
		await client.send_message(message.channel, 'You can\'t move that way')
		return

	await client.send_message(message.channel, 'You will move {}'.format(movement))
	playerdata[message.server.id][message.author.id]["location"] = newLoc
	return

@base.apsfunc
async def look(client, message):
	return(xd)
