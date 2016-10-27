import numpy as np
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import ephem
import sys
from astropy.time import Time

## VERSION CHECK ##
if(sys.version_info < (3,0)):
	print("Correcting for Python 2.7")
	def input(str=""):
		return raw_input(str)

'''### CLASS DESCRIPTIONS ##################################################
 class Observer(latitude, longitude, date)
	function get_nextrise(Planet)
		gets the next rise time of Planet at the observatory
	function get_nextset(Planet)
		gets the next set time of Planet at the observatory
	function get_prevrise(Planet)
		gets the previous rise time of Planet at the observatory
	function get_prevset(Planet)
		gets the previuos set time of Planet at the observatory

 class Planet(planet,rot_rate)
	## also includes the Sun ##
	variable rotationrate
		a static Planet.rot_rate or
		a function Planet.get_rot_rate()
	subclass ephem.Planet()
		used in conjunction with Observer class

 function get_best_date(Planet,Observer,date,cml)
	get the closest observable window for cml of Planet 
	 at Observer location

##########################################################################'''

## Input functions ##
def get_inp(output,default):
	## Prints out output and requests input	##
	## if input is empty, returns default 	##
	inp = input(output)
	if(inp == ""):
		inp = default
	return inp

## Input planet ##


## Input array of date and desired CML ##

