#Python Text RPG

#Lost Hero#

import cmd
import textwrap
import sys
import os
import time
import random

screen_width = 100

#### Player Setup ####

class Player():
	def __init__(self):
		self.name = '' # Name
		self.hp = 0 # HP 
		self.mp = 0 # Magic Points
		self.status_effects = [] # Status Effects
		self.location = 'start'
		self.job = ''
		self.game_over = False
myPlayer = Player()

#### Title Screen ####

def title_screen_select():
	option = input(">")
	if(option.lower() == ("play")):
		setup_game()
	elif(option.lower() == ("help")):
		help_menu()
	elif(option.lower() == ("quit")):
		sys.exit()
	while(option.lower() not in ['play', 'help', 'quit']):
		print("Please enter a valid command.")
		option = input(">")
		if(option.lower() == ("play")):
			setup_game()
		elif(option.lower() == ("help")):
			help_menu()
		elif(option.lower() == ("quit")):
			sys.exit()

def title_screen():
	os.system('clear')
	print("####################################")
	print("# Welcome to Fallen Hero Text RPG! #")
	print("####################################")
	print("               - Play -             ")
	print("               - Help -             ")
	print("               - Quit -             ")
	print("      - Copyright Furnicarul -      ")
	title_screen_select()

def help_menu():
	print("####################################")
	print("# Welcome to Fallen Hero Text RPG! #")
	print("####################################")
	print("- Use up, down, left, right to move -")
	print("- Type your commands to do them -")
	print("- Good Luck & Have Fun -")
	print("      - Copyright Furnicarul -      ")
	title_screen_select()


#### MAP ####


#-------------#
#	| 	|   |   |
#-------------#
#	|		|		|		|
#-------------#
#	|		|		|		|
#-------------#
#	|		|		|		|
#-------------#

ZONENAME = ''
DESCRIPTION = 'description'
EXAMINATION = 'examine'
SOLVED = False
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

solved_places = {'a1': False, 'a2': False, 'a3': False,
								'b1': False, 'b2': False, 'b3': False,
								'c1': False, 'c2': False, 'c3': False,
								'd1': False, 'd2': False, 'd3': False
								}

zonemap = {
	'a1': {
		ZONENAME: 'Start',
		DESCRIPTION: 'The adventure start here...',
		EXAMINATION: 'Go you mighty adventurer ! Make your story heard by everyone',
		SOLVED: False,
		UP: '',
		DOWN: 'b1',
		LEFT: '',
		RIGHT: 'a2',
	},
	'a2': {
		ZONENAME: 'The Forge',
		DESCRIPTION: 'The place where you can make your arrmor and sword more powerful',
		EXAMINATION: 'The best forge in the World',
		SOLVED: False,
		UP: '',
		DOWN: 'b2',
		LEFT: 'a1',
		RIGHT: 'a3',
	},
	'a3': {
		ZONENAME: 'Town Market',
		DESCRIPTION: 'The place where you can buy amazing stuff',
		EXAMINATION: 'Cool items and people that you can met',
		SOLVED: False,
		UP: '',
		DOWN: 'b3',
		LEFT: 'a2',
		RIGHT: '',
	},
	'b1': {
		ZONENAME: 'Home',
		DESCRIPTION: 'description',
		EXAMINATION: 'examine',
		SOLVED: False,
		UP: 'up',
		DOWN: 'down',
		LEFT: 'left',
		RIGHT: 'right',
	},
	'b2': {
		ZONENAME: 'The Hole',
		DESCRIPTION: 'This the mother of the spiders live...',
		EXAMINATION: 'If you kill her you will gain Legendary Gear !',
		SOLVED: False,
		UP: 'a2',
		DOWN: 'c2',
		LEFT: 'b1',
		RIGHT: 'b3',
	},
	'b3': {
		ZONENAME: 'The Graveyard',
		DESCRIPTION: 'The skelletons are killing the villigers ! Save them !',
		EXAMINATION: 'The skelletions',
		SOLVED: False,
		UP: 'a3',
		DOWN: 'c3',
		LEFT: 'b2',
		RIGHT: '',
	},
	'c1': {
		ZONENAME: 'The Fallen Hero...',
		DESCRIPTION: 'Here his sword rests and waits to be bringed back to fight',
		EXAMINATION: 'The Most Powerfull Sword',
		SOLVED: False,
		UP: 'b1',
		DOWN: 'd1',
		LEFT: 'b3',
		RIGHT: 'c2',
	},
	'c2': {
		ZONENAME: 'The Castel',
		DESCRIPTION: 'The place where The Mighty King rest with his palladins...',
		EXAMINATION: 'Go and take some quests',
		SOLVED: False,
		UP: 'b2',
		DOWN: 'd2',
		LEFT: 'c1',
		RIGHT: 'c3',
	},
	'c3': {
		ZONENAME: 'The Gates',
		DESCRIPTION: 'Where adventurers start the adventure !',
		EXAMINATION: 'Go and kill some rats or goblins and start your ADVENTURE',
		SOLVED: False,
		UP: 'b3',
		DOWN: 'd3',
		LEFT: 'c2',
		RIGHT: '',
	},
	'd1': {
		ZONENAME: 'Orks Market',
		DESCRIPTION: 'The place where the magic wakes up to life !',
		EXAMINATION: 'There are some cool items that I can buy...Only if I afford',
		SOLVED: False,
		UP: 'c1',
		DOWN: '',
		LEFT: 'c3',
		RIGHT: 'd2',
	},
	'd2': {
		ZONENAME: 'The ghost forest',
		DESCRIPTION: 'Ghost Forest - Sight...',
		EXAMINATION: 'This place looks creepy, kill the ghosts fast',
		SOLVED: False,
		UP:'c2',
		DOWN: '',
		LEFT: 'd1',
		RIGHT: 'd3',
	},
	'd3': {
		ZONENAME: 'Dungeon',
		DESCRIPTION: 'The place where monsters wake up to life',
		EXAMINATION: 'This place looks horror, kill them fast and go home',
		SOLVED: False,
		UP: 'c3',
		DOWN: '',
		LEFT: 'd2',
		RIGHT: '',
	},
}


