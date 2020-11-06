#!/usr/bin/env python3
#
# Project homepage: https://github.com/mwoolweaver
# Licence: <http://unlicense.org/>
# Created by Michael Woolweaver <m.woolweaver@icloud.com>
# ================================================================================

from os import path
from lib.debug import debuginfo, debuginfoDBV, debuginfoDBVV, debuginfoDBVVV, sqlError

def fetchFiles(filesWeNeed):

    groupsWeNeed = []
    entriesToAddByGroup = []
    for fileNeeded in filesWeNeed:
        debuginfo('[i] Collecting existing entries from {}\n'.format(fileNeeded))
        # Reset both of these each time the loop restarts
        entriesToAdd = [] # Make a list of files
        emptyLineNumber = None

        debuginfoDBVV('    - {}\n'.format(fileNeeded))
        # Make sure we can find the file and the file isn't empty
        if path.isfile(fileNeeded) and path.getsize(fileNeeded) > 0:

            # If found, open for reading as bytes ('rb')
            with open(fileNeeded, 'rb') as file:

                # Read file, decode ('UTF-8') it and split it by ('\n')
                filesWeNeedByLine = file.read().decode('UTF-8').split('\n')
                file.close()

            # If there is more than 1 line
            debuginfoDBVVV(filesWeNeedByLine)
            if len(filesWeNeedByLine) > 1:
                
                # Used to make a list of usable lines in each file
                newLineSplitList = []

                # for each line found filesWeNeedByLine
                for newLine in filesWeNeedByLine:
                    debuginfoDBVV('    - {}'.format(newLine))
                    # make sure line is NOT empty
                    if newLine not in ['', ' ', '\r']:

                        # split at double comma to create a list
                        newL = newLine.split(',,')

                        for var in newL:
                            debuginfoDBVV('    - {}'.format(var))

                            var1 = var.lstrip() # remove leading space if there is one
                            var2 = var1.rstrip() # remove trailing space if there is one

                            # If variable is all digits
                            if var2.isdigit() == True:
                                index = newL.index(var)
                                newL[index] = int(var2)

                            elif var2.isdigit() == False:
                                index = newL.index(var)
                                newL[index] = str(var2)
                            
                            else:
                                debuginfo('Something is wrong @ double comma split.')

                        newLineSplitList.append(tuple(newL))
                        index1 = newLineSplitList.index(tuple(newL))

                        # list group should always be on the first line
                        if index1 == 0:
                            debuginfo('    - Found group {} in {}\n'.format(newLineSplitList[index1][1], fileNeeded))
                            groupsWeNeed.append(newLineSplitList[index1])
                        else:
                            debuginfoDBV('    - Found domain {}\n'.format(newLineSplitList[index1][1]))
                            entriesToAdd.append(newLineSplitList[index1])

                    # If we find an empty line
                    else:
                        emptyLineNumber = filesWeNeedByLine.index(newLine)

                        # If the empty line is the first line exit the loop.
                        # list group should always be on the first line
                        if emptyLineNumber == 0:
                            break

                if emptyLineNumber is None or emptyLineNumber != 0:
                    entriesToAddByGroup.append(entriesToAdd)
                    debuginfo("    - {} domains discovered in {}\n" .format(len(entriesToAdd), fileNeeded))

                elif emptyLineNumber == 0:
                    debuginfo ('First line can\'t be empty in {}'.format(fileNeeded))
                    debuginfo ('Trying next file.')
                else:
                    debuginfo("Something is wrong @ check empty line.")

            elif len(filesWeNeedByLine) == 0 or len(filesWeNeedByLine) == 1:
                debuginfo ("{} needs more lines in it.".format(fileNeeded))
            else:
                debuginfo("Something is wrong @ split file by line.")

        elif not path.isfile(fileNeeded):
            debuginfo ("Can not find {}.".format(fileNeeded))
        elif path.getsize(fileNeeded) == 0:
            debuginfo ("{} is empty.".format(fileNeeded))
        else:
            debuginfo("Something is wrong @ check for file.")

    return (groupsWeNeed, entriesToAddByGroup)
