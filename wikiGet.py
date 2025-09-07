#!/usr/bin/env python3

# ---------------------------------------------------------------------------- #
# Wiki micro query frontend and interpreter.                                   #
# Version 0.9                                                                  #
#                                                                              #
# by Magnetic-Fox                                                              #
#                                                                              #
# Main program code.                                                           #
#                                                                              #
# Copyright (c) 2020-2021 Bartłomiej "Magnetic-Fox" Węgrzyn                    #
# ---------------------------------------------------------------------------- #

# Edited by Magnetic-Fox, 07.09.2025

# ---------------------------------------------------------------------------- #
# Import section                                                               #
# ---------------------------------------------------------------------------- #

# Import necessary libraries
import requests
import json
import sys

# Import string table
from wiki_stringtable import *

# Default known Wikis
knownWikis = {
	'Wikipedia PL': ['https://pl.wikipedia.org/',True,''],
	'Wikipedia EN': ['https://en.wikipedia.org/',True,''],
	'WikiFur PL': ['http://pl.wikifur.com/',True,''],
	'WikiFur EN': ['http://en.wikifur.com/',True,''],
	'Nonsensopedia PL': ['http://nonsa.pl/',False,'api.php']
}

# Default selected Wiki
wiki = knownWikis["Wikipedia EN"][0]
useStandardAPIUrl = knownWikis["Wikipedia EN"][1]
nonStandardAPIUrl = knownWikis["Wikipedia EN"][2]

# Configuration file name
configFileName = "WikiConfig.json"

# ---------------------------------------------------------------------------- #
# Main functions and procedures                                                #
# ---------------------------------------------------------------------------- #

# Gets data using standard Wiki API. Return in JSON.
def getWikiData(wikiURL, title, useStandardAPIUrl = True, nonStandardAPIUrl = ""):
	if useStandardAPIUrl:
		APIUrl="w/api.php"
	else:
		APIUrl=nonStandardAPIUrl

	url=wikiURL+APIUrl+"?action=query&prop=extracts&explaintext=true&format=json&indexpageids=true&redirects=true&titles="+title

	try:
		response=requests.get(url)
	except:
		raise getError

	return response.json()

# Lists pages available throught query.
def listPages(wikiDataResponse):
	return wikiDataResponse["query"]["pageids"]

# Determines if the requested page is missing or query is invalid.
def pageMissing(wikiDataResponse):
	return ('-1' in listPages(wikiDataResponse)) and (('missing' in wikiDataResponse["query"]["pages"][listPages(wikiDataResponse)[0]]) or ('invalid' in wikiDataResponse["query"]["pages"][listPages(wikiDataResponse)[0]]))

# Gets requested page's title.
def getPageTitle(wikiDataResponse, pageID):
	return wikiDataResponse["query"]["pages"][pageID]["title"]

# Gets requested page's extract (main text).
def getPageExtract(wikiDataResponse, pageID):
	return wikiDataResponse["query"]["pages"][pageID]["extract"]

# Combines single page's title and extract into one output.
def getPageContents(wikiDataResponse, pageID):
	return getPageTitle(wikiDataResponse,pageID) + "\n\n"+getPageExtract(wikiDataResponse,pageID)

# Gets all pages related to the query.
def getPagesContents(wikiDataResponse):
	output = ""

	for i in range(len(listPages(wikiDataResponse))):
		if i > 0:
			output += "\n\n"

		output += getPageContents(wikiDataResponse, listPages(wikiDataResponse)[i])

	return output

# Determines if the query was redirected to another topic.
def redirected(wikiDataResponse):
	return 'redirects' in wikiDataResponse["query"]

# Lists redirections.
def listRedirections(wikiDataResponse):
	return wikiDataResponse["query"]["redirects"]

# Gets redirections in brief format.
def getRedirections(wikiDataResponse):
	output=""

	for i in range(len(listRedirections(wikiDataResponse))):
		if i == 0:
			output += listRedirections(wikiDataResponse)[i]["from"]

		output += " -> "
		output += listRedirections(wikiDataResponse)[i]["to"]

	return output

# Gets fully formatted page from selected Wiki.
def getFullPage(wikiURL, title, useStandardAPIUrl = True, nonStandardAPIUrl = ''):
	output = ""

	try:
		data = getWikiData(wikiURL, title, useStandardAPIUrl, nonStandardAPIUrl)

		if pageMissing(data):
			output = noPageString

		else:
			if redirected(data):
				output += getRedirections(data)
				output += "\n\n"

			output += getPagesContents(data)

	except:
		output = getErrorString

	return output

# Loads configuration from file.
def loadConfig():
	global knownWikis, wiki, textWrappingWidth, useStandardAPIUrl, nonStandardAPIUrl

	configFile = open(configFileName, "r")
	configData = configFile.read()
	config = json.loads(configData)
	knownWikis = config["wikis"]
	setting = config["lastWiki"]
	wiki = setting[0]
	useStandardAPIUrl = setting[1]
	nonStandardAPIUrl = setting[2]
	configFile.close()

# Saves configuration to file.
def saveConfig():
	config = dict()
	config["wikis"] = knownWikis
	setting = [wiki, useStandardAPIUrl, nonStandardAPIUrl]
	config["lastWiki"] = setting
	configFile = open(configFileName, "w")
	configData = json.dumps(config)
	configFile.write(configData)
	configFile.close()

