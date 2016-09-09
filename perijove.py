import numpy as np
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import ephem

#####  TO DO #########
# Figure out the minimum and maximum times for Jupiter observing #
# Calculate n rotations to minimum and maximum #
# Figure out 1 day before and 1 day after #
######################

floridaobs = ephem.Observer()
floridaobs.lat = "28:04:58.8"
floridaobs.long = '-80:36:21.6'

kittobs = ephem.Observer()
kittobs.lat = "32:04:58.8"
kittobs.long = '-112:04:15.6'

canaryobs = ephem.Observer()
canaryobs.lat = '28:17:26.2'
canaryobs.long = '-16:33:24.1'

cerraobs = ephem.Observer()
cerraobs.lat = '-30:10:09'
cerraobs.long = '-70:48:21'

obs = {"florida": floridaobs, "cerra": cerraobs, "arizona": kittobs, "canary": canaryobs}

file = open('perijove_dat.txt','r')
out = open('perijove2.dat','w')

jup_rotation = timedelta(hours = 9.9)
#out.write("UTC, Eastern, Eastern - Rotation, Eastern - 1/2Rotation, Eastern + 1/2 Rotation, Eastern + Rotation, \
#			Mountain, Mountain - Rotation, Mountain - 1/2Rotation, Mountain + 1/2 Rotation, Mountain + Rotation, \
#			Canary, Canary - Rotation, Canary - 1/2Rotation, Canary + 1/2 Rotation, Canary + Rotation \n")
for line in file:
	dat = str.split(line)
	month, day, year = str.split(dat[2],"/")
	hour, min, sec = str.split(dat[3],":")

	utc = pytz.utc	
	date = datetime(int(year), int(month), int(day), int(hour), int(min), int(sec), 0, tzinfo = utc)
	
	florida = timezone('US/Eastern')
	cerra = timezone('Chile/Continental')
	arizona = timezone('US/Mountain')
	canary = timezone('Atlantic/Canary')
	
	tzs = {"florida": florida, "arizona": arizona, "cerra": cerra, "canary": canary}
	fmt = "%Y/%m/%d %H:%M:%S"
	
	line = "Perijove time (UTC): %s - In Florida %s "%(date.strftime(fmt), date.astimezone(florida).strftime(fmt)) + "\n"
	
	for timez in ['florida','cerra','arizona','canary']:
		tz = tzs[timez]
		observe = obs[timez]
		peri = date#.astimezone(tz)
		observe.date = peri.strftime(fmt)
		
		jup = ephem.Jupiter()
		sun = ephem.Sun()
		
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
		
		if(jupprevrise > jupprevset):	# i.e. jupiter is up right now
			if(sunprevrise > sunprevset):	# i.e. sun is up
				if(jupnextset > sunnextset):	# i.e. sun sets first
					mintime = sunnextset
					maxtime = jupnextset
				if(sunnextset > jupnextset):	# i.e. jupiter sets first
					mintime = jupnextrise
					maxtime = sunnextrise
			else:	# sun is down right now 
			#(i.e. sun set first, since jupiter is still up)
				mintime = sunprevset
				maxtime = jupnextset
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
		mintime = mintime.astimezone(tz)
		maxtime = maxtime.astimezone(tz)
		line = line + "%s: From %s to %s"%(timez,mintime.strftime(fmt), maxtime.strftime(fmt))
		if(timez != "florida"):
			mintime = mintime.astimezone(tzs['florida'])
			maxtime = maxtime.astimezone(tzs['florida'])
			line = line + " - In Florida: %s to %s"%(mintime.strftime(fmt), maxtime.strftime(fmt))
		line = line + "\n"
	line = line + "\n"
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