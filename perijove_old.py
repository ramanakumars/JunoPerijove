import numpy as np
from datetime import datetime, timedelta
from pytz import timezone
import pytz

file = open('perijove_dat.txt','r')
out = open('perijove.csv','w')

jup_rotation = timedelta(hours = 9.9)
out.write("UTC, Eastern, Eastern - Rotation, Eastern - 1/2Rotation, Eastern + 1/2 Rotation, Eastern + Rotation, \
			Mountain, Mountain - Rotation, Mountain - 1/2Rotation, Mountain + 1/2 Rotation, Mountain + Rotation, \
			Canary, Canary - Rotation, Canary - 1/2Rotation, Canary + 1/2 Rotation, Canary + Rotation \n")
for line in file:
	dat = str.split(line)
	month, day, year = str.split(dat[2],"/")
	hour, min, sec = str.split(dat[3],":")

	utc = pytz.utc	
	date = datetime(int(year), int(month), int(day), int(hour), int(min), int(sec), 0, tzinfo = utc)
	
	eastern = timezone('US/Eastern')
	arizona = timezone('US/Mountain')
	canary = timezone('Etc/GMT+1')
	
	tzs = {"eastern": eastern, "arizona": arizona, "canary": canary}
	
	localdt = date.astimezone(tzs["eastern"])
	minusjuprot = localdt - jup_rotation
	minushalfjuprot = localdt - 0.5*jup_rotation
	plusjuprot = localdt + jup_rotation
	plushalfjuprot = localdt + 0.5*jup_rotation
	
	fmt = "%Y-%m-%d %H:%M:%S"
	
	line = date.strftime(fmt) + ", "
	
	for timez in ['eastern','arizona','canary']:
		tz = tzs[timez]
		localdttz = date.astimezone(tz)
		minusjuprottz = localdttz - jup_rotation
		minushalfjuprottz = localdttz- 0.5*jup_rotation
		plusjuprottz = localdttz + jup_rotation
		plushalfjuprottz = localdttz + 0.5*jup_rotation
		line = line + "%s, %s, %s, %s, %s, "%(localdttz.strftime(fmt), minushalfjuprottz.strftime(fmt), minusjuprottz.strftime(fmt), plushalfjuprottz.strftime(fmt), plusjuprottz.strftime(fmt))
	line = line + "\n"
	out.write(line)
	
print("Done")
	
