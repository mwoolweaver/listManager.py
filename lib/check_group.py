#!/usr/bin/env python3
#
# Project homepage: https://github.com/mwoolweaver
# Licence: <http://unlicense.org/>
# Created by Michael Woolweaver <m.woolweaver@icloud.com>
# ================================================================================

from lib.debug import debuginfo, debuginfoDBV, sqlError

def checkGroupIFCorrect(gravity, sqlError, groups, commentTags):

    needGroupList = []
    x = 0
    ALLHAVE = False
    debuginfo('[i] Checking for group_id on entries added by script!!!!!')
    for group in groups: # For every group in list
        
        entriesFound = gravity.execute("SELECT * FROM domainlist WHERE comment LIKE '%{}%' AND id NOT IN (SELECT domainlist_id FROM domainlist_by_group WHERE group_id LIKE {})".format(commentTags[x], group[0][0]))
        needGroup = entriesFound.fetchall()

        debuginfo("    - Found {} entries from {} that need group_id = {}".format(len(needGroup), group[0][2], group[0][0]))
        debuginfoDBV('      {}'.format(group[0][2]))
        debuginfoDBV('      {}\n'.format(commentTags[x]))
        x+=1

        if needGroup != []:
            needGroupList.append(needGroup)
        elif needGroup == []:
            needGroup = None
            needGroupList.append(needGroup)

    #print (needGroupList)
    check = [None] * len(needGroupList)
    #print (check)
    if check == needGroupList:
        debuginfo('[i] No entries need group_id updated\n')
        ALLHAVE = True
        return(needGroupList, ALLHAVE)

    else:
        return(needGroupList, ALLHAVE)

def addGroupToDomain(gravity, sqlError, needGroups, groups, newDomains, newGroup):

    ALLHAVE = needGroups[1]
    needGroup = needGroups[0]
    

    if ALLHAVE == False:
        debuginfo('Adding group_id to entries')
        for group in groups:
            groupsIndex = groups.index(group)
            groupID = group[0]
            for groupNeeded in needGroup:

                needGroupIndex = needGroup.index(groupNeeded)

                if groupNeeded != None and groupsIndex == needGroupIndex:
                    for domain in groupNeeded:

                        debuginfo(domain[0:3])
                        debuginfo(groupID)
                        if newDomains == True:
                            gravity.executescript("UPDATE domainlist_by_group SET group_id={} WHERE domainlist_id = {} ".format(group[0][0], domain[0]))
                            debuginfo("UPDATE domainlist_by_group SET group_id={} WHERE domainlist_id = {} ".format(group[0][0], domain[0]))
                            continue
                        elif newGroup == True:
                            gravity.executescript("INSERT INTO domainlist_by_group (domainlist_id, group_id) VALUES ({},{}) ".format(domain[0], group[0][0]))
                            debuginfo("updating group_id to {} for {}".format(group[0][0], domain[2]))
                            continue
                        elif ALLHAVE == False:
                            gravity.executescript("UPDATE domainlist_by_group SET group_id={} WHERE domainlist_id = {} ".format(group[0][0], domain[0]))
                            debuginfo("INSERT INTO domainlist_by_group (domainlist_id, group_id) VALUES ({},{})".format(domain[0], group[0][0]))
                            continue

def checkGroup(gravity, sqlError, ourGroupsInGravity, commentTags, newAddition, newGroup):

    needGroup = checkGroupIFCorrect(gravity, sqlError, ourGroupsInGravity, commentTags)
    
    addGroupToDomain(gravity, sqlError, needGroup, ourGroupsInGravity, newAddition, newGroup)