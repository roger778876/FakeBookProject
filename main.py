#! /usr/bin/python
print "content-type: text/html\n"

import cgitb
cgitb.enable()


# This is the main Python program
# The user's inputs are received in this program, which 
# then calls functions from various other modules to present
# the user with a new page with new info


# detect what the user wants to do
import cgi
queryString = cgi.FieldStorage()

# checks if there is no user action
if not ("userAction" in queryString):
	import loginRegisterModule
	loginRegisterModule.htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>You cannot visit main.py directly.<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')		
	exit()
	
	
# requires forms: "username", "password"... submit name: "Login"
if queryString["userAction"].value == "Login":		# user wants to login to existing account
	username = queryString["username"].value
	password = queryString["password"].value
	
	# if username/password is valid, goes to mainpage
	# if incorrect, goes to error page
	# the printing of the html in mainPageModule.py; loginRegisterModule.py will call it
	import loginRegisterModule
	if loginRegisterModule.checkUserPass(username, password):
		import mainPageModule
		mainPageModule.createCompleteMainPage(username, password)
	else:
		loginRegisterModule.htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>Incorrect login.<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')
		
# requires forms: "newUsername", "newPassword", "newOwner"... submit name: "Create"	
elif queryString["userAction"].value == "Create":	# user wants to create a new account
	newUsername = queryString["newUsername"].value
	newPassword = queryString["newPassword"].value
	newOwner = queryString["newOwner"].value
	
	# combines all of the fields into a single line to be appended to profiles.csv
	newUserRecord = newUsername + "|" + newPassword + "|" + newOwner + "|" + "**!!**\n"

	import loginRegisterModule
	loginRegisterModule.checkAcctExistAndCreate(newUsername, newUserRecord)

# requires forms: "commentContent"; hidden forms: "username", "password", "postTimeDate"... submit name: "Comment"
elif queryString["userAction"].value == "Comment":
	username = queryString["username"].value
	password = queryString["password"].value
	postTimeDate = queryString["postTimeDate"].value
	newComment = queryString["commentContent"].value
	from time import strftime	# import the time of comment
	commentTimeDate = strftime("%Y-%m-%d %H:%M:%S")

	import loginRegisterModule
	if loginRegisterModule.checkUserPass(username, password):		# if the user/pass is valid
		import mainPageModule
		mainPageModule.appendNewComment(username, postTimeDate, commentTimeDate, newComment)
		mainPageModule.createCompleteMainPage(username, password)
	else:
		loginRegisterModule.htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>You are not logged in.<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')
		
# requires forms: "postContent"; hidden forms: "username", "password"... submit name: "Post"
elif queryString["userAction"].value == "Post":
	username = queryString["username"].value
	password = queryString["password"].value
	newPostContent = queryString["postContent"].value
	from time import strftime	# import the time of the new post
	newPostTimeDate = strftime("%Y-%m-%d %H:%M:%S")
	
	import loginRegisterModule
	if loginRegisterModule.checkUserPass(username, password):		# if the user/pass is valid
		import mainPageModule
		mainPageModule.appendToMainPageCSV(newPostTimeDate, username, newPostContent, "", "", password)
	else:
		loginRegisterModule.htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>You are not logged in.<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')
		
# requires hidden forms: "username", "password"... submit name: "Home"	
elif queryString["userAction"].value == "Home":
	username = queryString["username"].value
	password = queryString["password"].value
			
	import loginRegisterModule
	if loginRegisterModule.checkUserPass(username, password):	# if the user/pass is valid
		import mainPageModule
		mainPageModule.createCompleteMainPage(username, password)
	else:
		loginRegisterModule.htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>You are not logged in.<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')
			
