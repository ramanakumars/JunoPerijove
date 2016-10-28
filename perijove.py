import numpy as np
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import sys

try:
	import ephem
except ImportError:
	print("You need pyephem to run this code. If you have pip, use pip install pyephem")
	sys.exit(1)
	
try:
	from astropy.time import Time
except ImportError:
	print("You need astropy to run this code. If you have pip, use pip install astropy")
	sys.exit(1)

## REQUIRED #############################################################
# This code requires astropy and pyephem. To install use python-pip:	#
# In a terminal, type:													#
#	pip install astropy													#
# Once complete type:													#
#	pip install pyephem													#
#########################################################################

def cmlsys3(jd):
	## IMPORTANT: jd format is YYYY-mm-ddTHH:MM:ss #
	# e.g. 	09/14/2016 at 12:25:30 PM is 2016-09-14T12:25:30
	#		09/14/2016 at 5:10:15 PM is 2016-09-14T17:10:15
    th = 0.0

    pi = np.pi
    kr = pi / 180.

    # CML III and Io phase by Radio Jupiter Pro:
    # 108.54 and 207.27

    # was used in the original QBasic source code:
    # rotationRate = 870.4529
    # CML III and Io phase obatined using this rotaion rate:
    # 108.82009487692267 207.246372083202

    # rotaion rate correction found at   http://www.projectpluto.com/grs_form.htm 
    # rotationRate = 870.4535567
    # CML III and Io phase obatined using this rotaion rate:
    # 108.82074540061876 207.246372083202

    # value found in   http://lasp.colorado.edu/home/mop/files/2015/02/CoOrd_systems7.pdf
    # "...This is the current IAU value."
    rotationRate = 870.536000
    # CML III and Io phase obatined using this rotaion rate:
    # 108.90241334354505 207.246372083202

    fjd = jd
    d0 = fjd - 2435108

    d = d0 + th / 24.0
    v = (157.0456 + .0011159 * d) % 360.0
    m = (357.2148 + .9856003 * d) % 360.0
    n = (94.3455 + .0830853 * d + .33 * np.sin(kr * v)) % 360.0
    j = (351.4266 + .9025179 * d - .33 * np.sin(kr * v)) % 360.0
    a = 1.916 * np.sin(kr * m) + .02 * np.sin(kr * 2.0 * m)
    b = 5.552 * np.sin(kr * n) + .167 * np.sin(kr * 2.0 * n)
    k = j + a - b
    r = 1.00014 - .01672 * np.cos(kr * m) - .00014 * np.cos(kr * 2.0 * m)
    re = 5.20867 - .25192 * np.cos(kr * n) - .0061 * np.cos(kr * 2.0 * n)
    dt = np.sqrt(re * re + r * r - 2 * re * r * np.cos(kr * k))
    sp = r * np.sin(kr * k) / dt
    ps = sp / .017452
    dl = d - dt / 173.0
    pb = ps - b
    xi = 150.4529 * int(dl) + rotationRate * (dl - int(dl))
    L3 = (274.319 + pb + xi + .01016 * 51.0) % 360.0
    U1 = 101.5265 + 203.405863 * dl + pb
    U2 = 67.81114 + 101.291632 * dl + pb
    z = (2.0 * (U1 - U2)) % 360.0
    U1 = U1 + .472 * np.sin(kr * z)
    U1 = (U1 + 180.0) % 360.0

    L3 = L3
    U1 = U1
    return L3, U1


#####  TO DO #########
# Figure out the minimum and maximum times for Jupiter observing #
# Calculate n rotations to minimum and maximum #
# Figure out 1 day before and 1 day after #
######################

## Setting up the observing sites ##
floridaobs = ephem.Observer()
floridaobs.lat = "28:04:58.8"
floridaobs.long = '-80:36:21.6'

kittobs = ephem.Observer()
kittobs.lat = "32:04:58.8"
kittobs.long = '-112:04:15.6'

canaryobs = ephem.Observer()
canaryobs.lat = '28:45:25'
canaryobs.long = '-17:53:33'

cerraobs = ephem.Observer()
cerraobs.lat = '-30:10:09'
cerraobs.long = '-70:48:21'

## Make a dictionary of observing sites so we can loop through them ##
obs = {"florida": floridaobs, "cerra": cerraobs, "arizona": kittobs, "canary": canaryobs}

## Get the perijove data ##
file = open('perijove_dat.txt','r')

## Open the outfile for writing ##
out = open('perijove_cml_new_h.dat','w')

jup_rotation = 9.9

