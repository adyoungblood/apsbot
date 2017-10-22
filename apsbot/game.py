#from apsbot import base
#from apsbot.base import config

import asyncio
import json

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

playerdata = json.load(open('playerdata.json'))
mapdata = json.load(open('mapdata.json'))

@base.prefunc
async def data_exists(client, message):
	try:
		aaa = playerdata[message.server.id]
	except KeyError:
		playerdata[message.server.id] = {}
	try:
		aaa = playerdata[message.server.id][message.author.id]
	except KeyError:
		playerdata[message.server.id][message.author.id] = {"health" : 0, "inventory" : {}, "location" : (0, 0, 0)}
	return True


@base.apsfunc
async def move(client, message):
	movement = message.lower().strip()[1]
	playerLoc = playerdata[message.server.id][message.author.id]["location"]

	try:
		if movements[movement][0] == 'x':
			newLoc = (playerLoc[0] + movements[movement][1], playerLoc[1], playerLoc[2])
			if mapdata
		elif movements[movement][0] == 'y':


	playerdata[message.server.id][message.author.id]["location"] = ()