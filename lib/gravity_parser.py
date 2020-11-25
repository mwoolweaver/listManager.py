#!/usr/bin/env python3
#
# Project homepage: https://github.com/mwoolweaver
# Licence: <http://unlicense.org/>
# Created by Michael Woolweaver <m.woolweaver@icloud.com>
# ================================================================================

from lib.debug import debuginfo, debuginfoDBV, debuginfoDBVV, debuginfoDBVVV, sqlError

def parseGravity(filesFound, groups, gravityFetched):

    needToDeleteByGroup = []
    needToAddByGroup = []

    scriptAddGravityByGroup = gravityFetched[0]
    userAddGravity = gravityFetched[1]

    # Make a list of new entries
    domainsByGroupNew = []
    for groupOfEntries in filesFound:
        domainsList = []
        for entry in groupOfEntries:
            domainsList.append(entry[1])

        domainsByGroupNew.append(domainsList)

    # Make a list of domains in old gravity
    domainsByGroupOld = []
    for groupEntryOld in scriptAddGravityByGroup: # for each group
        if groupEntryOld != None:
            toRemoveList = []
            toRemoveCommentList = []
            for entryOld in groupEntryOld: # for each entry
                debuginfoDBVVV('    - {}'.format(entryOld)) 
                toRemoveList.append(entryOld[2])
                toRemoveCommentList.append(entryOld[6])

        else:
            domainsByGroupOld.append(None)
            continue

        domainsByGroupOld.append(toRemoveList)
    
    # Make a list of domains added by user that are also in script
    userAddDomainList = []
    userAddTempWE = []
    userAddTempBE = []
    userAddTempWR = []
    userAddTempBR = []
    # Make sure we found some User added domains
    if userAddGravity != [None]:
        # for every entry added by user we found in the database
        for domainGroup in domainsByGroupNew:
            for userAddINgravity in userAddGravity:
                if userAddINgravity != None:
                    if userAddINgravity[2] in domainGroup:
                        # Sort user added domains by type. see here ---> https://docs.pi-hole.net/database/gravity/#domain-tables-domainlist
                        if userAddINgravity[1] == 0:    # 0 = exact whitelist
                            userAddDomainList.append(userAddINgravity[2])  # add the domain we found to the list we created
                            userAddTempWE.append(userAddINgravity[2])
                        elif userAddINgravity[1] == 1:  # 1 = exact blacklist
                            userAddDomainList.append(userAddINgravity[2])  # add the domain we found to the list we created
                            userAddTempBE.append(userAddINgravity[2])
                        elif userAddINgravity[1] == 2: # 2 = regex whitelist
                            userAddDomainList.append(userAddINgravity[2])  # add the domain we found to the list we created
                            userAddTempWR.append(userAddINgravity[2])
                        elif userAddINgravity[1] == 3: # 3 = regex blacklist
                            userAddDomainList.append(userAddINgravity[2])  # add the domain we found to the list we created
                            userAddTempBR.append(userAddINgravity[2])
                        else:
                            # technically we should never get here but just in case we do tell us when it heppens
                            debuginfo('Something is wrong @ parse User Add domain type.{}'.format(userAddINgravity))
                    else:
                        continue
                else:
                    print ('BREAK!!!!')
                    break
    
        userAddByType = [userAddTempWE, userAddTempBE, userAddTempWR, userAddTempBR]
        domainTypes =['exact whitelist', 'exact blacklist', 'regex whitelist', 'regex blacklist']
        # Make us aware of User Added domains that are also in our script
        w = 0
        if userAddDomainList != [] and userAddDomainList != [None]:  # If list not empty
            debuginfo('[i] Checking Gravity for domains added by user that are in new script.')
            for userAdd in userAddByType:
                debuginfo('[i] {} {} entries added by the user that would be added by script.\n'.format(len(userAdd), domainTypes[w]))
                w += 1
                if userAdd != []:
                    for userADD in userAdd:  # for every domain the user added that's also in script
                        debuginfo('    {}. {}'.format(userAdd.index(userADD) + 1, userADD))  # Show us what we found
        # If we don't find any
        else:
            debuginfo ('    - {} domains added by the user that would be added by script.\n'.format(len(userAddDomainList))) # notify of negative result
    else:
        userAddDomainList = userAddGravity

    # Check Gravity database for domains added by script that are not in new script
    # Make a list of domains that are no longer in this script
    INgravityNOTnewList = []

    debuginfo('[i] Checking Gravity for domains previously added by script that are NOT in new script.')
    x = 0
    #debuginfoDBVV(domainsByGroupOld)
    checkEmpty = [None] * len(domainsByGroupOld) # create a list of None values with as many values as there are groups
    # If we found NO domains previously added by script we know we need to add them all so skip to after else:
    if domainsByGroupOld != checkEmpty:
        for newDomainGroup in domainsByGroupNew: # for every domain in new script.
            groupNeed = groups[x]
            domainGroupIndex = domainsByGroupNew.index(newDomainGroup)
            x += 1
            for groupEntryOld in domainsByGroupOld: # for every domain previously added by script
                INgravityNOTnew = []
                needToDelete = []
                if groupEntryOld != None:
                    if domainsByGroupNew.index(newDomainGroup) == domainsByGroupOld.index(groupEntryOld):
                        for oldEntry in groupEntryOld:
                            debuginfoDBVV('    - Checking {}'.format(oldEntry))
                            entryIndex = groupEntryOld.index(oldEntry)
                            if oldEntry not in newDomainGroup and oldEntry not in userAddDomainList:
                                debuginfoDBVV('    - Found old entry {}'.format(oldEntry))    
                                INgravityNOTnew.append(oldEntry)
                                needToDelete.append(scriptAddGravityByGroup[domainGroupIndex][entryIndex])
                            else:
                                continue
                    else:
                        continue
                else:
                    needToDelete.append(None)
                    INgravityNOTnewList.append(None)
                    continue
                
                if INgravityNOTnew != [] and needToDelete != []:
                    INgravityNOTnewList.append(INgravityNOTnew)
                    needToDeleteByGroup.append(needToDelete)
                    debuginfo('    - Found {} old entries from {}\n'.format(len(INgravityNOTnew), groupNeed[1]))

                    for oldDomain in INgravityNOTnew:
                        debuginfo('    {}. {}'.format(INgravityNOTnew.index(oldDomain) + 1, oldDomain))  # Show us what we found

                else:
                    INgravityNOTnewList.append(None)
                    debuginfo('    - Found no old entries added from {}.\n'.format(groupNeed[1])) # notify of negative result
                    continue
        
        # Check Gravity database for new domains to be added by script
        debuginfo('[i] Checking for domains not in Gravity.')
        for NEWGROUP in domainsByGroupNew:
            domainGroupIndex = domainsByGroupNew.index(NEWGROUP)
            needToAdd = []
            for new in NEWGROUP:
                if domainsByGroupOld[domainGroupIndex] != None:
                    
                    if new in domainsByGroupOld[domainGroupIndex] or new in userAddDomainList:
                        continue

                    else:
                        debuginfo('    - {} . {}'.format(NEWGROUP.index(new)+1, new))
                        newENTRYIndex = NEWGROUP.index(new)
                        needToAdd.append(filesFound[domainGroupIndex][newENTRYIndex])
                        continue

                else:
                    debuginfoDBV('')
                    debuginfoDBV('{} - {}'.format(new, NEWGROUP.index(new)))
                    newENTRYIndex = NEWGROUP.index(new)
                    debuginfoDBV(filesFound[domainGroupIndex][newENTRYIndex])
                    needToAdd = []
                    continue

            if needToAdd != []:
                needToAddByGroup.append(needToAdd)
            elif needToAdd == []:
                needToAddByGroup.append(None)
    # We found NO domains previously added by script so add all
    else:
        INgravityNOTnewList.append(None)
        needToDeleteByGroup.append(None)
        debuginfo('[i] Found no entries previously added by script that are NOT in new script.') # notify of negative result
        for NEWGROUP in domainsByGroupNew:
            domainGroupIndex = domainsByGroupNew.index(NEWGROUP)
            needToAdd = []
            for new in NEWGROUP:
                newENTRYIndex = NEWGROUP.index(new)
                needToAdd.append(filesFound[domainGroupIndex][newENTRYIndex])
            
            if needToAdd != []:
                needToAddByGroup.append(needToAdd)
    debuginfoDBVV(needToAddByGroup)
    addedByUser = userAddDomainList
#
    return (needToAddByGroup, needToDeleteByGroup, addedByUser)
