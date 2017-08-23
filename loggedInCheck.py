# This module checks if the user is logged in & if username/password are valid
# This module should always run when the user clicks to a new page of the site


# CSV Acct/Pass file location
# change it once here, which will change it for all functions
profileCSVFileLocation = "../projectHiddenFiles/profiles.csv"


# returns True/False
def checkUserPass(username, password):
	import loginRegisterModule		# borrows csvToDict and checkKeyMatch
	profilesDict = loginRegisterModule.csvToDict(profileCSVFileLocation)	# file location changeable at top of this program
	if loginRegisterModule.checkKeyMatch(profilesDict, username):	# check if there is such an acct name
		if profilesDict[username]["password"] == password:			# check if pass for the acct is correct
			return True
		else:	# wrong pass
			return False
	else:
		return False