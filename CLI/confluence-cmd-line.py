#!/usr/bin/python
# Confluence XML RPC Fun!
#
import os
import sys
import getpass
import xmlrpclib
from xmlrpclib import Server

server = Server("https://extranet.contegix.com/rpc/xmlrpc")

def authentication():
	# Creates the authentication token
	print "Please provide your username: "
	userName = sys.stdin.readline()
	password = getpass.getpass("Please enter your password: ")
	token = server.confluence1.login(userName.rstrip("\n"), password.rstrip("\n"))
	return token

def blogPost(token):
	print "Please provide the title you'd like for your shift notes: "
	title = sys.stdin.readline()
	title = title.rstrip("\n")
        print "Please provide the text we'll be appending to the page. Please keep in mind that all wiki markup rules do apply. Just press Ctrl+D to quit"
        content = sys.stdin.read()
	print "What space will this be posted to?"
	spaceKey = sys.stdin.read()
	spaceKey = spaceKey.rstrip("\n")
	newBlog = {"title":title,"space":spaceKey,"content":content}
	server.confluence1.storeBlogEntry(token, newBlog)

def updatePage(token):
	print "Please provide the space key we'll be posting to:"
	spaceKey = sys.stdin.readline()
	spaceKey = spaceKey.rstrip("\n")
	print "Please provide the page name we'll be updating:"
	pageName = sys.stdin.readline()
	pageName = pageName.rstrip("\n")
	page = server.confluence1.getPage(token, spaceKey, pageName)
	print "Please provide the text we'll be appending to the page. Please keep in mind that all wiki markup rules do apply. Just press Ctrl+D to quit"
	content = sys.stdin.read()
	page["content"] += content
	server.confluence1.storePage(token, page)
	print "\nThanks for using Mark's magical Confluence script. The URL of that you just edited is: "
	print page["url"]	

def newPage(token):
        print "Please provide the space key we'll be posting to:"
        spaceKey = sys.stdin.readline()
        spaceKey = spaceKey.rstrip("\n")
        print "Please provide the name of the page you'd like to create:"
        pageName = sys.stdin.readline()
        pageName = pageName.rstrip("\n")
        print "Please provide the text we'll be appending to the page. Please keep in mind that all wiki markup rules do apply. Just press Ctrl+D to quit"
        content = sys.stdin.read()
        newPost = {"title":pageName,"content":content,"space":spaceKey}
        server.confluence1.storePage(token, newPost)
        createdPage = server.confluence1.getPage(token, spaceKey, pageName)
        print "\nThanks for using Mark's magical Confluence script. The URL of that you just created is: "
        print createdPage["url"]

def search(token):
	print "Please provide your search criteria: "
	criteria = sys.stdin.readline()
	criteria = criteria.rstrip("\n")
	print
	results = server.confluence1.search(token, criteria, 50)
	for i in results:
		print "Title: \t %s" % i["title"]
		print "URL: \t %s" % i["url"]
		print "Excerpt: \t %s" % i["excerpt"]
		print

def addUser(token):
	print "Please provide the username to create: "
	userName = sys.stdin.readline()
	userName = userName.rstrip("\n")
	print "Please enter user's full name: "
	fullName = sys.stdin.readline()
	fullName = fullName.rstrip("\n")
	print "Please enter user's email address: "
	email = sys.stdin.readline()
	email = email.rstrip("\n")
	print "Please provide the password for this user:"
	password = sys.stdin.readline()
	password = password.rstrip("\n")
	userDict = {"name":userName, "fullname":fullName,"email":email}
	server.confluence1.addUser(token, userDict, password)
	server.confluence1.addUserToGroup(token, userName, "confluence-users")
        verification = server.confluence1.getUser(token, userName)
        print "User: %s" % verification["name"]
        verification = server.confluence1.getUserGroups(token, userName)
        print "Groups: %s" % verification

def addUserToGroup(token):
	print "Please provide the username we'll be working with:"
        userName = sys.stdin.readline()
        userName = userName.rstrip("\n")
	print "Please provide the group we'll be adding this user to:"
	groupName = sys.stdin.readline()
	groupName = groupName.rstrip("\n")
	server.confluence1.addUserToGroup(token, userName, groupName)
	verification = server.confluence1.getUser(token, userName)
	print "User: %s" % verification["name"]
	verification = server.confluence1.getUserGroups(token, userName)
	print "Groups: %s" % verification

def delUser(token):
	print "What user will we be nuking today?"
	userName = sys.stdin.readline()
        userName = userName.rstrip("\n")
	print "Are you sure? (y/n)"
	sanity = sys.stdin.readline()
	sanity = sanity.rstrip("\n")
	sanity = sanity.lower()
	if (sanity == "yes") | (sanity == "y"):
		server.confluence1.removeUser(token, userName)
		print "This user has been removed"
	else:
		print "Understood. This user will not be removed. Goodbye!"
		sys.exit(1)

def removeFromGroup(token):
	print "What user will we be working with today?"
	userName = sys.stdin.readline()
        userName = userName.rstrip("\n")
	print "What group will we removing this user from?"
	groupName = sys.stdin.readline()
        groupName = groupName.rstrip("\n")
	server.confluence1.removeUserFromGroup(token, userName, groupName)
	verification = server.confluence1.getUser(token, userName)
        print "User: %s" % verification["name"]
        verification = server.confluence1.getUserGroups(token, userName)
        print "Groups: %s" % verification

