#!/usr/bin/env python3
#
# Project homepage: https://github.com/mwoolweaver
# Licence: <http://unlicense.org/>
# Created by Michael Woolweaver <m.woolweaver@icloud.com>
# ================================================================================

import os
from inspect import getframeinfo, stack
from sqlite3 import Error as sqlError
from subprocess import call
import argparse

os.system('clear')
print('use -h or --help for more info')
# Used to verify user defined Pi-hole directory string
def dir_path(string):
    try:
        os.path.isdir(string)
        return string
    except NotADirectoryError as error:
        debuginfo('Something Wrong @ dir_path. {}'.format(error))

docker = False
# setup arg parser
parser = argparse.ArgumentParser()
# define acceptable args
parser.add_argument("-u", "--uninstall", action='store_true', help="optional: Used for uninstalling script added entries.")
parser.add_argument("-db", "--debug", action='store_true', help="optional: Used for debug when script fails.")
parser.add_argument("-dbv", "--debugX2", action='store_true', help="optional: Used for debug when script fails and -db doesnt show enough.")
parser.add_argument("-dbvv", "--debugX3", action='store_true', help="optional: Used for debug when script fails and -dbv doesnt show enough.")
parser.add_argument("-dbvvv", "--debugX4", action='store_true', help="optional: Used for debug when script fails and -dbvv doesnt show enough.")
parser.add_argument("-D", "--docker",  action='store_true', help="optional: set if you're using Pi-hole in docker environment.")
parser.add_argument("-d", "--dir", type=dir_path, help="optional: Pi-hole etc directory.")
#get args 
args = parser.parse_args()

if args.uninstall: 
    uninstall = True
else:
    uninstall = False

if args.debug: 
    ifDebug = True
else:
    ifDebug = False

if args.debugX2: 
    ifDebug = True
    ifDebugx2 = True
else:
    ifDebugx2 = False

if args.debugX3: 
    ifDebug = True
    ifDebugx2 = True
    ifDebugx3 = True
else:
    ifDebugx3 = False

if args.debugX4: 
    ifDebug = True
    ifDebugx2 = True
    ifDebugx3 = True
    ifDebugx4 = True
else:
    ifDebugx4 = False

def restart_pihole(docker):
    if docker is True:
        debuginfo('Restarting Pi-hole via Docker')
        call("docker exec -it pihole pihole restartdns reload", shell=True)

    else:
        debuginfo('Restarting Pi-hole')
        call(['pihole', 'restartdns', 'reload'])

# Credit ---> https://stackoverflow.com/a/24439444
def debuginfo(message):
    if ifDebug == True:
        caller = getframeinfo(stack()[1][0])
        print ("{}:{}:{} - {}".format(caller.filename, caller.lineno, caller.function, message))

    else:
        return()

def debuginfoDBV(message):
    if ifDebug == True and ifDebugx2 == True:
        caller = getframeinfo(stack()[1][0])
        print ("{}:{}:{} - {}".format(caller.filename, caller.lineno, caller.function, message))

    else:
        return()

def debuginfoDBVV(message):
    if ifDebug == True and ifDebugx2 == True and ifDebugx3 == True:
        caller = getframeinfo(stack()[1][0])
        print ("{}:{}:{} - {}".format(caller.filename, caller.lineno, caller.function, message))

    else:
        return()

def debuginfoDBVVV(message):
    if ifDebug == True and ifDebugx2 == True and ifDebugx3 == True and ifDebugx4 == True:
        caller = getframeinfo(stack()[1][0])
        print ("{}:{}:{} - {}".format(caller.filename, caller.lineno, caller.function, message))

    else:
        return()


def notdebug(message):
    if ifDebug == True or ifDebugx2 == True and ifDebugx3 == True and ifDebugx4 == True:
        return()
    else:
        return(print (message))