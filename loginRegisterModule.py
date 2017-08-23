# This module is used for allowing the user to log into his/her account
# and for adding newly created accounts to profiles csv file
# The central python file will call this program when needed


# file locations
# change it once here, which will change it for all functions
profileCSVFileLocation = "../projectHiddenFiles/profiles.csv"
htmlTemplateFile = "htmlTemplate.html"



'''HTML CODE'''
def htmlMessage(title, metaRefresh, message):
	source = open(htmlTemplateFile, "rU")
	htmlTemplate = source.read()
	source.close()
	
	finalHTML = htmlTemplate.replace("REPLACETITLE", title) \
							.replace("METAREPLACE", metaRefresh) \
							.replace("REPLACEBODY", message)
							
	print finalHTML

	
			
'''LOGIN TO EXISTING ACCOUNT CODE'''	
# modular function that reads CSV data from a .csv file
# and creates a dictionary using each line's first value as the keys
# the .csv file's first line should be headers

def csvToDict(fileName):
	# binds the file contents to "csvData"
	source = open(fileName, "rU")
	csvData = source.read()
	source.close
	
	# converts the content to a list "csvDataList", separated by **!!** (makeshift newlines)
	csvDataList = csvData.split("**!!**\n")
	
	# extracts/cuts the headers into a list "csvHeaders"
	csvHeaders = csvDataList.pop(0).split("|")	# splits by pipelines ("|") (alternative to commas)
	
	# creates dictionary of headers/values, then binds the dictionary
	# to the first value of the respective CSV line in a new dict. "finalDict"
	finalDict = {}
	for record in csvDataList:
		recordList = record.split("|")
		
		headerValueDict = {}
		headerValuePair = 1			# starts at index 1 to ignore header 0 and value 0
		while headerValuePair < len(recordList):
			headerValueDict[csvHeaders[headerValuePair]] = recordList[headerValuePair]	# binds value to header
			headerValuePair += 1
		
		# binds dictionary of header/value pairs to the key (first value of the CSV line)
		finalDict[recordList[0]] = headerValueDict
		
	finalDict.pop("")	# this removes the empty key, merely for convenience
	return finalDict


# check if key is in dictionary. True/False
def checkKeyMatch(dictionary, key):
	return key in dictionary


# check if account name is in the csv dictionary, then check if password is valid
# returns True/False
def checkUserPass(username, password):
	profilesDict = csvToDict(profileCSVFileLocation)	# file location changeable at top of this program
	if checkKeyMatch(profilesDict, username):	# check if there is such an acct name
		if profilesDict[username]["password"] == password:			# check if pass for the acct is correct
			return True
		else:	# wrong pass
			return False
	else:	# wrong username
		return False



'''CREATE NEW ACCOUNT CODE'''
# helper function; modular function that appends newContent to fileName
# the newContent should have a "\n" as its first character when appending to .csv files
def appendToCSV(newContent):
	# open the .csv file for appending
	source = open(profileCSVFileLocation, "a")
	source.write(newContent)
	source.close()
	
# the newUserRecord must end in **!!**\n and use pipelines as separators
'''call this function to create new acct'''
def checkAcctExistAndCreate(accountName, newUserRecord):
	if accountName == "username" or accountName == "LOGGEDINUSER" or accountName.find("|") != -1 or accountName.find("**!!**") != -1 or \
	newUserRecord.count("|") != 3 or newUserRecord.count("**!!**") != 1:
	# if the account name or user record is non-conforming
		htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>Username/password/first name cannot include the strings: | or **!!**<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')
	else:
		# open the file for reading 
		source = open(profileCSVFileLocation, "rU")
		content = source.read()
		source.close
		
		# check for existence of account with same username
		lookFor = "**!!**\n" + accountName + "|"	# accountName and newlines/separators, to be more specific
		if content.find(lookFor) == -1:		# if account name does not belong to someone else
			appendToCSV(newUserRecord)
			htmlMessage("Success", '<meta http-equiv="refresh" content="3;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>Successful account creation.<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')
		else:
			htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>Account name already taken.<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')