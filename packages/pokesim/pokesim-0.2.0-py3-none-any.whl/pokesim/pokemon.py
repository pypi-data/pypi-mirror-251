"""
Defines data structures and routines for dealing with a pokemon and its various metadata
"""

import random
import os
from . import nature
from . import move
from . import utils
from . import constants
from . import poketypes

suffixes = {0:"st", 1:"nd", 2:"rd", 3:"th"}

class Pokemon():
	"""
	A class representing a pokemon, and all the information that entails
	"""

	def __init__(self, species: str, name: str | None = None):
		"""
		Creates a pokemon, reading in basic data from a file in `../data/pokemon/<name>`
		"""
		self.species = species
		self.name = name if name else species
		self.accuracy = 100
		self.evasiveness = 100
		self.status = constants.NON
		self.priority = 0
		self.stages = {
			constants.ATTACK: 0,
			constants.DEFENSE: 0,
			constants.SPECIAL_ATTACK: 0,
			constants.SPECIAL_DEFENSE: 0,
			constants.SPEED: 0,
			constants.CRIT: 0,
			constants.ACCURACY: 0,
			constants.EVASIVENESS: 0
		}
		self.EVs = [0,0,0,0,0,0]
		self.level = 0
		self.nature: str | None = None
		self.shadow = False

		with open(os.path.join(utils.dataDir, "pokemon", species)) as datafile:
			lines = datafile.read().split("\n")
			self.type1 = poketypes.Type(int(lines[0]))
			self.type2 = poketypes.Type(int(lines[1]))
			if int(lines[2]):
				self.gender = 'n'
			else:
				self.gender = 'm'
			self.height = float(lines[3])
			self.weight = float(lines[4])
			self.maxHP = int(lines[5])
			self.attack = int(lines[6])
			self.defense = int(lines[7])
			self.specialAttack = int(lines[8])
			self.specialDefense = int(lines[9])
			self.speed = int(lines[10])
			self.availableAbilities = lines[11].split(" ")
			self.ability = None
			self.availableMoves: set[tuple[str, int]] = set()
			self.moves = [move.Move(""), move.Move(""), move.Move(""), move.Move("")]

			for line in lines[12:]:
				if not line:
					# handles blank lines at the end of POSIX-compliant text files
					break
				line = line.split(" ")
				requiredLevel = int(line.pop())
				self.availableMoves.add((" ".join(line), requiredLevel))

		self.hp = self.maxHP

	def setStats(self):
		"""
		Sets a pokemons's stats based on its nature, EVs and base stats
		(assumes perfect IVs)
		"""
		if self.nature is None:
			raise ValueError("Pokemon isn't initialized; cannot set stats (use setup)")
		mults = nature.statMult(self.nature)

		self.maxHP = (2 * self.maxHP) + 31 + int( self.EVs[0] / 4.0 )
		self.maxHP = int(self.maxHP * self.level / 100.0)
		self.maxHP = self.maxHP + self.level + 10
		self.hp = self.maxHP

		self.attack = (2 * self.attack) + 31 + int( self.EVs[1] / 4.0 )
		self.attack = int(self.attack * self.level / 100.0)
		self.attack += 5
		self.attack = int(self.attack * mults[0])

		self.defense = (2.0 * self.defense) + 31 + int( self.EVs[2] / 4.0 )
		self.defense = int(self.defense * self.level / 100.0)
		self.defense += 5
		self.defense = int(self.defense * mults[1])

		self.specialAttack = (2.0 * self.specialAttack) + 31 + int( self.EVs[3] / 4.0 )
		self.specialAttack = int(self.specialAttack * self.level / 100.0)
		self.specialAttack += 5
		self.specialAttack = int(self.specialAttack * mults[2])

		self.specialDefense = (2.0 * self.specialDefense) + 31 + int( self.EVs[4] / 4.0 )
		self.specialDefense = int(self.specialDefense * self.level / 100.0)
		self.specialDefense += 5
		self.specialDefense = int(self.specialDefense * mults[3])

		self.speed = (2.0 * self.speed) + 31 + int( self.EVs[5] / 4.0 )
		self.speed = int(self.speed * self.level / 100.0)
		self.speed += 5
		self.speed = int(self.speed * mults[4])

	def setMove(self, moveNo: int):
		"""
		An interactive routine to set the pokemon's `moveNo`th move
		"""
		available = { availableMove[0] for availableMove in self.availableMoves
		                       if availableMove[1] <= self.level }

		utils.setCompleter(available)
		for index, knownMove in enumerate(self.moves):
			if knownMove.name and index != moveNo:
				available.remove(str(knownMove))
		while True:
			print(f"Select {self}'s {moveNo+1}{suffixes[moveNo]} move.")
			choice = input("(move, or type 'l' to list available moves) [Debug Moveset]:")
			if not choice:
				self.moves[moveNo] = move.Move(["Growl", "Sweet Scent", "Razor Leaf", "Vine Whip"][moveNo])
				self.moves[moveNo].readData()
				break
			if choice == 'l':
				utils.cls()
				for availableMove in available:
					print(availableMove)
				print()
				continue
			elif choice in available:
				self.moves[moveNo] = move.Move(choice)
				self.moves[moveNo].readData()
				break
			elif choice and choice in (x.name for x in self.moves if x):
				utils.cls()
				print(self, "already knows", f"{choice}!\n")
			utils.cls()
			print(f"Unrecognized move: '{choice}'\n")

	def changeStage(self, stat: constants.Stats, amt: int) -> str:
		"""
		Changes a Pokemon's stat (specified by 'stat') stage by the given amount.
		Returns a string describing what took place.
		"""
		if amt > 0 and self.stages[stat] >= 6:
			self.stages[stat] = 6
			return f"{self}'s {stat} won't go any higher!"
		elif amt < 0 and self.stages[stat] <= -6:
			self.stages[stat] = -6
			return f"{self}'s {stat} won't go any lower!"

		self.stages[stat] = (self.stages[stat] + amt )
		if self.stages[stat] > 6:
			self.stages[stat] = 6
		elif self.stages[stat] < -6:
			self.stages[stat] = -6

		return f"{self}'s {stat} {constants.statChangeFlavorText(amt)}"


	def useMove(self, mymove: move.Move, otherpoke: 'Pokemon', othermove: move.Move) -> str:
		"""
		Handles what happens when a pokemon uses a move on another pokemon.
		Returns a string describing the interaction
		"""
		mymove.pp -=1
		hitChance = random.randrange(101)
		effacc = 100.0
		if self.stages[constants.ACCURACY] > 0:
			effacc *= ( 3 + self.stages[constants.ACCURACY] ) / 3.0
		elif self.stages[constants.ACCURACY] < 0:
			effacc *= 3.0 / ( 3 + self.stages[constants.ACCURACY] )

		effev = 100.0
		if otherpoke.stages[constants.EVASIVENESS] > 0:
			effev *= ( 3 + otherpoke.stages[constants.EVASIVENESS] ) / 3.0
		elif otherpoke.stages[constants.EVASIVENESS] < 0:
			effev *= 3.0 / ( 3 - otherpoke.stages[constants.EVASIVENESS] )

		if hitChance > int(mymove.accuracy * effacc / effev ):
			return f"... but it {'missed' if mymove.moveType != move.STATUS else 'failed'}!"

		# Some damaging move, either physical or special
		if mymove.moveType != move.STATUS:
			dmg, eventStr = calcDmg(self, mymove, otherpoke, othermove)
			otherpoke.hp -= dmg
			if otherpoke.hp < 0:
				otherpoke.hp = 0
			return f"{eventStr}It dealt {dmg} damage!"

		# Some status move
		else:
			targetPoke = self if mymove.target else otherpoke
			return "\n".join(
			    targetPoke.changeStage(stat, mymove.stageChanges[i])\
			    for i, stat in\
			    enumerate(mymove.affectedStats))

	def __repr__(self) -> str:
		"""
		A string representation of a Pokemon
		"""
		printstr = ['Lv. {:<3d} {:<24s}'.format(self.level, str(self))]
		printstr.append("Type: {:>8s}{: <42s}".format(str(self.type1),
			                                '/'+str(self.type2) if self.type2 != poketypes.TYPELESS else ''))
		printstr.append("Height: %2.1fm%s" % (self.height, ' '*20))
		printstr.append("Weight: %3.1fkg%s" % (self.weight, ' '*19))
		printstr.append("Gender: {: <24}".format("Male" if self.gender == 'm' else
			                                   ("Female" if self.gender == 'f' else
			                                   ("Genderless" if self.gender == 'n' else
			                                    "unset"))))
		printstr.append("Nature: {: <24s}".format(self.nature if self.nature else 'unset'))
		printstr.append("Status: {: <24s}".format(
		                str(self.status) if self.status != constants.NON else "Healthy"))
		printstr.append("MaxHP/CurrentHP: %4d/%4d%s" % (self.maxHP, self.hp, ' '*6))
		printstr.append("Attack: %3d (Stage: %+d)%s" % (self.attack,
		                                               self.stages[constants.ATTACK],
		                                               ' '*9))
		printstr.append("Defense: %3d (Stage: %+d)%s" % (self.defense,
		                                              self.stages[constants.DEFENSE],
		                                              ' '*8))
		printstr.append("Special Attack: %3d (Stage: %+d) " % (self.specialAttack,
		                                                      self.stages[constants.SPECIAL_ATTACK]))
		printstr.append("Special Defense: %3d (Stage: %+d)" % (self.specialDefense,
			                                                  self.stages[constants.SPECIAL_DEFENSE]))
		printstr.append("Speed: %3d (Stage: %+d)%s" % (self.speed,
			                                        self.stages[constants.SPEED],
		                                            ' '*10))
		printstr.append("Crit Stage: %+d%s" % (self.stages[constants.CRIT], ' '*18))
		printstr.append("Accuracy Stage: %+d%s" % (self.stages[constants.ACCURACY], ' '*14))
		printstr.append("Evasiveness Stage: %+d%s" % (self.stages[constants.EVASIVENESS], ' '*11))
		printstr.append("        Moves%s" % (' '*19))
		printstr.append("=====================%s" % (' '*11))
		for mymove in self.moves:
			if mymove:
				printstr.append("  {:<30s}".format(str(mymove)))


		return "\n".join(printstr)

	def __str__(self) -> str:
		"""
		Returns the name of a pokemon, ready for printing
		"""
		return self.name