''' DEPRECATED
#out.write("UTC, Eastern, Eastern - Rotation, Eastern - 1/2Rotation, Eastern + 1/2 Rotation, Eastern + Rotation, \
#			Mountain, Mountain - Rotation, Mountain - 1/2Rotation, Mountain + 1/2 Rotation, Mountain + Rotation, \
#			Canary, Canary - Rotation, Canary - 1/2Rotation, Canary + 1/2 Rotation, Canary + Rotation \n")'''
for line in file:
	## Seperate the line into arrays by splitting with whitespace ##
	dat = str.split(line)
	
	## Get the datetime data ##
	month, day, year = str.split(dat[2],"/")
	hour, min, sec = str.split(dat[3],":")
	
	## CML dat[21]
	cml_juno = np.float(dat[21])

	## Set up the UTC timezone and convert the perijove times to UTC ##
	utc = pytz.utc	
	date = datetime(int(year), int(month), int(day), int(hour), int(min), int(sec), 0, tzinfo = utc)
	
	## Set up timezones for each observatory ##
	florida = timezone('US/Eastern')
	cerra = timezone('Chile/Continental')
	arizona = timezone('US/Mountain')
	canary = timezone('Atlantic/Canary')
	
	## Create a dictionary of timezones so we can loop through them for each perijove ##
	tzs = {"florida": florida, "arizona": arizona, "cerra": cerra, "canary": canary}
	
	## Define a timezone format to output ##
	fmt = "%Y/%m/%d %H:%M:%S"
	cmlfmt = "%Y-%m-%dT%H:%M:%S"
	
	## Line defines the output string. We will add to it at each loop and write out this "line" ##
	line = "Perijove time (UTC): %s - In Florida %s "%(date.strftime(fmt), date.astimezone(florida).strftime(fmt)) + "\n"
	dateorig = date
	for dayi in range(-2,3):
		date = dateorig + timedelta(days = dayi)
		if(dayi < 0):
			line = line + "%d days before perijove \n"%(-dayi)
		elif(dayi > 0):
			line = line + "%d days after perijove \n"%(dayi)
		else:
			line = line + "Day of perijove \n"
		for timez in ['florida','cerra','arizona','canary']:
			## Select the timezone and observatory ##
			tz = tzs[timez]
			observe = obs[timez]
			
			## Set the perijove date and time ##
			peri = date
			## Match the date of the observatory to the perijove date and time ##
			observe.date = peri.strftime(fmt)
			
			## Get the time of the perijove at the local observatory ##
			perilocal = date.astimezone(tz)
			
			## Set up the observables as Jupiter and Sun 
			##(we are not observing Sun, but we need its position)
			jup = ephem.Jupiter()
			sun = ephem.Sun()
			
			## Get the following in the UTC timezone:
			##	- previous jupiter rise/set
			## 	- next jupiter rise/set
			## 	- previous sun rise/set
			##	- next sun rise/set
			
			jupprevrise = observe.previous_rising(jup)
			jupprevrise = jupprevrise.datetime()
			jupprevrise = jupprevrise.replace(tzinfo=utc)
			
			jupnextrise = observe.next_rising(jup)
			jupnextrise = jupnextrise.datetime()
			jupnextrise = jupnextrise.replace(tzinfo=utc)
			
			
			jupprevset = observe.previous_setting(jup)
			jupprevset = jupprevset.datetime()
			jupprevset = jupprevset.replace(tzinfo=utc)
			
			jupnextset = observe.next_setting(jup)
			jupnextset = jupnextset.datetime()
			jupnextset = jupnextset.replace(tzinfo=utc)
			
			sunprevrise = observe.previous_rising(sun)
			sunprevrise = sunprevrise.datetime()
			sunprevrise = sunprevrise.replace(tzinfo=utc)
			
			sunnextrise = observe.next_rising(sun)
			sunnextrise = sunnextrise.datetime()
			sunnextrise = sunnextrise.replace(tzinfo=utc)
			
			
			sunprevset = observe.previous_setting(sun)
			sunprevset = sunprevset.datetime()
			sunprevset = sunprevset.replace(tzinfo=utc)
			
			sunnextset = observe.next_setting(sun)
			sunnextset = sunnextset.datetime()
			sunnextset = sunnextset.replace(tzinfo=utc)
			
			
			## For this part, see the POSSIBILITIES comment below ##
			if(jupprevrise > jupprevset):	# i.e. jupiter is up right now
				if(sunprevrise > sunprevset):	# i.e. sun is up
					if(jupnextset > sunnextset):	# i.e. sun sets first
						condition = "JU SU SF"
						mintime = sunnextset
						maxtime = jupnextset
					if(sunnextset > jupnextset):	# i.e. jupiter sets first
						condition = "JU SU JF"
						mintime = jupnextrise
						maxtime = sunnextrise
				else:	# sun is down right now 
				#(i.e. sun set first, since jupiter is still up)
					condition = "JU SD JU"
					if(jupprevrise > sunprevset):
						mintime = jupprevrise
					else:
						mintime = sunprevset
					if(jupnextset < sunnextrise):
						maxtime = jupnextset
					else:
						maxtime = sunnextrise
			else:	# jupiter is down
				if(sunprevrise > sunprevset):	# i.e. sun is up
					# then jupiter sets first
					mintime = jupnextrise
					maxtime = sunnextrise
				else:	# sun is down right now 
					if(jupprevset > sunprevset):	# i.e. sun sets first
						mintime = sunprevset
						maxtime = jupprevset
					elif(jupnextrise < sunnextrise):	# jupiter sets first
						mintime = jupnextrise
						maxtime = sunnextrise

			## Get the times to get the CML from min and maxtime above
			mintimecml = Time(mintime.strftime(cmlfmt),format='isot', scale='utc')
			maxtimecml = Time(maxtime.strftime(cmlfmt),format='isot', scale='utc')
			
			## Calculate CML at min and max times
			mincml = cmlsys3(mintimecml.jd)[0]
			maxcml = cmlsys3(maxtimecml.jd)[0]
			
			## Save the originals for printout 
			mincmlorig = mincml
			maxcmlorig = maxcml
			
			## If maxcml goes to the next orbit, add 360
			if(maxcml < mincml): 
				maxcml = maxcml + 360.
			
			## Calculate the differences
			mindiffcml = mincml - cml_juno
			maxdiffcml = maxcml - cml_juno
			
			## Our observing windows is from mintime to maxtime ##
			mintime = mintime.astimezone(tz)
			maxtime = maxtime.astimezone(tz)
			
			### HERE: ###################################################################
			## We need to get the CML (Central meridian longitude) of Jupiter and Juno	#
			## and compare the two, to see where Juno is relative to where we are 		#
			## seeing it. Once we have this info, we can get the number of rotations to	#
			## get the same field of view of Jupiter that Juno saw. 					#
			#############################################################################
			
			printout = True
			
			if((np.abs(mindiffcml) < 40.) or (np.abs(maxdiffcml) < 40.)):
				## If the CML's are within 40degrees of Juno
				printout = True
			elif((mindiffcml < 0.) and (maxdiffcml > 0)):
				## If the CML crosses the +- 40 region over the observing window
				## This is for cases where the window is more than 1/2 Jupiter rotation
				## i.e. >5-6 hours
				printout = True
			else:
				printout = False
				#printout = True
			
			if(printout):
				## Get the number of rotations of mintime and maxtime from the perijove ##
				mindiff = (mintime - perilocal).total_seconds()/(3600.*jup_rotation) + dayi*(24./jup_rotation)
				maxdiff = (maxtime - perilocal).total_seconds()/(3600.*jup_rotation) + dayi*(24./jup_rotation)
				
				## Add that info to the output line ##
				line = line + "  %s: \n "%(timez)
				#line = line + "\tFrom %s to %s\n"%(mintime.strftime(fmt), maxtime.strftime(fmt))
				
				## If it is not Florida, convert to EST ##
				if(timez != "florida"):
					mintime = mintime.astimezone(tzs['florida'])
					maxtime = maxtime.astimezone(tzs['florida'])
					## And write that out ##
				line = line + "\tIn Florida: %s to %s\n"%(mintime.strftime(fmt), maxtime.strftime(fmt))
				
				## Add the number of rotations from perijove ##
				#line = line + "\tNumber of rotations from perijove: %.2f, %.2f\n"%(mindiff,maxdiff)
				#line = line + "\tJuno CML %.2f \t MinCML %.2f \t MaxCML %.2f\n"%(cml_juno, mincmlorig,maxcmlorig)
				line = line + "\tDifference from Juno Observation: %.2f %.2f\n"%(mindiffcml,maxdiffcml)
	line = line + "\n" ## Linebreak for clarity
	line = line + "---------------------------------------------------------------------\n"
	line = line + "\n" ## Linebreak for clarity
	## Write it out
	out.write(line)
	
print("Done")
	
'''## POSSIBILITIES ##

## Jupiter is up right now ##
jupiter is up, sun is up, sun sets first
	- observe between sunset and jupiter set
jupiter is up, sun is up, jupiter sets first
	- observe between next jupiter rise and sun rise
jupiter is up, sun is down, sun sets first
	- observe between prev sunset and next jupiter set


## Jupiter is down right now ##
jupiter is down, sun is up, jupiter sets first
	- observe between next jupiter rise and sun rise
jupiter is down, sun is down, jupiter sets first
	- observe between next jupiter rise and sun rise
jupiter is down, sun is down, sun sets first
	- observe between previous sunset and previous jupiter set
		- and next sun/jupiter set?'''