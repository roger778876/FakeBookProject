# This module is used for creating the profile page for each user
# It also appends new "About Me" contents to profiles.csv

# file locations
# change it once here, which will change it for all functions
profileCSVFileLocation = "../projectHiddenFiles/profiles.csv"
profilePageTemplateFile = "profileTemplate.html"
editPageTemplateFile = "editAccountTemplate.html"


def createCompletePersonalProfilePage(username, password, destUsername):
	import loginRegisterModule
	profilesDict = loginRegisterModule.csvToDict(profileCSVFileLocation)	# create a profilesDict dictionary from profiles.csv
	ownerName = profilesDict[destUsername]["owner"]		# extract owner name
	aboutContent = profilesDict[destUsername]["about"]	# extract about me content

	source = open(profilePageTemplateFile, "rU")	# "profileTemplate.html"
	profileHTML = source.read()
	source.close()
	
	finalHTML = profileHTML.replace("LOGGEDINUSER", username) \
							.replace("USERNAME", destUsername) \
							.replace("LOGGEDINPASS", password) \
							.replace("OWNERNAME", ownerName) \
							.replace("ABOUTME", aboutContent)
							
	if username == destUsername:	# checks if the user and the profile are the same
		finalHTML = finalHTML.replace("DISABLED", "")	# if they are, then allow the user to edit About me
	# else, the user cannot edit another user's About Me
							
	print finalHTML
	

def editAboutMe(username, newAboutMe):
	newAboutMe = newAboutMe.replace("|", " ").replace("**!!**", " ").replace("\r\n", " ").replace("\n", " ")
	# make the comment conform

	source = open(profileCSVFileLocation, "rU")
	profileLines = source.readlines()
	source.close()
	dest = open(profileCSVFileLocation, "w", 0)
	for line in profileLines:
		firstSeparator = line.find("|")
		usernameField = line[:firstSeparator]	# extracts the username field
		if username != usernameField:	# writes each record line that does not have the desired username
			dest.write(line)
		else:
			editUserRecord = line			# this is the record that the new About Me is added to
			
	userRecordList = editUserRecord.split("|")
	userRecordList[-1] = newAboutMe + "**!!**\n"	# edit last element of the list to include the new about me content
	newUserRecord = "|".join(userRecordList)	# converts the list back into a string
	
	dest.write(newUserRecord)
	dest.close()
	
	
def createEditPage(username, password, message):
	import loginRegisterModule
	profilesDict = loginRegisterModule.csvToDict(profileCSVFileLocation)	# create a profilesDict dictionary from profiles.csv
	ownerName = profilesDict[username]["owner"]		# extract owner name
	password = profilesDict[username]["password"]		# extract owner name

	source = open(editPageTemplateFile, "rU")
	editHTML = source.read()
	source.close()
	
	finalHTML = editHTML.replace("LOGGEDINUSER", username) \
						.replace("LOGGEDINPASS", password) \
						.replace("OWNERNAME", ownerName) \
						.replace("MESSAGE", message)
	
	print finalHTML
	

def editOwner(username, password, editOwner):
	if editOwner.find("|") != -1 or editOwner.find("**!!**") != -1:
	# if the account name or user record is non-conforming
		createEditPage(username, password, "Owner name cannot include the strings: | or **!!**")
	else:
		source = open(profileCSVFileLocation, "rU")
		profileLines = source.readlines()
		source.close()
		dest = open(profileCSVFileLocation, "w", 0)
		for line in profileLines:
			firstSeparator = line.find("|")
			usernameField = line[:firstSeparator]	# extracts the username field
			if username != usernameField:	# writes each record line that does not have the desired username
				dest.write(line)
			else:
				editUserRecord = line			# this is the record that the edited owner is added to
				
		userRecordList = editUserRecord.split("|")
		userRecordList[2] = editOwner	# edit last element of the list to include the new about me content
		newUserRecord = "|".join(userRecordList)	# converts the list back into a string
		
		dest.write(newUserRecord)
		dest.close()
		createEditPage(username, password, "Owner name changed!")
	
def editPassword(username, password, editPassword):
	if editPassword.find("|") != -1 or editPassword.find("**!!**") != -1:
	# if the account name or user record is non-conforming
		createEditPage(username, password, "Password cannot include the strings: | or **!!**")
	else:
		source = open(profileCSVFileLocation, "rU")
		profileLines = source.readlines()
		source.close()
		dest = open(profileCSVFileLocation, "w", 0)
		for line in profileLines:
			firstSeparator = line.find("|")
			usernameField = line[:firstSeparator]	# extracts the username field
			if username != usernameField:	# writes each record line that does not have the desired username
				dest.write(line)
			else:
				editUserRecord = line			# this is the record that the edited owner is added to
				
		userRecordList = editUserRecord.split("|")
		userRecordList[1] = editPassword	# edit last element of the list to include the new about me content
		newUserRecord = "|".join(userRecordList)	# converts the list back into a string
		
		dest.write(newUserRecord)
		dest.close()
		createEditPage(username, password, "Password changed!")