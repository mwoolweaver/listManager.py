#!/usr/bin/env python3
#
# Project homepage: https://github.com/mwoolweaver
# Licence: <http://unlicense.org/>
# Created by Michael Woolweaver <m.woolweaver@icloud.com>
# ================================================================================

from lib.debug import debuginfo, debuginfoDBV, debuginfoDBVV, debuginfoDBVVV, sqlError

def getUserAddGravity(groups, gravity, sqlError, commentTags):

    # check database for user added exact whitelisted domains
    debuginfo ('[i] Collecting user added entries from gravity.')
    userAddFound = []
    # Check Gravity database for exact whitelisted domains added by user, if NOT '%qjz9zk%' OR isnull it is NOT from this script
    fetchUserAdd = ""
    if len(groups) == 4:
        fetchUserAdd = "SELECT type, domain, enabled, comment FROM domainlist WHERE comment isnull OR comment NOT LIKE '%{}%' and comment NOT LIKE '%{}%' and comment NOT LIKE '%{}%' and comment NOT LIKE '%{}%'".format(commentTags[0], commentTags[1], commentTags[2], commentTags[3])
    elif len(groups) == 3:
        fetchUserAdd = "SELECT * FROM domainlist WHERE comment isnull OR comment NOT LIKE '%{}%' and comment NOT LIKE '%{}%' and comment NOT LIKE '%{}%'".format(commentTags[0], commentTags[1], commentTags[2])
    elif len(groups) == 2:
        fetchUserAdd = "SELECT * FROM domainlist WHERE comment NOT LIKE '%{}%' and comment NOT LIKE '%{}%'".format(commentTags[0], commentTags[1])
    elif len(groups) == 1:
        fetchUserAdd = "SELECT * FROM domainlist WHERE comment NOT LIKE '%{}%'".format(commentTags[0])
    
    try:
        userAdd = gravity.execute(fetchUserAdd)
        userAddFetched = userAdd.fetchall()
        debuginfo('    - Found {} user added entries in gravity\n'.format(len(userAddFetched)))
        userAddFound = userAddFetched

    except sqlError as error:
        debuginfo (error)
    
    return (userAddFound)

def getScriptAddGravity(groups, gravity, sqlError, commentTags):

    entriesFoundByGroup = []
    
    for comment in commentTags:
        groupIndex = commentTags.index(comment)
        try:
            debuginfo('[i] Collecting existing entries for {} in Gravity.'.format(groups[groupIndex][0][2]))
            entriesFound = gravity.execute("SELECT * FROM domainlist WHERE comment LIKE '%{}%'".format(comment))
            entriesFetched = entriesFound.fetchall()
            if entriesFetched != []:
                debuginfo('    - Found {} domains from {}\n'.format(len(entriesFetched), groups[groupIndex][0][2]))
                entriesFoundByGroup.append(entriesFetched)

            elif entriesFetched == []:
                debuginfo('    - Found 0 domains from {}\n'.format(groups[groupIndex][0][2]))
                entriesFoundByGroup.append(None)

            else:
                debuginfo("Something is wrong @ fetching domain by group_id from script. {}\n".format(entriesFetched))
        
        except sqlError as error:
            debuginfo("Something is wrong @ fetching domain by group_id from script. \nError: {}\n".format(error))

    return (entriesFoundByGroup)

def getGroups(groups, gravity, sqlError):

    groupNeedAdd = []
    groupIDList = []
    commentTag = []
    newGroup = False
    test = []
    debuginfo('[i] Checking Gravity for groups we need')
    for group in groups:
        gravityGroups = gravity.execute("SELECT * FROM 'group' WHERE name LIKE '{}'".format(group[1]))
        groupsInGravity = gravityGroups.fetchall()
        test = groupsInGravity
        grouptoadd = group[0:3]
        
        if groupsInGravity == [] or test[0][2] not in grouptoadd[1] :
                debuginfo('NEDD TO ADD {} !!!!!!!!'.format(grouptoadd))
                try:
                    gravity.execute("INSERT OR IGNORE INTO 'group' (enabled, name, description) VALUES {}".format(grouptoadd))
                    groupNeedAdd.append(grouptoadd)
                    commentTag.append(group[3])
                    newGroup = True
                except sqlError as error:
                    debuginfo('Something wrong @ INSERT group')
                    debuginfo(error)
                    groupNeedAdd.append(grouptoadd)

        else:
            debuginfo('    - Found group_id {} for {}'.format(groupsInGravity[0][0], group[1]))
            debuginfoDBV('DO NOT NEDD TO ADD {} !!!!!!!!'.format(group[1]))
            commentTag.append(group[3])
            groupIDList.append(groupsInGravity)
            continue

    for checkGroup in groupNeedAdd:
        gravityGroupsCheck = gravity.execute("SELECT * FROM 'group' WHERE name LIKE '{}'".format(checkGroup[1]))
        groupsChecked = gravityGroupsCheck.fetchall()
        debuginfo('FOUND IT!!!! {} group_id = {}'.format(checkGroup[1], checkGroup[1]))
        debuginfo(groupsChecked)
        groupIDList.append(groupsChecked)

    return (groupIDList, groupIDList, commentTag, newGroup)

def getGravity(groups, gravity, sqlError):

    gotGroups = getGroups(groups, gravity, sqlError)

    groupsToAdd = gotGroups[0]

    groupsInGravity = gotGroups[1]
    commentTags = gotGroups[2]

    newGroup = gotGroups[3]

    debuginfo('    - ALL groups accounted for.\n')

    scriptAddGravity = getScriptAddGravity(groupsInGravity, gravity, sqlError, commentTags)

    userAddGravity = getUserAddGravity(groupsToAdd, gravity, sqlError, commentTags)
#                0                  1             2              3              4           5
    return (scriptAddGravity, userAddGravity, groupsToAdd, groupsInGravity, commentTags, newGroup)
