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

    domainsByGroupNew = []
    #domainCommentsByGroupNew = []
    # Make a list of domains in new list
    #debuginfo(filesFound)
    for groupOfEntries in filesFound:
        #print('\n\n')
        #print (groupOfEntries)
        #print('\n')
        domainsList = []
        for entry in groupOfEntries:
            domainsList.append(entry[1])

        domainsByGroupNew.append(domainsList)

    domainsByGroupOld = []

    # Make a list of domains in old gravity
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
    userAddDomainCommentList = []
    # for every entry added by user we found in the database
    userAddTempWE = []
    userAddTempBE = []
    userAddTempWR = []
    userAddTempBR = []
    if userAddGravity != [None]:
        for domainGroup in domainsByGroupNew: # for each group of new domains
            for userAddINgravity in userAddGravity:
                if userAddINgravity != None:
                    if userAddINgravity[2] in domainGroup:
                        if userAddINgravity[1] == 0:
                            userAddDomainList.append(userAddINgravity[2])  # add the domain we found to the list we created
                            userAddDomainCommentList.append(userAddINgravity[6])
                            userAddTempWE.append(userAddINgravity[2])
                        elif userAddINgravity[1] == 1:
                            userAddDomainList.append(userAddINgravity[2])  # add the domain we found to the list we created
                            userAddDomainCommentList.append(userAddINgravity[6])
                            userAddTempBE.append(userAddINgravity[2])
                        elif userAddINgravity[1] == 2:
                            userAddDomainList.append(userAddINgravity[2])  # add the domain we found to the list we created
                            userAddDomainCommentList.append(userAddINgravity[6])
                            userAddTempWR.append(userAddINgravity[2])
                        elif userAddINgravity[1] == 3:
                            userAddDomainList.append(userAddINgravity[2])  # add the domain we found to the list we created
                            userAddDomainCommentList.append(userAddINgravity[6])
                            userAddTempBR.append(userAddINgravity[2])
                        else:
                            debuginfo('Something is wrong @ parse User Add domain type.{}'.format(userAddINgravity))
                    else:
                        continue
                else:
                    print ('BREAK!!!!')
                    break
    
        userAddByType = [userAddTempWE, userAddTempBE, userAddTempWR, userAddTempBR]
        domainTypes =['exact whitelist', 'exact blacklist', 'regex whitelist', 'regex blacklist']
        debuginfo('[i] Checking Gravity for domains added by user that are in new script.')
        # Make user aware of User Added domains that are also in our script
        w = 0

        if userAddDomainList != [] and userAddDomainList != [None]:  # If list not empty
            for userAdd in userAddByType:
                debuginfo('[i] {} {} entries added by the user that would be added by script.\n'.format(len(userAdd), domainTypes[w]))
                w += 1
                if userAdd != []:
                    for userADD in userAdd:  # for every domain the user added that's also in script
                        debuginfo('    {}. {}'.format(userAdd.index(userADD) + 1, userADD))  # Show us what we found
        # If we don't find any
        else:
            #userAddDomainList.append(userAddINgravity)
            debuginfo ('    - {} domains added by the user that would be added by script.\n'.format(len(userAddDomainList))) # notify of negative result
    else:
        debuginfo ('[i] Found no domains added by the user that would be added by script.') # notify of negative result
        userAddDomainList = userAddGravity

    # Check Gravity database for domains added by script that are not in new script
    # Make a list of domains that are no longer in this script
    INgravityNOTnewList = []

    debuginfo('[i] Checking Gravity for domains previously added by script that are NOT in new script.')
    x = 0
    #debuginfoDBVV(domainsByGroupOld)
    checkEmpty = [None] * len(domainsByGroupOld)
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
    return (needToAddByGroup, needToDeleteByGroup, addedByUser)
