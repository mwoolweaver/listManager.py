#!/usr/bin/env python3
#
# Project homepage: https://github.com/mwoolweaver
# Licence: <http://unlicense.org/>
# Created by Michael Woolweaver <m.woolweaver@icloud.com>
# ================================================================================

from lib.debug import debuginfo, debuginfoDBV, restart_pihole, sqlError, docker, notdebug, uninstall

from lib.findGravity import findGravity

from lib.fetchListToAdd import fetchEntries, fetchGroups

from lib.getFromGravity import getGravity

from lib.gravity_parser import parseGravity

from lib.add_to_gravity import addDomainGravity, checkGroup

from lib.deleteFromGravity import deleteFromGravity

anudeepND_whitelist_csv_file = r'domains/anudeepND_whitelist.tsv'
anudeepND_optional_csv_file = r'domains/anudeepND_optional.tsv'
mmotti_regex_csv_file = r'domains/mmotti_regex.tsv'
mmotti_whitelist_csv_file = r'domains/mmotti_whitelist.tsv'

entriesWeNeed = [anudeepND_whitelist_csv_file, mmotti_regex_csv_file, mmotti_whitelist_csv_file]

groups_tsv = r'groups.tsv'

newAddition = False
newGroup = False

notdebug('Finding /etc/pihole/gravity.db')
foundGravity = findGravity()

gravityConnection = foundGravity[1]
gravity = foundGravity[2]

notdebug('We Found Gravity')

notdebug('Fetch Files Entries Are Sourced From')

filesFound = fetchEntries(entriesWeNeed)

groupsWeNeed = fetchGroups(groups_tsv)

entriesToAddByGroup = filesFound

notdebug('Fetched Files Entries Are Sourced From')

if uninstall == True:
    deleteFromGravity(gravity, groupsWeNeed, sqlError, uninstall)
    ifChangesMade = gravityConnection.total_changes

    if ifChangesMade > 0:
        gravityConnection.commit()

        gravityConnection.close()

        exit(0)

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