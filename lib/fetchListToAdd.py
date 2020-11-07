#!/usr/bin/env python3
#
# Project homepage: https://github.com/mwoolweaver
# Licence: <http://unlicense.org/>
# Created by Michael Woolweaver <m.woolweaver@icloud.com>
# ================================================================================

import pandas
from lib.debug import debuginfo, debuginfoDBV, debuginfoDBVV, debuginfoDBVVV, sqlError

anudeepND_whitelist_csv_file = r'../domains/anudeepND_whitelist.tsv'
anudeepND_optional_csv_file = r'../domains/anudeepND_optional.tsv'
mmotti_regex_csv_file = r'../domains/mmotti_regex.tsv'
mmotti_whitelist_csv_file = r'../domains/mmotti_whitelist.tsv'

entries_tsv = [anudeepND_whitelist_csv_file, mmotti_regex_csv_file, mmotti_whitelist_csv_file]

groups_tsv = r'../domains/groups.tsv'

def fetchEntries(filesWeNeed):

    listWeNeed = []
    for fileNeeded in filesWeNeed:

        location = pandas.read_csv(fileNeeded,delimiter='\t',encoding='utf-8')

        test3 = list(location.itertuples(index=False, name=None))
        #print(test3)
        listWeNeed.append(test3)

    #debuginfo(listWeNeed)
    
    return (listWeNeed)

def fetchGroups(fileNeeded):
    
    location = pandas.read_csv(fileNeeded,delimiter='\t',encoding='utf-8')
    test3 = list(location.itertuples(index=False, name=None))

    return (test3)

def fetchFiles(entriesNeeded, groupsNeeded):

    entriesByGroup = fetchEntries(entriesNeeded)

    groups = fetchGroups(groupsNeeded)

    print (groups)
    print('\n\n')
    
    domainsByGroup = []
    
    for groupOfEntries in entriesByGroup:
        print('\n\n')
        print (groupOfEntries)
        print('\n')
        domainsList = []
        for entry in groupOfEntries:
            domainsList.append(entry[1])

        domainsByGroup.append(domainsList)

    print(domainsByGroup)
    return (entriesByGroup, groups)

#fetchFiles(entries_tsv, groups_tsv)