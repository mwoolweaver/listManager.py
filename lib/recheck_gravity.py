#!/usr/bin/env python3
#
# Project homepage: https://github.com/mwoolweaver
# Licence: <http://unlicense.org/>
# Created by Michael Woolweaver <m.woolweaver@icloud.com>
# ================================================================================


def recheckGravity(gravity, INnewNOTgravityList, sqlError):

    print ('')
    print ('[i] Checking Gravity for newly added domains.')
    print ('')
    # Re-Check Gravity database for domains added by script after we update it
    try:
        gravityScript_after = gravity.execute(" SELECT * FROM domainlist WHERE type = 0 AND comment LIKE '%qjz9zk%' ")
        # fetch all matching entries which will create a tuple for us
        gravScriptAfterTUP = gravityScript_after.fetchall()
    
    except sqlError as error:
        print ("Failed to fetch domains to be checked after add.")
        print (error)

    gravScriptAfterList = [] # Make a list of domains so we can make sure all missing domains are in gravity
    gravScriptAfterListDI = []

    for gravScriptAfterDomain in gravScriptAfterTUP:
        gravScriptAfterList.append(gravScriptAfterDomain[2]) # only get the domain
        gravScriptAfterListDI.append(gravScriptAfterDomain[0]) # get unique domainlist_id

    weFOUNDitList = [] # Make list of missing domains we found

    for weFOUNDit in INnewNOTgravityList:
        if weFOUNDit in gravScriptAfterList:
            weFOUNDitList.append(weFOUNDit)
            print ('    - Found  {}. {} '.format(INnewNOTgravityList.index(weFOUNDit) + 1, weFOUNDit))

    return (weFOUNDitList, gravScriptAfterListDI)
    