# Simple interpreter utility.
def interpreter():
	global knownWikis, wiki, textWrappingWidth, useStandardAPIUrl, nonStandardAPIUrl

	loadConfig()
	wikisChange = False
	lastUsedWikiChange = False
	temporaryWikiUsed = False

	print(interpreterStart + wiki + interpreterInfo)

	while True:
		title = input(interpreterText)

		if len(title.lstrip()) > 0:
			if len(title.lstrip()) > 1 and title.lstrip()[0] == ':':

				# Adding new Wiki
				if title.lstrip()[1].upper() == 'A':
					inp1 = input(newWikiName)
					inp1 = inp1.lstrip()

					if len(inp1) > 0:
						inp2 = input(newWikiURL)
						inp2 = inp2.lstrip()

						if len(inp2) > 0:
							if(inp2[-1] == "/"):
								inp3 = ""

								while not((inp3.upper() == "Y") or (inp3.upper() == "YES") or (inp3.upper() == "N") or (inp3.upper() == "NO")):
									inp3 = input(ac_nonStandardAPI)
									inp3 = inp3.lstrip()

								inp3 = (inp3.upper() == "Y" or inp3.upper() == "YES")

								if not inp3:
									inp4 = ""
								else:
									inp4 = input(APIUrlString)

								if len(inp4) > 0 or (not inp3):
									setting = [inp2, not inp3, inp4]
									knownWikis[inp1] = setting

									print(newWikiAdded)

									wikisChange = True

								else:
									print(add_EmptyURL)

							else:
								print(add_IncorrectAddress)

						else:
							print(add_EmptyURL)

					else:
						print(add_EmptyURL)

				# Temporary changing Wiki
				elif title.lstrip()[1].upper() == 'C':
					inp = input(changeWiki)
					inp = inp.lstrip()

					if len(inp) > 0:
						if(inp[-1] == "/"):
							inp3 = ""

							while not((inp3.upper() == "Y") or (inp3.upper() == "YES") or (inp3.upper() == "N") or (inp3.upper() == "NO")):
								inp3 = input(ac_nonStandardAPI)
								inp3 = inp3.lstrip()

							inp3 = (inp3.upper() == "Y" or inp3.upper() == "YES")

							if not inp3:
								inp4 = ""
							else:
								inp4 = input(APIUrlString)

							if len(inp4) > 0 or (not inp3):
								wiki = inp
								useStandardAPIUrl = not inp3
								nonStandardAPIUrl = inp4
								lastUsedWikiChange = True
								temporaryWikiUsed = True

								print(wikiChanged + wiki + "\n")

						else:
							print(change_IncorrectAddress)

					else:
						print(change_EmptyURL)

				# Displaying Wiki
				elif title.lstrip()[1].upper() == 'D':
					print(currentWikiIs+wiki)

					if not useStandardAPIUrl:
						print(APIUrlString + nonStandardAPIUrl)

					print("")

				# Saving temporary Wiki to known Wikis
				elif title.lstrip()[1].upper() == 'E':
					if temporaryWikiUsed:
						inp = input(newWikiName)

						if len(inp) > 0:
							setting = [wiki, useStandardAPIUrl, nonStandardAPIUrl]
							knownWikis[inp] = setting

							print(newWikiAdded)

							wikisChange = True
							temporaryWikiUsed = False

					else:
						print(temp_NotInUse)

				# Displaying known Wikis
				elif title.lstrip()[1].upper() == 'K':
					print(knownWikisAre)

					for i in knownWikis:
						print(i + " -> " + knownWikis[i][0])

					print("\n", end = "")

				# Removing known Wiki
				elif title.lstrip()[1].upper() == 'R':
					inp = input(removeFromKnown)
					inp = inp.lstrip()

					if len(inp) > 0:
						if inp in knownWikis:
							print(remove_removed + inp + "\"\n")

							knownWikis.pop(inp, None)
							wikisChange = True

						else:
							print(notKnownStart + inp + remove_notKnownEnd)

					else:
						print(remove_emptyName)

				# Changing default selected Wiki
				elif title.lstrip()[1].upper() == 'S':
					inp = input(changeCurrent_name)
					inp = inp.lstrip()

					if len(inp) > 0:
						if inp in knownWikis:
							wiki = knownWikis[inp][0]
							useStandardAPIUrl = knownWikis[inp][1]
							nonStandardAPIUrl = knownWikis[inp][2]
							lastUsedWikiChange = True
							temporaryWikiUsed = False

							print(changeCurrent_changed + inp + " -> " + wiki + "\n")

						else:
							print(notKnownStart + inp + changeCurrent_notKnown)

					else:
						print(changeCurrent_emptyName)

				# Showing information about program
				elif title.lstrip()[1].upper() == 'I':
					print(infoString)

				# Showing help
				elif title.lstrip()[1] == '?':
					print(helpString)

				# Exiting program
				elif title.lstrip()[1].upper() == 'Q':
					if wikisChange or lastUsedWikiChange:
						saveConfig()

					break

				# Gathering page and displaying results
				else:
					if useStandardAPIUrl:
						print("\n" + getFullPage(wiki, title.lstrip()) + "\n")
					else:
						print("\n" + getFullPage(wiki,title.lstrip(),False, nonStandardAPIUrl) + "\n")

# ---------------------------------------------------------------------------- #
# Main program section.                                                        #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
	if len(sys.argv) > 1:
		if len(sys.argv) == 2 and sys.argv[1].upper() == '-I':
			interpreter()
