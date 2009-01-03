#!/usr/bin/env python

import os
import pygtk
pygtk.require("2.0")
import gtk
import csv
from random import choice
import string
import xmlrpclib
from xmlrpclib import Server

if __name__ == "__main__":
	pass

class ConfluenceLogin:
	def __init__(self, master=None):
		self.token = ""
		self.master = master
		self.login()
		
	def login(self):
	    #loginVBox Setup
		self.loginVBox = gtk.VBox(False, 0)
		
		#loginHBox Setup
		self.loginHBox = gtk.HBox(False, 0)
		
		#serverHBox Setup
		self.serverHBox = gtk.HBox(False, 0)
		
		#Server Setup
		self.serverLabel = gtk.Label("Server URL: ")
		self.serverEntry = gtk.Entry()
		self.serverEntry.set_text("http://localhost:8080/rpc/xmlrpc")
		self.serverHBox.pack_start(self.serverLabel, True, True, 0)
		self.serverHBox.pack_start(self.serverEntry, True, True, 0)
		
		#User Name Setup
		self.userNameLabel = gtk.Label("Username: ")
		self.userNameEntry = gtk.Entry()
		self.userNameEntry.set_text("admin")
		self.loginHBox.pack_start(self.userNameLabel, True, True, 0)
		self.loginHBox.pack_start(self.userNameEntry, True, True, 0)
		
		#Password Setup
		self.passwordHBox = gtk.HBox(False, 0)
		self.passwordLabel = gtk.Label("Password: ")
		self.passwordEntry = gtk.Entry()
		self.passwordEntry.set_text("admin")
		self.passwordEntry.set_visibility(False)
		self.passwordHBox.pack_start(self.passwordLabel, True, True, 0)
		self.passwordHBox.pack_start(self.passwordEntry, True, True, 10)
		
		#Login Button Setup
		self.loginButton = gtk.Button("     Login     ")
		self.loginButton.connect("clicked", self.authenticate)
		self.buttonHBox = gtk.HBox(False, 0)
		self.buttonHBox.pack_start(self.loginButton, True, False, 0)
		
		#VBox Packing
		self.loginVBox.pack_start(self.serverHBox, False, False, 20)
		self.loginVBox.pack_start(self.loginHBox, False, False, 20)
		self.loginVBox.pack_start(self.passwordHBox, False, False, 20)
		self.loginVBox.pack_start(self.buttonHBox, False, False, 20)
		
		#Show all Items
		self.serverEntry.show()
		self.serverLabel.show()
		self.userNameLabel.show()
		self.userNameEntry.show()
		self.passwordLabel.show()
		self.passwordEntry.show()
		self.loginButton.show()
		self.serverHBox.show()
		self.loginHBox.show()
		self.passwordHBox.show()
		self.buttonHBox.show()
		self.loginVBox.show()
		#return self.loginVBox 
		self.master.mainWindow.add(self.loginVBox)

	def authenticate(self, widget):
	    try:
	        if self.serverEntry.get_text().endswith("xmlrpc") != True:
	    	    raise NameError, "Invalid URL"
	    	else:
	        	self.server = Server(self.serverEntry.get_text())

	        self.token = self.server.confluence1.login(self.userNameEntry.get_text(), self.passwordEntry.get_text())
	        self.master.mainWindow.remove(self.loginVBox)
	        self.launchPad()

	    except xmlrpclib.Fault:
    		self.master.errDialog("\t\t\tLogin Failed\t\t\t")

	    except NameError:
    		self.master.errDialog("\t\t\tURL Must end with proper RPC \n http://test.com/rpc/xmlrpc for example\t\t\t")

	    except:
    		self.master.errDialog("\t\tConnection Failed\t\t")

	def launchPad(self):
		    #Vertical Box
		self.menuVBox = gtk.VBox(False, 0)
		
		#Menu Label
		self.menuLabel = gtk.Label("What Actions Would You Like to Perform Today?")
		
		#User Management
		self.userManageButton = gtk.Button("Manage Users")
		self.userManageButton.connect("clicked", self.master.userObj.userManagement)
		
		#Search Button
		self.searchButton = gtk.Button("Search Confluence")
		self.searchButton.connect("clicked", self.master.searchObj.searchConfluence)
		
		#Content Management Button
		self.contentButton = gtk.Button("Content Management")
		self.contentButton.connect("clicked", self.master.contentObj.contentManagement)
		
		#Pack it all Up
		self.menuVBox.pack_start(self.menuLabel, False, False, 0)
		self.menuVBox.pack_start(self.userManageButton, False, False, 30)
		self.menuVBox.pack_start(self.searchButton, False, False, 30)
		self.menuVBox.pack_start(self.contentButton, False, False, 30)
		
		#Show it Off
		self.menuLabel.show()
		self.userManageButton.show()
		self.searchButton.show()
		self.contentButton.show()
		self.menuVBox.show()
		self.master.mainWindow.add(self.menuVBox)
		