# requires hidden forms: "username", "password"... submit name: "Profile"	
elif queryString["userAction"].value == "Profile":
	username = queryString["username"].value
	password = queryString["password"].value
	
	import loginRegisterModule
	if loginRegisterModule.checkUserPass(username, password):	# if the user/pass is valid
		import profilePageModule
		profilePageModule.createCompletePersonalProfilePage(username, password, username)
	else:
		loginRegisterModule.htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>You are not logged in.<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')

# requires hidden forms: "username", "password"... submit name: "editAboutMe"	
elif queryString["userAction"].value == "editAboutMe":
	username = queryString["username"].value
	password = queryString["password"].value
	newAboutMe = queryString["aboutContent"].value
	
	import loginRegisterModule
	if loginRegisterModule.checkUserPass(username, password):	# if the user/pass is valid
		import profilePageModule
		profilePageModule.editAboutMe(username, newAboutMe)
		profilePageModule.createCompletePersonalProfilePage(username, password, username)
	else:
		loginRegisterModule.htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>You are not logged in.<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')

# requires hidden forms: "username", "password", "viewProfileUsername"... submit name: "OtherProfile"	
elif queryString["userAction"].value == "OtherProfile":
	username = queryString["username"].value
	password = queryString["password"].value
	viewProfileUsername = queryString["viewProfileUsername"].value
	
	import loginRegisterModule
	if loginRegisterModule.checkUserPass(username, password):	# if the user/pass is valid
		import profilePageModule
		profilePageModule.createCompletePersonalProfilePage(username, password, viewProfileUsername)
	else:
		loginRegisterModule.htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>You are not logged in.<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')
		
# requires hidden forms: "username", "password", "postTimeDate"... submit name: "LikePost"	
elif queryString["userAction"].value == "LikePost":
	username = queryString["username"].value
	password = queryString["password"].value
	postTimeDate = queryString["postTimeDate"].value
	
	import loginRegisterModule
	if loginRegisterModule.checkUserPass(username, password):	# if the user/pass is valid
		import mainPageModule
		mainPageModule.appendNewLike(username, postTimeDate)
		mainPageModule.createCompleteMainPage(username, password)
	else:
		loginRegisterModule.htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>You are not logged in.<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')

# requires hidden forms: "username", "password", "editOwner"... submit name: "editAccount"	
elif queryString["userAction"].value == "editAccount":
	username = queryString["username"].value
	password = queryString["password"].value

	import loginRegisterModule
	if loginRegisterModule.checkUserPass(username, password):	# if the user/pass is valid
		import profilePageModule
		profilePageModule.createEditPage(username, password, "")
	else:
		loginRegisterModule.htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>You are not logged in.<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')
		
# requires hidden forms: "username", "password", "editOwner"... submit name: "editOwner"	
elif queryString["userAction"].value == "editOwner":
	username = queryString["username"].value
	password = queryString["password"].value
	editOwner = queryString["editOwner"].value
	
	import loginRegisterModule
	if loginRegisterModule.checkUserPass(username, password):	# if the user/pass is valid
		import profilePageModule
		profilePageModule.editOwner(username, password, editOwner)
	else:
		loginRegisterModule.htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>You are not logged in.<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')
		
# requires hidden forms: "username", "password", "editPassword"... submit name: "editPassword"	
elif queryString["userAction"].value == "editPassword":
	username = queryString["username"].value
	password = queryString["password"].value
	editPassword = queryString["editPassword"].value
	
	import loginRegisterModule
	if loginRegisterModule.checkUserPass(username, password):	# if the user/pass is valid
		import profilePageModule
		profilePageModule.editPassword(username, password, editPassword)
	else:
		loginRegisterModule.htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>You are not logged in.<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')

else:
	import loginRegisterModule
	loginRegisterModule.htmlMessage("Error", '<meta http-equiv="refresh" content="5;url=http://bart.stuy.edu/~cesar.mu/project/">', '<center><br>You cannot visit main.py directly.<br>You should be redirected to the login page shortly, or<br><a href="http://bart.stuy.edu/~cesar.mu/project/">Return to login page immediately</a></center>')