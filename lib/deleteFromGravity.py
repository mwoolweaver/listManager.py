#!/usr/bin/env python3
#
# Project homepage: https://github.com/mwoolweaver
# Licence: <http://unlicense.org/>
# Created by Michael Woolweaver <m.woolweaver@icloud.com>
# ================================================================================

from lib.debug import debuginfo, debuginfoDBV, sqlError


def deleteFromGravity(gravity, needToDeleteList, sqlError, uninstall):

    check = [None] * len(needToDeleteList)

    if check != needToDeleteList:

        if uninstall == False:
            print ('[i] {} domain(s) added previously by script that are not in new script.\n')

            for needTOdelete in needToDeleteList: # For every domain in gravity we need to 
            
                debuginfo('    - deleting {}. {}'.format(needToDeleteList.index(needTOdelete) + 1, needTOdelete[0][2])) # show us what needs to be deleted
                sql_delete_domain = " DELETE FROM domainlist WHERE id = {} ".format(needTOdelete[0][0]) # Make our sql statement
                print(sql_delete_domain)
                try:
                    gravity.executescript(sql_delete_domain) # Delete domain from gravity

                except sqlError as error:
                    print ('Failed to delete {}'.format(needTOdelete[2]))
                    print (error)
                    exit(1)

            return (len(needToDeleteList))

        else:
            debuginfo('Uninstall')
            comments = []
            names = []
            for group in needToDeleteList:
                names.append(group[1])
                comments.append((group[3]))

            x = len(needToDeleteList) - 1
            while x >= 0:

                #debuginfo('    - deleting {}. {}'.format(needToDeleteList.index(needTOdelete) + 1, needTOdelete[0][2])) # show us what needs to be deleted
                sql_delete_domain = " DELETE FROM domainlist WHERE comment LIKE '%{}%' ".format(comments[x]) # Make our sql statement
                sql_delete_group = " DELETE FROM 'group' WHERE name LIKE '{}' ".format(names[x])
                try:
                    debuginfo(sql_delete_domain)
                    gravity.executescript(sql_delete_domain) # Delete domain from gravity

                except sqlError as error:
                    print ('Failed to delete {}'.format(sql_delete_domain))
                    print (error)
                    exit(1)
                
                try:
                    debuginfo(sql_delete_group)
                    gravity.executescript(sql_delete_group)

                except sqlError as error:
                    print ('Failed to delete {}'.format(sql_delete_group))
                    print (error)
                    exit(1)

                x -= 1

            return (len(needToDeleteList))



    else:
        return (debuginfo('Nothing Needs Deleting'))