def setEVs(pokemon: Pokemon):
	"""
	An interactive procedure to set the EVs of a given pokemon
	"""
	total = 510
	while total:
		print(f"Choose a stat to put Effort Values into (You have {total} remaining EVs to spend)\n")
		print(f"[0]: HP              -\t{pokemon.EVs[0]}")
		print(f"[1]: Attack          -\t{pokemon.EVs[1]}")
		print(f"[2]: Defense         -\t{pokemon.EVs[2]}")
		print(f"[3]: Special Attack  -\t{pokemon.EVs[3]}")
		print(f"[4]: Special Defense -\t{pokemon.EVs[4]}")
		print(f"[5]: Speed           -\t{pokemon.EVs[5]}")
		print()
		stat = input("[Default stats - 252 HP, 252 ATK, 6 DEF]:")
		if not stat:
			pokemon.EVs = [252, 252, 6, 0, 0, 0]
			utils.cls()
			break
		try:
			stat = int(stat)
			if stat not in range(6):
				utils.cls()
				print("Please choose one of the displayed numbers")
				print()
				continue
		except ValueError:
			utils.cls()
			print("Please enter a number")
			print()
			continue
		print()
		print("Now enter the number of effort values to increase by (max for one stat is 252)")
		amt = input(":")
		try:
			amt = int(amt)
		except ValueError:
			utils.cls()
			print("Please enter a number")
			print()
			continue
		utils.cls()
		if amt + pokemon.EVs[stat] > 252:
			print("Amount would overflow stat! (max 252)\n")
		elif amt + pokemon.EVs[stat] < 0:
			print("Cannot have less than 0 EVs!\n")
		elif total - amt < 0:
			print("You don't have that many EVs to spend!\n")
		else:
			pokemon.EVs[stat] += amt
			total -= amt

