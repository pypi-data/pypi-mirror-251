"""
Defines pokemon types and methods for dealing with them
"""

import enum
import sys
from . import color

class Type(enum.Enum):
	"""
	Holds information about a pokemon's type, including metadata and pretty-printing information.
	"""

	# Pokemon Types
	Normal   =  0
	Fighting =  1
	Flying   =  2
	Poison   =  3
	Ground   =  4
	Rock     =  5
	Bug      =  6
	Ghost    =  7
	Steel    =  8
	Fire     =  9
	Water    = 10
	Grass    = 11
	Electric = 12
	Psychic  = 13
	Ice      = 14
	Dragon   = 15
	Dark     = 16
	Fairy    = 17
	Shadow   = 18
	Typeless = 19

	@staticmethod
	def colors() -> dict["Type", color.Color]:
		"""
		Returns a dictionary for getting the color associated with a type
		"""
		return {
			Type.Normal: color.Color(168, 168, 120),
			Type.Fighting: color.Color(192, 48, 40),
			Type.Flying: color.Color(168, 144, 240),
			Type.Poison: color.Color(160, 64, 160),
			Type.Ground: color.Color(224, 192, 104),
			Type.Rock: color.Color(184, 160, 56),
			Type.Bug: color.Color(168, 184, 32),
			Type.Ghost: color.Color(112, 88, 152),
			Type.Steel: color.Color(184, 184, 208),
			Type.Fire: color.Color(240, 128, 48),
			Type.Water: color.Color(104, 144, 240),
			Type.Grass: color.Color(120, 200, 80),
			Type.Electric: color.Color(248, 208, 48),
			Type.Psychic: color.Color(248, 88, 136),
			Type.Ice: color.Color(152, 216, 216),
			Type.Dragon: color.Color(112, 56, 248),
			Type.Dark: color.Color(112, 88, 72),
			Type.Fairy: color.Color(238, 153, 172),
			Type.Shadow: color.Color(96, 78, 130)
		}


	def __str__(self) -> str:
		"""
		Returns a (possibly colorful) string name of a type
		"""

		# Typeless has no string representation
		if self is Type.Typeless:
			return ""

		# Print in color if possible
		if sys.stdout.isatty():
			return color.colorSprintf(self._name_, Type.colors()[self])
		return self._name_

# Constant types for export
NORMAL   =  Type.Normal
FIGHTING =  Type.Fighting
FLYING   =  Type.Flying
POISON   =  Type.Poison
GROUND   =  Type.Ground
ROCK     =  Type.Rock
BUG      =  Type.Bug
GHOST    =  Type.Ghost
STEEL    =  Type.Steel
FIRE     =  Type.Fire
WATER    = Type.Water
GRASS    = Type.Grass
ELECTRIC = Type.Electric
PSYCHIC  = Type.Psychic
ICE      = Type.Ice
DRAGON   = Type.Dragon
DARK     = Type.Dark
FAIRY    = Type.Fairy
SHADOW   = Type.Shadow
TYPELESS = Type.Typeless

typechart = ((1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 0.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
             (2.0, 1.0, 0.5, 0.5, 1.0, 2.0, 0.5, 0.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0),
             (1.0, 2.0, 2.0, 1.0, 1.0, 0.5, 2.0, 1.0, 0.5, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
             (1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 1.0, 0.5, 0.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0),
             (1.0, 1.0, 0.0, 2.0, 1.0, 2.0, 0.5, 1.0, 2.0, 2.0, 1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
             (1.0, 0.5, 2.0, 1.0, 0.5, 1.0, 2.0, 1.0, 0.5, 2.0, 1.0, 0.5, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0),
             (1.0, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 1.0, 2.0, 1.0, 2.0, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0),
             (0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0),
             (1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 1.0),
             (1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 2.0, 1.0, 2.0, 0.5, 0.5, 2.0, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0),
             (1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 2.0, 0.5, 0.5, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0),
             (1.0, 1.0, 0.5, 0.5, 2.0, 2.0, 0.5, 1.0, 0.5, 0.5, 2.0, 0.5, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0),
             (1.0, 1.0, 2.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 0.5, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0),
             (1.0, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0),
             (1.0, 1.0, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 2.0, 1.0, 1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 1.0),
             (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 0.0, 1.0, 1.0),
             (1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0),
             (1.0, 2.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0),
             (2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 0.5, 1.0),
             (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0))
