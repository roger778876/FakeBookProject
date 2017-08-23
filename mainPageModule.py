# This module is used to append to the mainpage posts CSV file, 
# as well as printing the mainpage's HTML
# The central python file will call this program's functions when needed

# file locations
# change it once here, which will change it for all functions
mainPagePostsCSV = "../projectHiddenFiles/mainpage.csv"
mainHtmlTemplateFile = "htmlTemplate.html"
navigationBarTemplateFile = "navBar.html"
newPostTableTemplateFile = "newPostTableTemplate.html"
postTableTemplateFile = "postTableTemplate.html"
postCommentTableTemplateFile = "postCommentTableTemplate.html"


if __name__ == "__main__":		# when testing just the module
	from time import strftime	# import the current time for later test cases
	print strftime("%Y-%m-%d %H:%M:%S")
	
'''appendToMainPageCSV: combines all of the fields and appends to the mainpage.csv file'''
# this only appends, formatting should be done beforehand
# the separators between fields are pipelines ("|")
# the separators between records are **!!**
# the newlines come *after* each record, meaning the previous mainpage.csv file must have a newline at the end
def appendToMainPageCSV(timeDate, username, postContent, postLikes, postComments, password):
	if postContent.find("|") != -1 or postContent.find("**!!**") != -1:		# new post is non-conforming
		import loginRegisterModule
		loginRegisterModule.htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>Post content cannot include the strings: | or **!!**<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')
	else:
		postContent = postContent.replace("$%$%", " ").replace("\r\n", " ").replace("\n", " ")
		# make post content conform
		newRecord = timeDate + "|" + username + "|" + postContent + "|" + postLikes + "|" + postComments + "**!!**\n"
		dest = open(mainPagePostsCSV, "a", 0)
		dest.write(newRecord)
		dest.close()
		createCompleteMainPage(username, password)

	
# appendToMainPageCSV(strftime("%Y-%m-%d %H:%M:%S"), "username", "content ", "postlikes", "postcomments")

# extract individual comments from a full comment field from mainpage.csv
# called in createCompleteMainPage; supposed to receive only the comment field of one timeDate
# RETURNS HTML FOR THE WHOLE COMMENT SECTION (excluding new comment form)
# comment field format: USERNAME$%$%TIMEDATE$%$%COMMENT$%$%
# use $%$% to split
def extractPostCommentsToHTML(commentField):
	userCommentList = commentField.split("$%$%")	# user/time/comment will be grouped (0,1,2) (3,4,5) etc.
	userCommentList.pop(-1)		# removes last empty string element that comes from splitting by $%$%
	# print userCommentList
	
	source = open(postCommentTableTemplateFile, "rU")	# opens the comment table template
	commentTemplate = source.read()
	source.close()
	finalHTML = ""
	i = 0
	while i < len(userCommentList):		# user/time/comment will be grouped (0,1,2) (3,4,5) etc.
		username = userCommentList[i]
		timeDate = userCommentList[i+1]
		content = userCommentList[i+2]
		
		newCommentHTML = commentTemplate.replace("USERNAME", username) \
										.replace("TIMEDATE", timeDate) \
										.replace("COMMENT", content)
		finalHTML = newCommentHTML + finalHTML
		i += 3
	return finalHTML
	

def appendNewComment(username, postTimeDate, commentTimeDate, newComment):
	newComment = newComment.replace("|", " ").replace("$%$%", " ").replace("**!!**", " ").replace("\r\n", " ").replace("\n", " ")
	# make the comment conform

	source = open(mainPagePostsCSV, "rU")
	postLines = source.readlines()
	source.close()
	dest = open(mainPagePostsCSV, "w", 0)
	for line in postLines:
		timeDate = line[:19]			# views the timeDate field
		if timeDate != postTimeDate:	# writes each post line that does not have the correct timeDate
			dest.write(line)
		else:
			newPostLine = line			# this is the post that the new comment is added to
			
	newPostLineList = newPostLine.split("|")	# gets separate fields of the postline as list elements
	newCommentEntry = username + "$%$%" + commentTimeDate + "$%$%" + newComment + "$%$%" + "**!!**\n"	# creates a new comment entry
	commentField = newPostLineList[-1]	# retrieves the last element of the postline list, aka the comment field
	newPostLineList[-1] = commentField[0:-7] + newCommentEntry	# adds on the new comment entry
	newPostLine = "|".join(newPostLineList)		# converts the postline list back into a string
	dest.write(newPostLine)
	dest.close()
	
