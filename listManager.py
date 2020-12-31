#!/usr/bin/env python3
#
# Project homepage: https://github.com/mwoolweaver
# Licence: <http://unlicense.org/>
# Created by Michael Woolweaver <m.woolweaver@icloud.com>
# ================================================================================

from lib.debug import restart_pihole, sqlError, docker, notdebug, uninstall

from lib.findGravity import findGravity

from lib.fetchListToAdd import fetchEntries, fetchGroups

from lib.getFromGravity import getGravity

from lib.gravity_parser import parseGravity

from lib.add_to_gravity import addDomainGravity, checkGroup

from lib.deleteFromGravity import deleteFromGravity

groups_tsv = r'groups.tsv'

groups = fetchGroups(groups_tsv)

groupsWeNeed = groups[0]
entriesWeNeed = groups[1]

newAddition = False
newGroup = False

notdebug('Finding /etc/pihole/gravity.db')
foundGravity = findGravity()

gravityConnection = foundGravity[1]
gravity = foundGravity[2]

notdebug('We Found Gravity')

if uninstall == True:

    notdebug("Removing Entries added by script.")

    deleteFromGravity(gravity, groupsWeNeed, sqlError, uninstall)
    ifChangesMade = gravityConnection.total_changes

    if ifChangesMade > 0:
        gravityConnection.commit()
        gravityConnection.close()
        
        notdebug('')
        restart_pihole(docker)
        notdebug('')
        notdebug('Done. Happy ad-blocking :)')
        notdebug('')

        exit(0)

notdebug('Fetch Files Entries Are Sourced From domains/')

filesFound = fetchEntries(entriesWeNeed)

entriesToAddByGroup = filesFound

notdebug('Fetched Entries From Sourced Files.')

notdebug('Fetching Entries From Gravity Database')

gravityFetched = getGravity(groupsWeNeed, gravity, sqlError)

groupsInGravity = gravityFetched[3]
commentTags = gravityFetched[4]

newGroup = gravityFetched[5]

notdebug('Fetched Entries From Gravity Database')

notdebug('Parsing Entries Fetched From Database')

gravityParsed = parseGravity(filesFound, groupsWeNeed, gravityFetched)

needToAddByGroup = gravityParsed[0]
needToDeleteByGroup = gravityParsed[1]
addedByUser = gravityParsed[2]

notdebug('Parsed Entries Fetched From Database')

notdebug('Updating Gravity IF needed.')

if not addDomainGravity(gravity, sqlError, needToAddByGroup, groupsWeNeed):
    newAddition = True
    
checkGroup(gravity, sqlError, groupsInGravity, commentTags, newAddition, newGroup)

deleteFromGravity(gravity, needToDeleteByGroup, sqlError, uninstall)

ifChangesMade = gravityConnection.total_changes

if ifChangesMade > 0:
    gravityConnection.commit()

gravityConnection.close()

notdebug('All Entries Have Been Accounted For.')

if ifChangesMade > 0:
    notdebug('')
    restart_pihole(docker)

notdebug('')
notdebug('Done. Happy ad-blocking :)')
notdebug('')

exit(0)
