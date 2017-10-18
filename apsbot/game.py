from apsbot import base
from apsbot.base import config

import asyncio

import sqlite3

conn = sqlite3.connect('rpgdata.cb')

movements = {
	'north' : ('y', 1),
	'up' : ('y', 1),
	'south' : ('y', -1),
	'down' : ('y', -1),
	'left' : ('x', -1),
	'west' : ('x', -1),
	'right' : ('x', 1),
	'east' : ('x', 1)
}

def moveplayer((x, y)):
	conn.execute("SELECT 1 FROM testtable LIMIT 1;")

@base.apsfunc
async def move(client, message):
	'''**{0}move (direction)**
	Move your player in your server's
	instance of the text-rpg game.
	*Example: '{0}move south'*'''
	direction = message.content.split()[1]
	try:
		if movements[direction][0] == 'x':
			move = (movements[direction][1], 0)
		elif movements[direction][0] == 'y':
			move = (0, movements[direction][1])
		
    	except KeyError:
      		print("You can't move that way.")