# appendNewComment("username", "password", "2016-05-31 18:33:21", "2016-05-31 11:22:33", "hello!!!!!  dd")


def appendNewLike(username, postTimeDate):
	source = open(mainPagePostsCSV, "rU")
	postLines = source.readlines()
	source.close()
	dest = open(mainPagePostsCSV, "w", 0)
	for line in postLines:
		timeDate = line[:19]			# views the timeDate field
		if timeDate != postTimeDate:	# writes each post line that does not have the correct timeDate
			dest.write(line)
		else:
			newPostLine = line			# this is the post that the new like is added to
			
	newPostLineList = newPostLine.split("|")	# gets separate fields of the postline as list elements
	if newPostLineList[-2].find(username) == -1:	# if the user has not liked the post previously
		newPostLineList[-2] = username + ", " + newPostLineList[-2]	# adds new liker to front of existing like field
	else:	# the user has liked the post previously, so we assume they want to unlike
		newPostLineList[-2] = newPostLineList[-2].replace(username + ", ", "")
	newPostLine = "|".join(newPostLineList)		# converts the postline list back into a string
	dest.write(newPostLine)
	dest.close()
	

'''createPostTable: sorts all fields into a HTML table, prints HTML code'''
# there is no <!DOCTYPE html> etc., only the <table> elements
# this reads from the templateFile, where the HTML template code is stored
# receives html code for commentsection
def createPostTable(timeDate, poster, postContent, postLikes, postComments, loggedUser, loggedPass):
	source = open(postTableTemplateFile, "rU")
	postTableTemplate = source.read()
	source.close()
	postTable = postTableTemplate.replace("USERNAME", poster) \
										.replace("TIMEDATE", timeDate)	\
										.replace("POSTCONTENT", postContent)	\
										.replace("LIKESRECEIVED", postLikes)	\
										.replace("COMMENTSECTION", postComments) \
										.replace("LOGGEDINUSER", loggedUser) \
										.replace("LOGGEDINPASS", loggedPass) \
										.replace("POSTINGTIME", timeDate)
	return postTable
	
# print createPostTable(strftime("%Y-%m-%d %H:%M:%S"), "username", "content ", "postlikes", "postcomments")



# create post tables for all posts stored in mainpage.csv
# prints out the tables in reverse chronological order, aka latest first
def createAllPosts(username, password):
	import loginRegisterModule		# only imports if needed, saves memory
	postsDict = loginRegisterModule.csvToDict(mainPagePostsCSV)	# creates dictionary of posts records
	revKeyList = sorted(postsDict.keys())[::-1]		# sorts posts by reverse time/date (latest appears first)
	# return revKeyList
	
	finalHTML = ""
	for timeDate in revKeyList:								# goes through each timeDate in order
		poster = postsDict[timeDate]["username"]			# creates variables to be used in createPostTable
		postContent = postsDict[timeDate]["postContent"]
		postLikes = postsDict[timeDate]["postLikes"]
		postComments = extractPostCommentsToHTML(postsDict[timeDate]["postComments"])	# change this to accomadate new function
		
		finalHTML += createPostTable(timeDate, poster, postContent, postLikes, postComments, username, password)
		
	return finalHTML
	
# print createAllPosts("mainpage.csv")

def createNavBar(username, password):
	source = open(navigationBarTemplateFile, "rU")
	navBarHTML = source.read()
	source.close()
	
	finalHTML = navBarHTML.replace("LOGGEDINUSER", username).replace("LOGGEDINPASS", password)
	return finalHTML


def createNewPostFormTable(username, password):
	source = open(newPostTableTemplateFile, "rU")
	newPostTemplate = source.read()
	source.close()
	
	finalHTML = newPostTemplate.replace("LOGGEDINUSER", username).replace("LOGGEDINPASS", password)
	return finalHTML


# create surrounding webpage (DOCTYPE, etc.) with all posts included
# the body should be already in HTML, and ready to replace the placeholder
def createCompleteMainPage(username, password):
	navBarHTML = createNavBar(username, password)
	newPostForm = createNewPostFormTable(username, password)
	postsHTML = createAllPosts(username, password)
	
	source = open(mainHtmlTemplateFile, "rU")	# "htmlTemplate.html"
	htmlTemplate = source.read()
	source.close()
	finalHTML = htmlTemplate.replace("REPLACETITLE", "FakeBook") \
							.replace("METAREPLACE", "") \
							.replace("REPLACEBODY", navBarHTML + newPostForm + postsHTML)
								
	print finalHTML