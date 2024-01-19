#!/usr/bin/env python3 -OO

"""
This package contains the functionality for a fully-playable Pokémon battle simulation.
"""

__version__ = "0.2.0"

import os
import platform
import random
import sys
from . import utils
from . import pokemon
from . import move

def chooseAPokemon(available: set[str], opponent: bool = False) -> pokemon.Pokemon:
	"""
	Gets a Pokémon from the user. If ``opponent`` is true, this is the opposing
	Pokémon.
	"""

	utils.setCompleter(available)

	choiceStr = f"Choose {'''your opponent's''' if opponent else 'a'} Pokémon"

	while True:
		print(choiceStr)
		choice = input("(Pokémon Name, or 'l' list available Pokémon) [Bulbasaur]: ")

		if choice == 'l':
			utils.cls()
			print('\n'.join(available))
			continue
		elif choice in available:
			break
		elif not choice:
			choice = "Bulbasaur"
			break
		else:
			print(f"'{choice}' is not a recognized Pokémon!")

	utils.cls()
	species = choice
	nickname = choice

	while True:
		choice = input("Nickname this Pokémon? [y/N]: ").lower()
		if choice in {'y', 'yes'}:
			while True:
				choice = input("Enter nickname (max 48 characters):")
				if choice:
					if len(choice) <= 48:
						nickname = choice
						break
					else:
						print("Nickname too long!")
				else:
					print("Nickname cannot be blank!")
			break
		elif not choice or choice in {'n', 'no'}:
			break
		print("Please enter 'y' or 'n' (or just hit 'Enter').")

	poke = pokemon.Pokemon(species, "The opponent's " + nickname if opponent else nickname)
	pokemon.setup(poke)
	return poke

def chooseAMove(poke: pokemon.Pokemon, opponent: pokemon.Pokemon) -> move.Move:
	"""
	Gets a move choice from the user
	"""

	while True:
		utils.printHealthBars(poke, opponent)
		print("Choose a move:")
		for moveNumber, mv in enumerate(poke.moves):
			print("[{:d}]: {:<30s}{:2d}/{:<2d}".format(moveNumber + 1, str(mv), mv.pp, mv.maxPP))
		print("[5] Print Pokémon for debugging")
		try:
			choice = int(input("(1-5): "))
		except ValueError:
			utils.cls()
			print("Please enter a number.\n")
		else:
			if choice in range(1, 5):
				choice = poke.moves[choice - 1]
				if choice.pp:
					break
				utils.cls()
				print("Out of PP!")
			elif choice == 5:
				utils.dumpPokemon(poke, opponent)
			else:
				utils.cls()
				print("Please enter a number from 1 to 5\n")

	return choice


def main() -> int:
	"""
	Runs the main simulator
	"""

	# Theoretically reads in the list of pokemon
	available_pokemon = set(os.listdir(os.path.join(utils.dataDir, "pokemon")))
	utils.cls()

	print("Welcome to the Pokémon Battle Simulator (written in Python3)!\n")

	userPokemon = chooseAPokemon(available_pokemon)

	utils.cls()

	opponentPokemon = chooseAPokemon(available_pokemon, True)
	utils.cls()

	# Prints the opposing pokemon
	print("Battle Starting!\n")
	utils.dumpPokemon(userPokemon, opponentPokemon)

	playerWon = False

	# Battle Loop
	while True:
		_ = input("Press Enter to continue.")

		utils.cls()

		# Player chooses a move
		choice = chooseAMove(userPokemon, opponentPokemon)
		choiceStr = f"{userPokemon} used {choice}!"

		#opponent chooses a move
		utils.cls()
		opponentChoice = opponentPokemon.moves[random.randrange(4)]
		opponentChoiceStr = f"{opponentPokemon} used {opponentChoice}!"

		order = utils.decideOrder(userPokemon, choice, opponentPokemon, choice)

		if order:
			opponentEvents = opponentPokemon.useMove(opponentChoice, userPokemon, choice)
			if not userPokemon.hp or not opponentPokemon.hp:
				utils.printHealthBars(userPokemon, opponentPokemon)
				print(opponentChoiceStr, opponentEvents, sep="\n")
				playerWon = not opponentPokemon.hp
				break

			userEvents = userPokemon.useMove(choice, opponentPokemon, opponentChoice)
			utils.printHealthBars(userPokemon, opponentPokemon)
			print(opponentChoiceStr, opponentEvents, choiceStr, userEvents, sep="\n")
			if not userPokemon.hp or not opponentPokemon.hp:
				playerWon = not opponentPokemon.hp
				break

		else:
			userEvents = userPokemon.useMove(choice, opponentPokemon, opponentChoice)
			if not userPokemon.hp or not opponentPokemon.hp:
				utils.printHealthBars(userPokemon, opponentPokemon)
				print(choiceStr, userEvents, sep="\n")
				playerWon = not opponentPokemon.hp
				break

			opponentEvents = opponentPokemon.useMove(opponentChoice, userPokemon, choice)
			utils.printHealthBars(userPokemon, opponentPokemon)
			print(choiceStr, userEvents, opponentChoiceStr, opponentEvents, sep="\n")
			if not userPokemon.hp or not opponentPokemon.hp:
				playerWon = not opponentPokemon.hp
				break

	if playerWon:
		print(opponentPokemon, "fainted.")
		print("You Win!")
	else:
		print(userPokemon, "fainted.")
		print("You lose...")

	return 0

def run():
	"""
	A wrapper for main to catch the user quitting for less ugly ends to the program
	"""
	if len(sys.argv) > 1 and sys.argv[1] in {'-V', '--version'}:
		print("pokesim - Pokémon Battle Simulator - Version", __version__, f"(Platform: Python{platform.python_version()} {platform.system()})")
		exit(0)

	random.seed()
	try:
		main()
	except (KeyboardInterrupt, EOFError):
		exit(0)
