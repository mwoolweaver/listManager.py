#!/usr/bin/env python3
#
# Project homepage: https://github.com/mwoolweaver
# Licence: <http://unlicense.org/>
# Created by Michael Woolweaver <m.woolweaver@icloud.com>
# ================================================================================

import pandas
from lib.debug import debuginfo, debuginfoDBV, debuginfoDBVV, debuginfoDBVVV, sqlError

def fetchEntries(filesWeNeed):

    listWeNeed = []
    for fileNeeded in filesWeNeed:
        location = pandas.read_csv(fileNeeded,delimiter='\t',encoding='utf-8')
        test3 = list(location.itertuples(index=False, name=None))
        listWeNeed.append(test3)
#
    return (listWeNeed)

def fetchGroups(fileNeeded):
    
    location = pandas.read_csv(fileNeeded,delimiter='\t',encoding='utf-8')
    groups = list(location.itertuples(index=False, name=None))
#
    return (groups)
