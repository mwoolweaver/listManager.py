#!/usr/bin/env python3
#
# Project homepage: https://github.com/mwoolweaver
# Licence: <http://unlicense.org/>
# Created by Michael Woolweaver <m.woolweaver@icloud.com>
# ================================================================================

from os import path
from sqlite3 import connect
from sqlite3 import Error as sqlError

from lib.debug import debuginfo, debuginfoDBV, sqlError, args

def findGravity():
    
    # IF custom directory
    if args.dir:
        pihole_location = args.dir # set custom directory
    else:
        pihole_location = r'/etc/pihole' # set default pihole directory

    # Check for pihole path exsists
    if path.isdir(pihole_location):

        debuginfo('[i] Pi-hole path exists. - {}\n'.format(pihole_location))
        gravity_db_location = path.join(pihole_location, r'gravity.db')

        if path.isfile(gravity_db_location) and path.getsize(gravity_db_location) > 100:

            debuginfo('[i] Pi-Hole Gravity database found. - {}\n'.format(gravity_db_location))

            # see ---> https://stackoverflow.com/a/15355790
            # validate SQLite header
            with open(gravity_db_location, 'rb') as db:
                header = db.read(100)
            debuginfo('[i] Checking Gravity database header. - {}\n'.format(header[:16]))
            if header[:16] == b'SQLite format 3\x00':

                try:
                    gravityConnection = connect(gravity_db_location)
                    gravity = gravityConnection.cursor()
                    
                    debuginfo('[i] Connected to Gravity. - {}\n'.format(gravity_db_location))
                     #      0           1              2
                    return (True, gravityConnection, gravity)

                except sqlError as error:
                    debuginfo("Failed to connect to Gravity. Error: {}".format(error))
                    return(exit(1))
            
            elif header[:16] != b'SQLite format 3\x00':
                debuginfo('Something is wrong @ reading {}'.format(gravity_db_location))
                return(exit(1))
        
        elif path.isfile(gravity_db_location) == False:
            debuginfo ("Can not find {}.".format(gravity_db_location))
            return (exit(1))

        elif path.getsize(gravity_db_location) == 0:
            debuginfo ("{} is empty.".format(gravity_db_location))
            return (exit(1))

        else:
            debuginfo("Something is wrong @ check for file.")
            return (exit(1))

    elif path.isdir(pihole_location) == False:
        debuginfo ("Can not find {}.".format(pihole_location))
        return (exit(1))

    else:
        debuginfo("Something is wrong @ check for file.")
        return (exit(1))