#### Game INTERACTIVITY ####
def print_location():
	print('\n' + ('#' * (4 + len(myPlayer.location))))
	print('#' + myPlayer.location.upper() + '#')
	print('#' + zonemap[myPlayer.location][DESCRIPTION] + '#')
	print('\n' + ('#' * (4 + len(myPlayer.location))))

def prompt():
	print("\n" + "===============================")
	print("What would you like to do ?")
	action = input(">")
	acceptable_action = ['move', 'go', 'travel', 'walk', 'quit', 'examine', 'inspect', 'interact', 'look']
	while(action.lower() not in acceptable_action):
		print("Unknown action, try again.\n")
		action = input(">")
	if(action.lower() == "quit"):
		sys.exit()
	elif(action.lower() in ['move', 'go', 'travel', 'walk']):
		player_move(action.lower())
	elif(action.lower() in ['move', 'go', 'travel', 'walk', 'quit']):
		player_examine(action.lower())


def player_move(myAction):
	ask = "Where would you like to move to ?\n"
	dest = input(ask)
	if(dest in ['up']):
		destination = zonemap[myPlayer.location][UP]
		movement(destination)
	if(dest in ['down']):
		destination = zonemap[myPlayer.location][DOWN]
		movement(destination)
	if(dest in ['left']):
		destination = zonemap[myPlayer.location][LEFT]
		movement(destination)
	if(dest in ['right']):
		destination = zonemap[myPlayer.location][RIGHT]
		movement(destination)

def movement(destination):
	print("\n" + "You have moved to the " + destination + ".")
	myPlayer.location = destination
	print_location()

def player_examine(action):
	if zonemap[myPlayer.location][SOLVED]:
		print("You already did it.")
	else:
		print("You can trigger a puzzle here")

def main_game_loop():
	while(myPlayer.game_over == False):
		prompt()

def setup_game():
	os.system('clear')

	question1 = "Whats your name?\n"
	for char in question1:
		sys.stdout.write(char)
		sys.stdout.flush()
		time.sleep(0.05)
	player_name = input(">")
	myPlayer.name = player_name

	question2 = "Whats your role?\n"
	question2added = "(You can play as a warrior, mage or palladin)\n"
	for char in question2:
		sys.stdout.write(char)
		sys.stdout.flush()
		time.sleep(0.05)
	for char in question2added:
		sys.stdout.write(char)
		sys.stdout.flush()
		time.sleep(0.01)
	player_job = input(">")
	valid_jobs = ['warrior', 'mage', 'palladin']
	if(player_job.lower() in valid_jobs):
		myPlayer.job = player_job
		print("You are now a " + player_job + "!\n")
	while(player_job.lower() not in valid_jobs):
		player_job = input(">")
		if(player_job.lower() in valid_jobs):
			myPlayer.job = player_job
			print("You are now a " + player_job + "!\n")
	#### Player Stats ####
	if(myPlayer.job is 'warrior'):
		self.hp = 220
		self.mp = 50
	elif(myPlayer.job is 'mage'):
		self.hp = 120
		self.mp = 200
	elif(myPlayer.job is 'palladin'):
		self.hp = 200
		self.mp = 150
	
	question3 = "Welcome, " + player_name + " the " + player_job + ".\n"
	for char in question3:
		sys.stdout.write(char)
		sys.stdout.flush()
		time.sleep(0.05)
	player_name = input(">")
	myPlayer.name = player_name

	speech1 = "Welcome to this Fantasy World !\n"
	speech2 = "Good Luck & Have Fun\n"
	speech3 = "Hehehehhe...\n"
	for char in speech1:
		sys.stdout.write(char)
		sys.stdout.flush()
		time.sleep(0.03)
	for char in speech2:
		sys.stdout.write(char)
		sys.stdout.flush()
		time.sleep(0.03)
	for char in speech3:
		sys.stdout.write(char)
		sys.stdout.flush()
		time.sleep(0.03)
	os.system('clear')
	print("#######################")
	print("#      Lets start     #")
	print("#######################")
	main_game_loop()

title_screen()