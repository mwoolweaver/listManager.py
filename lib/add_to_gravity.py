#!/usr/bin/env python3
#
# Project homepage: https://github.com/mwoolweaver
# Licence: <http://unlicense.org/>
# Created by Michael Woolweaver <m.woolweaver@icloud.com>
# ================================================================================

from lib.debug import debuginfo, debuginfoDBV, sqlError

from lib.check_group import checkGroup

def addDomainGravity(gravity, sqlError, needToAddByGroup, groups):

    a = 0
    check = [None] * len(needToAddByGroup)
    if check != needToAddByGroup:
        for addNew in needToAddByGroup: # For every domain in list
            group = groups[a][2]
            a += 1
            if addNew != None:
                debuginfo ('    - Adding {} entries from {}'.format(len(addNew), group)) # show it to us
                for add in addNew:
                    try:
                        debuginfo ('       - {}. {}'.format(addNew.index(add) + 1, add)) # show it to us
                        gravity.execute("INSERT OR IGNORE INTO domainlist (type, domain, enabled, comment) VALUES (?,?,?,?)",(add[0], add[1],add[2],add[3]))

                    except sqlError as error:
                        debuginfo ('Failed to add {}'.format(add[1]))
                        debuginfo (error)

            elif addNew == None:
                debuginfo ('    - No entries to add from {}'.format(group)) # show it to us
                continue
    else:
        debuginfo ('    - ALL entries have been found. No entries to add.\n')
        ALLFOUND = True
        return (ALLFOUND)