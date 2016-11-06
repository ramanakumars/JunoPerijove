import numpy as np

importfile = open("perijove_dat.txt","r")

outfile = open("perilist.dat","w")

for line in importfile:
	dat = str.split(line)
	date = dat[2]
	time = dat[3]
	cml = dat[21]
	outdat = "%s %s %.2f\n"%(date, time, np.float(cml))
	outfile.write(outdat)
	

outfile.close()
importfile.close()