def setGender(pokemon: Pokemon):
	"""
	Interactively sets a Pokemon's gender
	"""
	while pokemon.gender != 'n':
		print("Choose the Pokémon's gender")
		choice = input('(m/f) [m]: ')
		if choice in {'m', 'f'}:
			pokemon.gender = choice
			break
		elif not choice:
			pokemon.gender = 'm'
			break
		utils.cls()
		print("This ain't tumblr")

def setLevel(pokemon: Pokemon):
	"""
	interactively sets a Pokemon's level
	"""
	while not pokemon.level:
		print("Choose the Pokémon's level")
		choice = input("(1-100) [100]: ")
		try:
			if not choice:
				pokemon.level = 100
			elif int(choice) in range(1,101):
				pokemon.level = int(choice)
			else:
				utils.cls()
				print(choice, "is not a valid level!")
		except ValueError:
			utils.cls()
			print("Please enter a number.")

def setNature(pokemon: Pokemon):
	"""
	Interactively sets a Pokemon's Nature
	"""
	utils.setCompleter({n for n in nature.Natures.keys()})
	while not pokemon.nature:
		print(f"Choose {pokemon}'s nature")
		choice = input("(Nature, or 'l' to list natures) [Hardy]: ")
		if choice == 'l':
			utils.cls()
			nature.printNatures()
			print()
			continue
		elif choice in nature.Natures:
			pokemon.nature = choice
			break
		elif not choice:
			pokemon.nature = 'Hardy'
			break
		utils.cls()
		print(f"Not a nature: '{choice}'")
	utils.setCompleter(set())

