#! /usr/bin/env python3

# ---------------------------------------------------------------------------- #
# Wiki micro query frontend and interpreter.                                   #
# Version 0.9                                                                  #
#                                                                              #
# by Magnetic-Fox                                                              #
#                                                                              #
# String table for a program.                                                  #
#                                                                              #
# Copyright (c) 2020-2021 Bartłomiej "Magnetic-Fox" Węgrzyn                    #
# ---------------------------------------------------------------------------- #

noPageString=            "This page does not exists."

getErrorString=          "Article get error. " \
                         "Check selected Wiki or your internet connection."
                 
interpreterText=         "Wiki> "

currentWikiIs=           "\nCurrent Wiki is: "

interpreterStart=        "Wiki Interpreter 0.9\n(c)2020-2021 Magnetic-Fox!\n" \
                         +currentWikiIs
        
interpreterInfo=         "\n\nType : and command to configure this " \
                         "interpreter.\n"
        
newWikiName=             "\nNew Wiki name: "
newWikiURL=              "New Wiki URL address: "
newWikiAdded=            "New Wiki added to list of known Wikis.\n"

add_IncorrectAddress=    "Incorrect address of new Wiki - not added.\n"
add_EmptyURL=            "Empty string - Wiki not added.\n"

changeWiki=              "\nChange Wiki to (URL address): "
wikiChanged=             "Wiki changed to: "

change_IncorrectAddress= "Incorrect address of Wiki - not changed.\n"
change_EmptyURL=         "Empty string - Wiki not changed.\n"

knownWikisAre=           "\nKnown Wikis are:\n"

removeFromKnown=         "\nRemove from known Wikis (name): "

notKnownStart=           "Wiki \""

remove_notKnownEnd=      "\" not known - not removed.\n"
remove_removed=          "Removed Wiki: \""
remove_emptyName=        "Empty string - Wiki not removed.\n"

changeCurrent_name=      "\nChange wiki to (name): "
changeCurrent_changed=   "Wiki changed to: "
changeCurrent_notKnown=  "\" not known - not changed.\n"
changeCurrent_emptyName= "Empty string - Wiki not changed.\n"

infoString=              "\nWiki micro query frontend and interpreter\n" \
                         "(c)2020-2021 Magnetic-Fox!\n"
                         
helpString=              "\nHelp\n\nA - Add Wiki to known Wikis\n" \
                         "C - Temporarily changes Wiki's URL\n" \
                         "D - Display current Wiki\n" \
                         "E - Save temporary Wiki to known Wikis\n" \
                         "K - List known Wikis\n" \
                         "R - Remove Wiki from known Wikis\n" \
                         "S - Change to the known Wiki\n" \
                         "I - Show program information\n" \
                         "? - Display this help\n" \
                         "Q - Quit the interpreter\n"

APIUrlString=            "API URL: "

ac_nonStandardAPI=       "Is this Wiki uses non-standard API? (y/n) "

temp_NotInUse=           "No temporary Wiki to save.\n"