def addGroup(token):
        print "What group will we adding?"
        groupName = sys.stdin.readline()
        groupName = groupName.rstrip("\n")
	server.confluence1.addGroup(token, groupName)
	verification = server.confluence1.getGroups(token)
	print "Available Groups: %s" % verification

def removeGroup(token):
        print "What group will we removing?"
        groupName = sys.stdin.readline()
        groupName = groupName.rstrip("\n")
        server.confluence1.removeGroup(token, groupName, "")
        verification = server.confluence1.getGroups(token)
        print "Available Groups: %s" % verification

def removePage(token):
        print "Please provide the space key we'll be removing from:"
        spaceKey = sys.stdin.readline()
        spaceKey = spaceKey.rstrip("\n")
        print "Please provide the page name we'll be removing:"
        pageName = sys.stdin.readline()
        pageName = pageName.rstrip("\n")
        page = server.confluence1.getPage(token, spaceKey, pageName)
	server.confluence1.removePage(token, page["id"])

def addSpace(token):
	print "Please provide the Space Name you'd like to add (not key):"
	spaceName = sys.stdin.readline()
	spaceName = spaceName.rstrip("\n")
	print "Please provide the Space Key that you desire (generally an all-cap abbreviation):"
	spaceKey = sys.stdin.readline()
	spaceKey = spaceKey.rstrip("\n")
	print "Please provide a short, one line description of the space:"
	spaceDesc = sys.stdin.readline()
	spaceDesc = spaceDesc.rstrip("\n")
	space = {"key":spaceKey,"name":spaceName,"description":spaceDesc}
	server.confluence1.addSpace(token, space)
	spaces = server.confluence1.getSpaces(token)
	print "Available Spaces:"
	for i in spaces:
		print i["name"]

def removeSpace(token):
	print "Please provide the space key you'd like to see blown away:"
        spaceKey = sys.stdin.readline()
        spaceKey = spaceKey.rstrip("\n")
	server.confluence1.removeSpace(token, spaceKey)
        spaces = server.confluence1.getSpaces(token)
        print "Available Spaces:"
        for i in spaces:
                print i["name"]

def importSpace(token):
	print "Please provide the path to the ZIPPED XML Space backup:"
	backup_zip = sys.stdin.readline()
	backup_zip = backup_zip.rstrip()
	backup_file = open(backup_zip, "r")
	backup_raw = backup_file.read()
	backup_binary = xmlrpclib.Binary(backup_raw)
	result = server.confluence1.importSpace(token, backup_binary)
	if result:
		print "Space imported successfully"
	else:
		print "Space import failed"

def menu():
        print "What would you like to do today?"
	print "1. User Management"
	print "2. Searching Extranet"
	print "3. Content Management"
	option = sys.stdin.readline()
        option = option.rstrip("\n")
	if option == '1':
		os.system("clear")
		print "1. Add user"
		print "2. Add User to Group"
		print "3. Remove User"
		print "4. Remove User from Group"
		print "5. Add Group"
		print "6. Remove Group"
		option = sys.stdin.readline()
	        option = option.rstrip("\n")
		if option == '1':
			auth = authentication()
			addUser(auth)
			server.confluence1.logout(auth)
		elif option == '2':
			auth = authentication()
			addUserToGroup(auth)
			server.confluence1.logout(auth)
		elif option == '3':
			auth = authentication()
			delUser(auth)
			server.confluence1.logout(auth)
		elif option == '4':
			auth = authentication()
			removeFromGroup(auth)
			server.confluence1.logout(auth)
		elif option == '5':
			auth = authentication()
			addGroup(auth)
			server.confluence1.logout(auth)
		elif option == '6':
			auth = authentication()
			removeGroup(auth)
			server.confluence1.logout(auth)
                else:
                        print "Invalid option"
                        sys.exit(1)


	elif option == '2':
		os.system("clear")
		auth = authentication()
		search(auth)
		server.confluence1.logout(auth)
	
	elif option == '3':
		os.system("clear")
		print "1. Blog Post"
		print "2. Add New Page"
		print "3. Update Existing Page"
		print "4. Remove Page"
		print "5. Add Space"
		print "6. Remove Space"
		print "7. Import Space"
		option = sys.stdin.readline()
	        option = option.rstrip("\n")
		if option == '1':
			auth = authentication()
			blogPost(auth)
			server.confluence1.logout(auth)
		elif option == '2':
			auth = authentication()
			newPage(auth)
			server.confluence1.logout(auth)
		elif option == '3':
			auth = authentication()
			updatePage(auth)
			server.confluence1.logout(auth)
		elif option == '4':
			auth = authentication()
			removePage(auth)
			server.confluence1.logout(auth)
		elif option == '5':
			auth = authentication()
			addSpace(auth)
			server.confluence1.logout(auth)
		elif option == '6':
			auth = authentication()
			removeSpace(auth)
			server.confluence1.logout(auth)
		elif option == '7':
			auth = authentication()
			importSpace(auth)
			server.confluence1.logout(auth)
		else:
			print "Invalid option"
			sys.exit(1)
	
	else:
        	print "Invalid option"
	        sys.exit(1)

		
if __name__ == "__main__":
	menu()
	sys.exit(0)