def setup(pokemon: Pokemon):
	"""
	Totally sets up a Pokemon, interactively.
	"""
	utils.setCompleter(set())
	utils.cls()
	setGender(pokemon)
	utils.cls()
	setLevel(pokemon)
	utils.cls()
	setNature(pokemon)
	utils.cls()
	setEVs(pokemon)
	pokemon.setStats()

	for i in range(4):
		pokemon.setMove(i)
		utils.cls()

def calcTypeEffectiveness(unused_attacker: Pokemon, defender: Pokemon, attack: move.Move) -> float:
	"""
	Calculates the type effectiveness modifier of an attack
	"""
	at1, at2 = attack.type1.value, attack.type2.value
	dt1, dt2 = defender.type2.value, defender.type2.value

	# Shadow moves have special rules, which I'll presumably use in the future
	if attack.type1 == poketypes.SHADOW:
		return 0.5 if defender.shadow else 2.0

	mod = poketypes.typechart[at1][dt1] * poketypes.typechart[at1][dt2]

	return mod * poketypes.typechart[at2][dt1] * poketypes.typechart[at2][dt2]

def calcDmg(pkmn: Pokemon, myMove: move.Move, otherpkmn: Pokemon, unused_othermove: move.Move) -> tuple[int, str]:
	"""
	Calculates damage done by pkmn to otherpkmn (who used 'othermove', if that matters)
	"""
	dmg = 2 * pkmn.level / 5.0
	dmg += 2
	dmg *= myMove.power

	eventStr = ''

	crit = move.critical(myMove.crit, pkmn.stages[constants.CRIT])
	if crit > 1:
		eventStr = "A critical hit!\n"

	effat, effdef = 0.0, 0.0
	atstage, defstage = 0, 0

	#Physical attack
	if myMove.moveType == move.PHYSICAL:
		effat = pkmn.attack
		effdef = pkmn.defense
		atstage = pkmn.stages[constants.ATTACK]
		defstage = otherpkmn.stages[constants.DEFENSE]
	#Special attack
	else:
		effat = pkmn.specialAttack
		effdef = pkmn.specialDefense
		atstage = pkmn.stages[constants.SPECIAL_ATTACK]
		defstage = otherpkmn.stages[constants.SPECIAL_DEFENSE]

	if atstage > 0:
		effat *= (2.0 + atstage) / 2.0
	elif atstage < 0 and crit == 1:
		effat *= 2.0 / (2.0 - atstage)

	if defstage > 0 and crit ==1:
		effdef *= (2.0 + defstage) / 2.0
	elif defstage < 0:
		effdef *= 2.0 / (2.0 - defstage)


	dmg *= effat/effdef
	dmg /= 50
	dmg += 2

	#Caclucate modifier
	mod = random.uniform(0.85, 1)
	if myMove.type1 != poketypes.TYPELESS:
		if pkmn.type1 == myMove.type1 or pkmn.type2 == myMove.type2:
			mod *= 1.5

	if myMove.type2 != poketypes.TYPELESS:
		if pkmn.type1 == myMove.type2 or pkmn.type2 == myMove.type2:
			mod *= 1.5

	if pkmn.status == constants.BRN and myMove.moveType == move.PHYSICAL:
		mod /= 2.0

	typeMod = calcTypeEffectiveness(pkmn, otherpkmn, myMove)
	mod *= typeMod

	if not typeMod:
		eventStr += 'But it had no effect!\n'
	elif typeMod < 1:
		eventStr += "It's not very effective...\n"
	elif typeMod > 1:
		eventStr += "It's super effective!\n"

	dmg *= mod * crit

	return int(dmg), eventStr
