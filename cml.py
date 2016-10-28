import numpy as np
from datetime import datetime, timedelta
from pytz import timezone
import pytz
from astropy.time import Time
import sys

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

mintime = datetime(2016,12,28,00,00,00,tzinfo=timezone('US/Mountain'))
maxtime = datetime(2016,12,28,9,00,00,tzinfo=timezone('US/Mountain'))

cmlfmt = "%Y-%m-%dT%H:%M:%S"

mintimecml = Time(mintime.strftime(cmlfmt),format='isot', scale='utc')
maxtimecml = Time(maxtime.strftime(cmlfmt),format='isot', scale='utc')

print(cmlsys3(mintimecml.jd)[0])
print(cmlsys3(maxtimecml.jd)[0])