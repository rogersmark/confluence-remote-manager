#!/usr/bin/env python
# Confluence XML RPC GTK Agent (acronym soup anyone?)
"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import pygtk
pygtk.require("2.0")
import gtk
import xmlrpclib
from xmlrpclib import Server

server = Server("http://localhost:8080/rpc/xmlrpc")

class ConfluenceGTK:

    def quit(self, widget=None, data=None):
        if self.token != "":
            self.server.confluence1.logout(self.token)
                        
        gtk.main_quit()

    def __init__(self):
        self.token = ""
        self.mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.mainWindow.set_size_request(600,500)
        self.mainWindow.set_title("Confluence Remote Updater")
        self.mainWindow.connect("delete_event", lambda w,e: self.quit())
        self.mainWindow.set_border_width(20)
        self.login()
        self.mainWindow.show()

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
        self.userNameEntry.set_text("")
        self.loginHBox.pack_start(self.userNameLabel, True, True, 0)
        self.loginHBox.pack_start(self.userNameEntry, True, True, 0)

        #Password Setup
        self.passwordHBox = gtk.HBox(False, 0)
        self.passwordLabel = gtk.Label("Password: ")
        self.passwordEntry = gtk.Entry()
        self.passwordEntry.set_text("")
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
        self.mainWindow.add(self.loginVBox)

    def authenticate(self, widget):
        try:
            if self.serverEntry.get_text().endswith("xmlrpc") != True:
                raise NameError, "Invalid URL"
            else:
                self.server = Server(self.serverEntry.get_text())
            self.token = self.server.confluence1.login(self.userNameEntry.get_text(), self.passwordEntry.get_text())
            self.mainWindow.remove(self.loginVBox)
            self.launchPad()
            
        except xmlrpclib.Fault:
            self.errDialog("           Login Failed              ")
            
        except NameError:
            self.errDialog("           URL Must end with proper RPC \n http://test.com/rpc/xmlrpc for example              ")
            
        except:
            self.errDialog("\t\tConnection Failed\t\t")

    def launchPad(self):
        #Vertical Box
        self.menuVBox = gtk.VBox(False, 0)
        
        #Menu Label
        self.menuLabel = gtk.Label("What Actions Would You Like to Perform Today?")

        #User Management
        self.userManageButton = gtk.Button("Manage Users")
        self.userManageButton.connect("clicked", self.userManagement)

        #Search Button
        self.searchButton = gtk.Button("Search Confluence")
        self.searchButton.connect("clicked", self.searchConfluence)

        #Content Management Button
        self.contentButton = gtk.Button("Content Management")
        self.contentButton.connect("clicked", self.contentManagement)

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
        self.mainWindow.add(self.menuVBox)

    def userManagement(self, widget):
        #Remove the current VBox
        self.mainWindow.remove(self.menuVBox)

        #Create our new Vbox
        self.userManagementVBox = gtk.VBox(False, 0)
        
        #Content Label
        self.userManageLabel = gtk.Label("Choose Your Content Options Below")

        #Couple of HBoxes to hold Radio buttons
        self.userManageHBoxTop = gtk.HBox(False, 0)
        self.userManageHBoxBottom = gtk.HBox(False,0)
        
        #Radio Buttons Center
        self.updatePostRadioVBox = gtk.VBox(False, 0)
        self.addUserRadio = gtk.Button("Add User")
        self.rmUserRadio = gtk.Button("Remove User")
        self.addGroupRadio = gtk.Button("Add Group")
        self.rmGroupRadio = gtk.Button("Remove Group")
        self.addToGroupRadio = gtk.Button("Add User To Group")
        self.rmFromGroupRadio = gtk.Button("Remove User From Group")

        #Connect the Buttons to Funcs
        self.addUserRadio.connect("clicked", self.addUser)
        self.rmUserRadio.connect("clicked", self.removeUser)
        self.addGroupRadio.connect("clicked", self.addGroup)
        self.rmGroupRadio.connect("clicked", self.removeGroup)
        self.addToGroupRadio.connect("clicked", self.addToGroup)
        self.rmFromGroupRadio.connect("clicked", self.removeFromGroup)

        #Pack All the Radio Buttons
        self.updatePostRadioVBox.pack_start(self.addUserRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.rmUserRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.addGroupRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.rmGroupRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.addToGroupRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.rmFromGroupRadio, False, False, 5)

        #Pack the VBox into the HBox so we can pack it into the greater VBox shortly.
        self.userManageHBoxTop.pack_start(self.updatePostRadioVBox, False, False, 200)
        
        #Now the buttons to direct us from here
        self.returnMainMenuButton = gtk.Button(" Main Menu ")
        self.returnMainMenuButton.connect("clicked", self.transToMain, self.userManagementVBox)
        self.userManageHBoxBottom.pack_start(self.returnMainMenuButton, True, True, 30)

        #Pack it all Up in VBox
        self.userManagementVBox.pack_start(self.userManageLabel, False, False, 15)
        self.userManagementVBox.pack_start(self.userManageHBoxTop, False, False, 10)
        self.userManagementVBox.pack_end(self.userManageHBoxBottom, False, False, 15)

        #show it all off
        self.userManageLabel.show()
        self.addUserRadio.show()
        self.rmUserRadio.show()
        self.addGroupRadio.show()
        self.rmGroupRadio.show()
        self.addToGroupRadio.show()
        self.rmFromGroupRadio.show()
        self.returnMainMenuButton.show()
        self.userManageHBoxBottom.show()
        self.updatePostRadioVBox.show()
        self.userManageHBoxTop.show()
        self.userManagementVBox.show()
    
        #Add to Window
        self.mainWindow.add(self.userManagementVBox)
        
    def addUser(self, widget=None, data=None):
        self.addUserDia = gtk.Dialog("Add User", self.mainWindow)
        okButton = gtk.Button("Submit", gtk.STOCK_OK)
        cancel = gtk.Button("Cancel", gtk.STOCK_CANCEL)
        userLabel = gtk.Label("Username: ")
        self.userEntry = gtk.Entry()
        passLabel = gtk.Label("Password: ")
        self.passEntry = gtk.Entry()
        nameLabel = gtk.Label("Full Name: ")
        self.nameEntry = gtk.Entry()
        emailLabel = gtk.Label("Email: ")
        self.emailEntry = gtk.Entry()
        
        #Buttons
        okButton.connect("clicked", self.rpc_addUser)
        cancel.connect("clicked", self.removeDialog, self.addUserDia)
        self.addUserDia.action_area.pack_start(cancel, True, True, 0)
        self.addUserDia.action_area.pack_end(okButton, True, True, 5)
        
        #Entries/Labels
        userHBox = gtk.HBox(False, 0)
        passHBox = gtk.HBox(False, 0)
        emailHBox = gtk.HBox(False, 0)
        nameHBox = gtk.HBox(False, 0)
        userHBox.pack_start(userLabel, True, True, 0)
        userHBox.pack_end(self.userEntry, True, True, 0)
        passHBox.pack_start(passLabel, True, True, 0)
        passHBox.pack_end(self.passEntry, True, True, 0)
        nameHBox.pack_start(nameLabel, True, True, 0)
        nameHBox.pack_end(self.nameEntry, True, True, 0)
        emailHBox.pack_start(emailLabel, True, True, 0)
        emailHBox.pack_end(self.emailEntry, True, True, 0)
        
        #Pack it Up
        self.addUserDia.vbox.pack_start(userHBox, True, True, 0)
        self.addUserDia.vbox.pack_start(passHBox, True, True, 0)
        self.addUserDia.vbox.pack_start(nameHBox, True, True, 0)
        self.addUserDia.vbox.pack_start(emailHBox, True, True, 0)
        
        #Show it all off
        okButton.show()
        cancel.show()
        userLabel.show()
        self.userEntry.show()
        passLabel.show()
        self.passEntry.show()
        nameLabel.show()
        self.nameEntry.show()
        emailLabel.show()
        self.emailEntry.show()
        userHBox.show()
        passHBox.show()
        nameHBox.show()
        emailHBox.show()
        self.addUserDia.show() 
        
    def rpc_addUser(self, widget=None, data=None):
        userDict = {"name":self.userEntry.get_text(), "fullname":self.nameEntry.get_text(), "email":self.emailEntry.get_text()}
        try:
            result = server.confluence1.addUser(self.token, userDict, self.passEntry.get_text())
            userDialog = gtk.Dialog("Success", self.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.removeDialog, userDialog)
            label = gtk.Label("User '%s' Added Successfully" % self.userEntry.get_text())
            userDialog.vbox.pack_start(label, True, True, 0)
            userDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            userDialog.show()
        except xmlrpclib.Fault:
            self.errDialog("           User Add Failed \n User Likely Exists Already              ")
    
    def removeUser(self, widget=None, data=None):
        self.rmUserDia = gtk.Dialog("Remove User", self.mainWindow)
        okButton = gtk.Button("Submit", gtk.STOCK_OK)
        cancel = gtk.Button("Cancel", gtk.STOCK_CANCEL)
        userLabel = gtk.Label("Username: ")
        self.userEntry = gtk.Entry()
        
        #Buttons
        okButton.connect("clicked", self.rpc_removeUser)
        cancel.connect("clicked", self.removeDialog, self.rmUserDia)
        self.rmUserDia.action_area.pack_start(cancel, True, True, 0)
        self.rmUserDia.action_area.pack_end(okButton, True, True, 5)
        
        #Entries/Labels
        userHBox = gtk.HBox(False, 0)
        userHBox.pack_start(userLabel, True, True, 0)
        userHBox.pack_end(self.userEntry, True, True, 0)
        
        #Pack it Up
        self.rmUserDia.vbox.pack_start(userHBox, True, True, 0)
        
        #Show it all off
        okButton.show()
        cancel.show()
        userLabel.show()
        self.userEntry.show()
        userHBox.show()
        self.rmUserDia.show() 
    
    def rpc_removeUser(self, widget=None, data=None):
        try:
            result = server.confluence1.removeUser(self.token, self.userEntry.get_text())
            userDialog = gtk.Dialog("Success", self.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.removeDialog, userDialog)
            label = gtk.Label("User '%s' Removed Successfully" % self.userEntry.get_text())
            userDialog.vbox.pack_start(label, True, True, 0)
            userDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            userDialog.show()
        except xmlrpclib.Fault:
            self.errDialog("           User removal failed.\n User likely doesn't exist              ")
    
    def addGroup(self, widget=None, data=None):
        self.addGroupDia = gtk.Dialog("Add Group", self.mainWindow)
        okButton = gtk.Button("Submit", gtk.STOCK_OK)
        cancel = gtk.Button("Cancel", gtk.STOCK_CANCEL)
        groupLabel = gtk.Label("Group Name: ")
        self.groupEntry = gtk.Entry()
        
        #Buttons
        okButton.connect("clicked", self.rpc_addGroup)
        cancel.connect("clicked", self.removeDialog, self.addGroupDia)
        self.addGroupDia.action_area.pack_start(cancel, True, True, 0)
        self.addGroupDia.action_area.pack_end(okButton, True, True, 5)
        
        #Entries/Labels
        addGroupHBox = gtk.HBox(False, 0)
        addGroupHBox.pack_start(groupLabel, True, True, 0)
        addGroupHBox.pack_end(self.groupEntry, True, True, 0)
        
        #Pack it Up
        self.addGroupDia.vbox.pack_start(addGroupHBox, True, True, 0)
        
        #Show it all off
        okButton.show()
        cancel.show()
        groupLabel.show()
        self.groupEntry.show()
        addGroupHBox.show()
        self.addGroupDia.show()
    
    def rpc_addGroup(self, widget=None, data=None):
        try:
            result = server.confluence1.addGroup(self.token, self.groupEntry.get_text())
            userDialog = gtk.Dialog("Success", self.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.removeDialog, userDialog)
            label = gtk.Label("Group '%s' Added Successfully" % self.groupEntry.get_text())
            userDialog.vbox.pack_start(label, True, True, 0)
            userDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            userDialog.show()
        except xmlrpclib.Fault:
            self.errDialog("           Group Addition Failed. \n You either lack the proper permissions, or the group exists.              ")
    
    def removeGroup(self, widget=None, data=None):
        self.rmGroupDia = gtk.Dialog("Remove Group", self.mainWindow)
        okButton = gtk.Button("Submit", gtk.STOCK_OK)
        cancel = gtk.Button("Cancel", gtk.STOCK_CANCEL)
        groupLabel = gtk.Label("Group Name: ")
        self.groupEntry = gtk.Entry()
        
        #Buttons
        okButton.connect("clicked", self.rpc_removeGroup)
        cancel.connect("clicked", self.removeDialog, self.rmGroupDia)
        self.rmGroupDia.action_area.pack_start(cancel, True, True, 0)
        self.rmGroupDia.action_area.pack_end(okButton, True, True, 5)
        
        #Entries/Labels
        rmGroupHBox = gtk.HBox(False, 0)
        rmGroupHBox.pack_start(groupLabel, True, True, 0)
        rmGroupHBox.pack_end(self.groupEntry, True, True, 0)
        
        #Pack it Up
        self.rmGroupDia.vbox.pack_start(rmGroupHBox, True, True, 0)
        
        #Show it all off
        okButton.show()
        cancel.show()
        groupLabel.show()
        self.groupEntry.show()
        rmGroupHBox.show()
        self.rmGroupDia.show()
    
    def rpc_removeGroup(self, widget=None, data=None):
        try:
            result = server.confluence1.removeGroup(self.token, self.groupEntry.get_text(), "")
            userDialog = gtk.Dialog("Success", self.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.removeDialog, userDialog)
            label = gtk.Label("Group '%s' Removed Successfully" % self.groupEntry.get_text())
            userDialog.vbox.pack_start(label, True, True, 0)
            userDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            userDialog.show()
        except xmlrpclib.Fault:
            self.errDialog("           \tGroup Removal Failed. \n You either lack the proper permissions, or the group doesn't exist.              ")
    
    def addToGroup(self, widget=None, data=None):
        self.addUserDia = gtk.Dialog("Add User to Group", self.mainWindow)
        okButton = gtk.Button("Submit", gtk.STOCK_OK)
        cancel = gtk.Button("Cancel", gtk.STOCK_CANCEL)
        userLabel = gtk.Label("Username: ")
        self.userEntry = gtk.Entry()
        groupLabel = gtk.Label("Group: ")
        self.groupEntry = gtk.Entry()
        
        #Buttons
        okButton.connect("clicked", self.rpc_addToGroup)
        cancel.connect("clicked", self.removeDialog, self.addUserDia)
        self.addUserDia.action_area.pack_start(cancel, True, True, 0)
        self.addUserDia.action_area.pack_end(okButton, True, True, 5)
        
        #Entries/Labels
        userHBox = gtk.HBox(False, 0)
        groupHBox = gtk.HBox(False, 0)
        userHBox.pack_start(userLabel, True, True, 0)
        userHBox.pack_end(self.userEntry, True, True, 0)
        groupHBox.pack_start(groupLabel, True, True, 0)
        groupHBox.pack_end(self.groupEntry, True, True, 0)
        
        #Pack it Up
        self.addUserDia.vbox.pack_start(userHBox, True, True, 0)
        self.addUserDia.vbox.pack_start(groupHBox, True, True, 0)
        
        #Show it all off
        okButton.show()
        cancel.show()
        userLabel.show()
        self.userEntry.show()
        groupLabel.show()
        self.groupEntry.show()
        userHBox.show()
        groupHBox.show()
        self.addUserDia.show()
    
    def rpc_addToGroup(self, widget=None, data=None):
        try:
            result = server.confluence1.addUserToGroup(self.token, self.userEntry.get_text(), self.groupEntry.get_text())
            userDialog = gtk.Dialog("Success", self.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.removeDialog, userDialog)
            label = gtk.Label("User Added to '%s' Successfully" % self.groupEntry.get_text())
            userDialog.vbox.pack_start(label, True, True, 0)
            userDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            userDialog.show()
        except xmlrpclib.Fault:
            self.errDialog("\t\tFailed to add user to Group.\n\t\tPlease check your permission level")
    
    def removeFromGroup(self, widget=None, data=None):
        self.addUserDia = gtk.Dialog("Add User to Group", self.mainWindow)
        okButton = gtk.Button("Submit", gtk.STOCK_OK)
        cancel = gtk.Button("Cancel", gtk.STOCK_CANCEL)
        userLabel = gtk.Label("Username: ")
        self.userEntry = gtk.Entry()
        groupLabel = gtk.Label("Group: ")
        self.groupEntry = gtk.Entry()
        
        #Buttons
        okButton.connect("clicked", self.rpc_removeFromGroup)
        cancel.connect("clicked", self.removeDialog, self.addUserDia)
        self.addUserDia.action_area.pack_start(cancel, True, True, 0)
        self.addUserDia.action_area.pack_end(okButton, True, True, 5)
        
        #Entries/Labels
        userHBox = gtk.HBox(False, 0)
        groupHBox = gtk.HBox(False, 0)
        userHBox.pack_start(userLabel, True, True, 0)
        userHBox.pack_end(self.userEntry, True, True, 0)
        groupHBox.pack_start(groupLabel, True, True, 0)
        groupHBox.pack_end(self.groupEntry, True, True, 0)
        
        #Pack it Up
        self.addUserDia.vbox.pack_start(userHBox, True, True, 0)
        self.addUserDia.vbox.pack_start(groupHBox, True, True, 0)
        
        #Show it all off
        okButton.show()
        cancel.show()
        userLabel.show()
        self.userEntry.show()
        groupLabel.show()
        self.groupEntry.show()
        userHBox.show()
        groupHBox.show()
        self.addUserDia.show()
    
    def rpc_removeFromGroup(self, widget=None, data=None):
        try:
            result = server.confluence1.removeUserFromGroup(self.token, self.userEntry.get_text(), self.groupEntry.get_text())
            userDialog = gtk.Dialog("Success", self.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.removeDialog, userDialog)
            label = gtk.Label("User Removed From '%s' Successfully" % self.groupEntry.get_text())
            userDialog.vbox.pack_start(label, True, True, 0)
            userDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            userDialog.show()
        except xmlrpclib.Fault:
            self.errDialog("\t\tFailed to add user to Group.\n\t\tPlease check your permission level")
                
    def searchConfluence(self, widget):
        self.mainWindow.remove(self.menuVBox)

        #Main boxes
        self.searchVBox = gtk.VBox(False, 0)
        self.searchHBox = gtk.HBox(False, 0)
        self.searchButtonsHBox = gtk.HBox(False, 0)

        #Title
        self.searchTitle = gtk.Label("Search Your Confluence Instance")

        #Search Section
        self.searchLabel = gtk.Label("Search: ")
        self.searchEntry = gtk.Entry()
        
        #Results
        self.searchView = gtk.TextView()
        self.searchView.set_editable(False)
        self.searchView.set_wrap_mode(gtk.WRAP_WORD)
        self.searchWindow = gtk.ScrolledWindow()
        self.searchWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.searchWindow.add(self.searchView)
        self.searchBuffer = self.searchView.get_buffer()
        self.searchBuffer.set_text("Results will be displayed here")
        self.searchHBox.pack_start(self.searchLabel, False, False, 0)
        self.searchHBox.pack_start(self.searchEntry, False, False, 0)

        #Buttons
        self.returnMainMenuButton = gtk.Button(" Main Menu ")
        self.returnMainMenuButton.connect("clicked", self.transToMain, self.searchVBox)
        self.searchSubmit = gtk.Button(" Search ")
        self.searchSubmit.connect("clicked", self.rpc_search)
        self.searchButtonsHBox.pack_start(self.returnMainMenuButton, True, True, 0)
        self.searchButtonsHBox.pack_start(self.searchSubmit, True, True, 0)

        #Pack it All Up
        self.searchVBox.pack_start(self.searchTitle, False, True, 0)
        self.searchVBox.pack_start(self.searchHBox, False, True, 15)
        self.searchVBox.pack_start(self.searchWindow, True, True, 0)
        self.searchVBox.pack_end(self.searchButtonsHBox, False, True, 0)

        #Show it All Off
        self.searchTitle.show()
        self.searchLabel.show()
        self.searchEntry.show()
        self.searchView.show()
        self.searchWindow.show()
        self.searchSubmit.show()
        self.returnMainMenuButton.show()
        self.searchButtonsHBox.show()
        self.searchHBox.show()
        self.searchVBox.show()
        self.mainWindow.add(self.searchVBox)

    def rpc_search(self, widget=None, data=None):
        self.searchBuffer.set_text("")
        try:
            results = self.server.confluence1.search(self.token, self.searchEntry.get_text(), 50)
            tempFile = open("/tmp/confSearch.tmp", "w")
            if tempFile:
                if results != "":
                    for i in results:
                        tempFile.write("Title: \t %s \n" % i["title"])
                        tempFile.write("URL: \t %s \n" % i["url"])
                        tempFile.write("Excerpt: \t %s \n\n" % i["excerpt"])
                tempFile.close()

            infile = open("/tmp/confSearch.tmp", "r")
            if infile:
                searchResults = infile.read()
                infile.close()
                self.searchBuffer.set_text(searchResults)

            os.remove("/tmp/confSearch.tmp")
        
        except xmlrpclib.Fault:
            self.errDialog("Search failed, and can be finicky at times.\nPlease try different search terms")
            
        except:
            self.errDialog("\t\tConnection Failed\t\t")

    def contentManagement(self, widget):
        #Remove the current VBox
        self.mainWindow.remove(self.menuVBox)

        #Create our new Vbox
        self.contentManagementVBox = gtk.VBox(False, 0)
        
        #Content Label
        self.contentManageLabel = gtk.Label("Choose Your Content Options Below")

        #Couple of HBoxes to hold Radio buttons
        self.contentManageHBoxTop = gtk.HBox(False, 0)
        self.contentManageHBoxBottom = gtk.HBox(False,0)
        
        #Radio Buttons Center
        self.updatePostRadioVBox = gtk.VBox(False, 0)
        self.updatePageRadio = gtk.Button("Updating Page")
#        self.updatePostRadio = gtk.Button("Updating Blog Post")
        self.pageRadio = gtk.Button("New Page")
        self.blogRadio = gtk.Button("New Blog Post")
        self.addSpaceRadio = gtk.Button("Add New Space")
        self.removePageRadio = gtk.Button("Remove Page")
#        self.removePostRadio = gtk.Button("Remove Blog Post")
        self.removeSpaceRadio = gtk.Button("Remove Space")

        #Connect the Buttons to Funcs
        self.updatePageRadio.connect("clicked", self.updatePage)
#        self.updatePostRadio.connect("clicked", self.updatePost)
        self.pageRadio.connect("clicked", self.newPage)
        self.blogRadio.connect("clicked", self.newBlogPost)
        self.addSpaceRadio.connect("clicked", self.newSpace)
        self.removePageRadio.connect("clicked", self.removePage)
#        self.removePostRadio.connect("clicked", self.removeBlogPost)
        self.removeSpaceRadio.connect("clicked", self.removeSpace)

        #Pack All the Radio Buttons
        self.updatePostRadioVBox.pack_start(self.updatePageRadio, False, False, 5)
#        self.updatePostRadioVBox.pack_start(self.updatePostRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.pageRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.blogRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.addSpaceRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.removePageRadio, False, False, 5)
#        self.updatePostRadioVBox.pack_start(self.removePostRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.removeSpaceRadio, False, False, 5)

        #Pack the VBox into the HBox so we can pack it into the greater VBox shortly.
        self.contentManageHBoxTop.pack_start(self.updatePostRadioVBox, False, False, 200)
        
        #Now the buttons to direct us from here
        self.returnMainMenuButton = gtk.Button(" Main Menu ")
        self.returnMainMenuButton.connect("clicked", self.transToMain, self.contentManagementVBox)
        self.contentManageHBoxBottom.pack_start(self.returnMainMenuButton, True, True, 30)

        #Pack it all Up in VBox
        self.contentManagementVBox.pack_start(self.contentManageLabel, False, False, 15)
        self.contentManagementVBox.pack_start(self.contentManageHBoxTop, False, False, 10)
        self.contentManagementVBox.pack_end(self.contentManageHBoxBottom, False, False, 15)

        #show it all off
        self.contentManageLabel.show()
        self.updatePageRadio.show()
        self.pageRadio.show()
        self.blogRadio.show()
#        self.updatePostRadio.show()
        self.addSpaceRadio.show()
        self.removePageRadio.show()
#        self.removePostRadio.show()
        self.removeSpaceRadio.show()
        self.returnMainMenuButton.show()
        self.contentManageHBoxBottom.show()
        self.updatePostRadioVBox.show()
        self.contentManageHBoxTop.show()
        self.contentManagementVBox.show()
    
        #Add to Window
        self.mainWindow.add(self.contentManagementVBox)    

    def transToMain(self, widget=None, data=None):
        self.mainWindow.remove(data)
        self.launchPad()    

    def updatePost(self, widget=None):
        print "updatePost"
        pass
    
    def updatePage(self, widget=None):
        self.mainWindow.remove(self.contentManagementVBox)
        
        #Set up the core of the window
        self.updatePageVBox = gtk.VBox(False, 0)
        self.updatePageScroll = gtk.ScrolledWindow()
        self.updatePageScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.updatePageTextView = gtk.TextView()
        self.updatePageTextView.set_cursor_visible(True)
        self.updatePageTextView.set_wrap_mode(gtk.WRAP_WORD)
        self.updatePageTextBuffer = self.updatePageTextView.get_buffer()

        #Button to Grab Current Content
        self.updateContentButton = gtk.Button("Grab Existing Page")
        self.updateContentButton.connect("clicked", self.grabContent)

        #Space Key
        self.updatePageHBox1 = gtk.HBox(False, 0)
        self.updatePageKeyLabel = gtk.Label("Space Key: ")
        self.updatePageKey = gtk.Entry()
        self.updatePageLabel = gtk.Label("Title: ")
        self.updatePagePostTitle = gtk.Entry()
        self.updatePageHBox1.pack_start(self.updatePageKeyLabel, False, False, 0)
        self.updatePageHBox1.pack_start(self.updatePageKey, False, False, 0)
        self.updatePageHBox1.pack_end(self.updatePagePostTitle, False, False, 0)
        self.updatePageHBox1.pack_end(self.updatePageLabel, False, False, 0)

        #Submit that shit
        self.returnMainMenuButton = gtk.Button(" Main Menu ")
        self.returnMainMenuButton.connect("clicked", self.transToMain, self.updatePageVBox)
        self.updatePageHBox2 = gtk.HBox(False, 0)
        self.updatePageHBox2.pack_start(self.returnMainMenuButton, True, True, 0)
        self.updatePageButton = gtk.Button("Submit")
        self.updatePageButton.connect("clicked", self.rpc_updatePage)
        self.updatePageHBox2.pack_start(self.updatePageButton, True, True, 0)

        #Page Title
        self.updatePageTitle = gtk.Label("Add New Page to Confluence")

        #Pack it all in
        self.updatePageScroll.add(self.updatePageTextView)
        self.updatePageVBox.pack_start(self.updatePageTitle, False, False, 0)
        self.updatePageVBox.pack_start(self.updatePageHBox1, False, False, 10)
        self.updatePageVBox.pack_start(self.updateContentButton, False, True, 10)
        self.updatePageVBox.pack_start(self.updatePageScroll, True, True, 0)
        self.updatePageVBox.pack_end(self.updatePageHBox2, False, False, 10)
        
        #Show it all off
        self.updatePageScroll.show()
        self.updatePageTextView.show()
        self.updatePageVBox.show()
        self.updatePageKeyLabel.show()
        self.updatePageKey.show()
        self.updatePageTitle.show()
        self.updatePageLabel.show()
        self.updatePagePostTitle.show()
        self.updatePageButton.show()
        self.updateContentButton.show()
        self.returnMainMenuButton.show()
        self.updatePageHBox1.show()
        self.updatePageHBox2.show()
        self.mainWindow.add(self.updatePageVBox)

    def grabContent(self, widget=None):
        try:
            self.pageText = self.server.confluence1.getPage(self.token, self.updatePageKey.get_text(), self.updatePagePostTitle.get_text())
            self.updatePageTextBuffer.set_text(self.pageText["content"])
            self.updatePageTextView.set_buffer(self.updatePageTextBuffer)
        except xmlrpclib.Fault:
            self.errDialog("\t\tPage Updating Failed\t\t\nPage either doesn't exist, or you lack permission")

    def rpc_updatePage(self, widget=None):
        try:
            startiter, enditer = self.updatePageTextBuffer.get_bounds()
            self.pageText["content"] = self.updatePageTextBuffer.get_text(startiter,enditer)
            result = self.server.confluence1.storePage(self.token, self.pageText)
            updatePageDialog = gtk.Dialog("Success", self.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.removeDialog, updatePageDialog)
            label = gtk.Label("Page updated Successfully")
            updatePageDialog.vbox.pack_start(label, True, True, 0)
            updatePageDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            updatePageDialog.show()
        except xmlrpclib.Fault:
            self.errDialog("\t\tPage Updating Failed\t\t\nPage either doesn't exist, or you lack permission")


    def newPage(self, widget=None):
        self.mainWindow.remove(self.contentManagementVBox)
        
        #Set up the core of the window
        self.newPageVBox = gtk.VBox(False, 0)
        self.newPageScroll = gtk.ScrolledWindow()
        self.newPageScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.newPageTextView = gtk.TextView()
        self.newPageTextView.set_cursor_visible(True)
        self.newPageTextView.set_wrap_mode(gtk.WRAP_WORD)
        self.newPageTextBuffer = self.newPageTextView.get_buffer()

        #Space Key
        self.newPageHBox1 = gtk.HBox(False, 0)
        self.newPageKeyLabel = gtk.Label("Space Key: ")
        self.newPageKey = gtk.Entry()
        self.newPageLabel = gtk.Label("Title: ")
        self.newPagePostTitle = gtk.Entry()
        self.newPageHBox1.pack_start(self.newPageKeyLabel, False, False, 0)
        self.newPageHBox1.pack_start(self.newPageKey, False, False, 0)
        self.newPageHBox1.pack_end(self.newPagePostTitle, False, False, 0)
        self.newPageHBox1.pack_end(self.newPageLabel, False, False, 0)

        #Submit that shit
        self.returnMainMenuButton = gtk.Button(" Main Menu ")
        self.returnMainMenuButton.connect("clicked", self.transToMain, self.newPageVBox)
        self.newPageHBox2 = gtk.HBox(False, 0)
        self.newPageHBox2.pack_start(self.returnMainMenuButton, True, True, 0)
        self.newPageButton = gtk.Button("Submit")
        self.newPageButton.connect("clicked", self.rpc_newPage)
        self.newPageHBox2.pack_start(self.newPageButton, True, True, 0)

        #Page Title
        self.newPageTitle = gtk.Label("Add New Page to Confluence")

        #Pack it all in
        self.newPageScroll.add(self.newPageTextView)
        self.newPageVBox.pack_start(self.newPageTitle, False, False, 0)
        self.newPageVBox.pack_start(self.newPageHBox1, False, False, 10)
        self.newPageVBox.pack_start(self.newPageScroll, True, True, 0)
        self.newPageVBox.pack_end(self.newPageHBox2, False, False, 10)
        
        #Show it all off
        self.newPageScroll.show()
        self.newPageTextView.show()
        self.newPageVBox.show()
        self.newPageKeyLabel.show()
        self.newPageKey.show()
        self.newPageTitle.show()
        self.newPageLabel.show()
        self.newPagePostTitle.show()
        self.newPageButton.show()
        self.returnMainMenuButton.show()
        self.newPageHBox1.show()
        self.newPageHBox2.show()
        self.mainWindow.add(self.newPageVBox)

    def rpc_newPage(self, widget=None):
        try:
            startiter, enditer = self.newPageTextBuffer.get_bounds()
            newPost = {"title":self.newPagePostTitle.get_text(), "space":self.newPageKey.get_text(), "content":self.newPageTextBuffer.get_text(startiter, enditer)}
            result = self.server.confluence1.storePage(self.token, newPost)
            newPageDialog = gtk.Dialog("Success", self.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.removeDialog, newPageDialog)
            label = gtk.Label("Page created Successfully")
            newPageDialog.vbox.pack_start(label, True, True, 0)
            newPageDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            newPageDialog.show()
        except xmlrpclib.Fault:
            self.errDialog("\t\tPage Creation Failed\t\t\nPage either exists, or you lack permission")
    
    def newBlogPost(self, widget=None):
        self.mainWindow.remove(self.contentManagementVBox)
        
        #Set up the core of the window
        self.newPostVBox = gtk.VBox(False, 0)
        self.newPostScroll = gtk.ScrolledWindow()
        self.newPostScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.newPostTextView = gtk.TextView()
        self.newPostTextView.set_cursor_visible(True)
        self.newPostTextView.set_wrap_mode(gtk.WRAP_WORD)
        self.newPostTextBuffer = self.newPostTextView.get_buffer()

        #Space Key
        self.newPostHBox1 = gtk.HBox(False, 0)
        self.newPostKeyLabel = gtk.Label("Space Key: ")
        self.newPostKey = gtk.Entry()
        self.newPostLabel = gtk.Label("Title: ")
        self.newPostPostTitle = gtk.Entry()
        self.newPostHBox1.pack_start(self.newPostKeyLabel, False, False, 0)
        self.newPostHBox1.pack_start(self.newPostKey, False, False, 0)
        self.newPostHBox1.pack_end(self.newPostPostTitle, False, False, 0)
        self.newPostHBox1.pack_end(self.newPostLabel, False, False, 0)

        #Submit that shit
        self.returnMainMenuButton = gtk.Button(" Main Menu ")
        self.returnMainMenuButton.connect("clicked", self.transToMain, self.newPostVBox)
        self.newPostHBox2 = gtk.HBox(False, 0)
        self.newPostHBox2.pack_start(self.returnMainMenuButton, True, True, 0)
        self.newPostButton = gtk.Button("Submit")
        self.newPostButton.connect("clicked", self.rpc_newPost)
        self.newPostHBox2.pack_start(self.newPostButton, True, True, 0)

        #Post Title
        self.newPostTitle = gtk.Label("Add New Post to Confluence")

        #Pack it all in
        self.newPostScroll.add(self.newPostTextView)
        self.newPostVBox.pack_start(self.newPostTitle, False, False, 0)
        self.newPostVBox.pack_start(self.newPostHBox1, False, False, 10)
        self.newPostVBox.pack_start(self.newPostScroll, True, True, 0)
        self.newPostVBox.pack_end(self.newPostHBox2, False, False, 10)
        
        #Show it all off
        self.newPostScroll.show()
        self.newPostTextView.show()
        self.newPostVBox.show()
        self.newPostKeyLabel.show()
        self.newPostKey.show()
        self.newPostTitle.show()
        self.newPostLabel.show()
        self.newPostPostTitle.show()
        self.newPostButton.show()
        self.returnMainMenuButton.show()
        self.newPostHBox1.show()
        self.newPostHBox2.show()
        self.mainWindow.add(self.newPostVBox)

    def rpc_newPost(self, widget=None, data=None):
        try:
            startiter, enditer = self.newPostTextBuffer.get_bounds()
            newPost = {"title":self.newPostPostTitle.get_text(), "space":self.newPostKey.get_text(), "content":self.newPostTextBuffer.get_text(startiter, enditer)}
            result = self.server.confluence1.storeBlogEntry(self.token, newPost)
            newPostDialog = gtk.Dialog("Success", self.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.removeDialog, newPostDialog)
            label = gtk.Label("Post created Successfully")
            newPostDialog.vbox.pack_start(label, True, True, 0)
            newPostDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            newPostDialog.show()
        except xmlrpclib.Fault:
            self.errDialog("\t\tBlog Post Creation Failed\t\t\nTitle either exists, Space doesn't, or you lack permission")


    def newSpace(self, widget=None):
        self.mainWindow.remove(self.contentManagementVBox)

        #Setup our VBox
        self.newSpaceVBox = gtk.VBox(False, 0)
        self.newSpaceMainTitle = gtk.Label("Add a new Space to Confluence")

        #Setup our HBoxes (4)
        self.newSpaceTitleHBox = gtk.HBox(False, 0)
        self.newSpaceKeyHBox = gtk.HBox(False, 0)
        self.newSpaceDescHBox = gtk.HBox(False, 0)
        self.newSpaceButtonsHBox = gtk.HBox(False, 0)

        #Return to Main Menu
        self.returnMainMenuButton = gtk.Button(" Main Menu ")
        self.returnMainMenuButton.connect("clicked", self.transToMain, self.newSpaceVBox)

        #Submit to Confluence
        self.newSpaceSubmit = gtk.Button(" Submit ")
        self.newSpaceSubmit.connect("clicked", self.rpc_addSpace)

        #Pack up the Buttons
        self.newSpaceButtonsHBox.pack_start(self.returnMainMenuButton, True, True, 0)
        self.newSpaceButtonsHBox.pack_start(self.newSpaceSubmit, True, True, 0)

        #Now the meat
        self.newSpaceTitleLabel = gtk.Label("Space Title: ")
        self.newSpaceTitleEntry = gtk.Entry()
        self.newSpaceTitleHBox.pack_start(self.newSpaceTitleLabel, True, True, 0)
        self.newSpaceTitleHBox.pack_start(self.newSpaceTitleEntry, True, True, 5)

        self.newSpaceKeyLabel = gtk.Label("Space Key: ")
        self.newSpaceKeyEntry = gtk.Entry()
        self.newSpaceKeyHBox.pack_start(self.newSpaceKeyLabel, True, True, 0)
        self.newSpaceKeyHBox.pack_start(self.newSpaceKeyEntry, True, True, 5)

        self.newSpaceDescLabel = gtk.Label("Description: ")
        self.newSpaceDescEntry = gtk.Entry()
        self.newSpaceDescHBox.pack_start(self.newSpaceDescLabel, True, True, 0)
        self.newSpaceDescHBox.pack_start(self.newSpaceDescEntry, True, True, 5)

        #Pack it all Up
        self.newSpaceVBox.pack_start(self.newSpaceMainTitle, False, True, 0)
        self.newSpaceVBox.pack_start(self.newSpaceTitleHBox, False, False, 40)
        self.newSpaceVBox.pack_start(self.newSpaceKeyHBox, False, False, 40)
        self.newSpaceVBox.pack_start(self.newSpaceDescHBox, False, False, 40)
        self.newSpaceVBox.pack_start(self.newSpaceButtonsHBox, False, False, 40)

        #Show it all Off
        self.returnMainMenuButton.show()
        self.newSpaceSubmit.show()
        self.newSpaceTitleLabel.show()
        self.newSpaceTitleEntry.show()
        self.newSpaceKeyLabel.show()
        self.newSpaceKeyEntry.show()
        self.newSpaceDescLabel.show()
        self.newSpaceDescEntry.show()
        self.newSpaceMainTitle.show()
        self.newSpaceTitleHBox.show()
        self.newSpaceKeyHBox.show()
        self.newSpaceDescHBox.show()
        self.newSpaceButtonsHBox.show()
        self.newSpaceVBox.show()
        self.mainWindow.add(self.newSpaceVBox)

    def rpc_addSpace(self, widget=None, data=None):
        try:
            space = {"key":self.newSpaceKeyEntry.get_text(),"name":self.newSpaceTitleEntry.get_text(),"description":self.newSpaceDescEntry.get_text()}
            result = self.server.confluence1.addSpace(self.token, space)
            newPageDialog = gtk.Dialog("Success", self.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.removeDialog, newPageDialog)
            label = gtk.Label("Space Added Successfully")
            newPageDialog.vbox.pack_start(label, True, True, 0)
            newPageDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            newPageDialog.show()
        except xmlrpclib.Fault:
            self.errDialog("\t\tSpace Creation Failed\t\t\nSpace either exists or you lack permission")

    def removePage(self, widget=None):
        self.mainWindow.remove(self.contentManagementVBox)

        #Setup our VBox
        self.removePageMainVBox = gtk.VBox(False, 0)
        self.removePageTitle = gtk.Label("Removing Page From Confluence")

        #Return to Main Menu
        self.returnMainMenuButton = ""
        self.returnMainMenuButton = gtk.Button(" Main Menu ")
        self.returnMainMenuButton.connect("clicked", self.transToMain, self.removePageMainVBox)

        #Our Submit Button
        self.removePageSubmit = gtk.Button("Submit")
        self.removePageSubmit.connect("clicked", self.rpc_removePage)

        #Button HBox
        self.removePageButtonHBox = gtk.HBox(False, 0)
        self.removePageButtonHBox.pack_start(self.returnMainMenuButton, True, True, 0)
        self.removePageButtonHBox.pack_start(self.removePageSubmit, True, True, 0)

        #Our Space Key Items
        self.removePageKeyHBox = gtk.HBox(False, 0)
        self.removePageKeyLabel = gtk.Label("Space: ")
        self.removePageKeyEntry = gtk.Entry()
        self.removePageKeyHBox.pack_start(self.removePageKeyLabel, False, False, 0)
        self.removePageKeyHBox.pack_start(self.removePageKeyEntry, True, True, 0)

        #Our Page Title Options
        self.removePageTitleHBox = gtk.HBox(False, 0)
        self.removePageTitleLabel = gtk.Label("Page Title: ")
        self.removePageTitleEntry = gtk.Entry()
        self.removePageTitleHBox.pack_start(self.removePageTitleLabel, False, False, 0)
        self.removePageTitleHBox.pack_start(self.removePageTitleEntry, True, True, 0)        

        #Pack it All Up
        self.removePageMainVBox.pack_start(self.removePageTitle, False, True, 0)
        self.removePageMainVBox.pack_start(self.removePageKeyHBox, False, False, 40)
        self.removePageMainVBox.pack_start(self.removePageTitleHBox, False, False, 40)
        self.removePageMainVBox.pack_start(self.removePageButtonHBox, False, False, 60)
        
        #Show it all Off
        self.removePageTitle.show()
        self.returnMainMenuButton.show()
        self.removePageSubmit.show()
        self.removePageKeyHBox.show()
        self.removePageKeyLabel.show()
        self.removePageKeyEntry.show()
        self.removePageButtonHBox.show()
        self.removePageTitleLabel.show()
        self.removePageTitleEntry.show()
        self.removePageTitleHBox.show()
        self.removePageMainVBox.show()
        self.mainWindow.add(self.removePageMainVBox)

    def rpc_removePage(self, widget=None):
        try:
            page = self.server.confluence1.getPage(self.token, self.removePageKeyEntry.get_text(), self.removePageTitleEntry.get_text())
            result = self.server.confluence1.removePage(self.token, page["id"])
            newPageDialog = gtk.Dialog("Success", self.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.removeDialog, newPageDialog)
            label = gtk.Label("Page Removed Successfully")
            newPageDialog.vbox.pack_start(label, True, True, 0)
            newPageDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            newPageDialog.show()
        except xmlrpclib.Fault:
            self.errDialog("\t\tPage Removal Failed\t\t\nPage either doesn't exist, or you lack permission")

    def removeSpace(self, widget=None):
        self.removeSpaceDialog = gtk.Dialog("Remove Space", self.mainWindow)
        button = gtk.Button("Okay", gtk.STOCK_OK)
        cancel = gtk.Button("Cancel", gtk.STOCK_CANCEL)
        self.removeSpaceEntry = gtk.Entry()
        cancel.connect("clicked", self.removeDialog, self.removeSpaceDialog)
        button.connect("clicked", self.rpc_removeSpace)
        label = gtk.Label("Space Key to Destroy: ")
        removeSpaceHBox = gtk.HBox(False, 0)
        removeSpaceHBox.pack_start(label, False, False, 0)
        removeSpaceHBox.pack_end(self.removeSpaceEntry, False, False, 0)
        button.show()
        label.show()
        self.removeSpaceEntry.show()
        cancel.show()
        removeSpaceHBox.show()
        self.removeSpaceDialog.vbox.pack_start(removeSpaceHBox, True, True, 0)
        self.removeSpaceDialog.action_area.pack_start(cancel, True, True, 0)
        self.removeSpaceDialog.action_area.pack_end(button, True, True, 5)
        self.removeSpaceDialog.show()

    def rpc_removeSpace(self, widget=None, data=None):
        try:
            self.server.confluence1.removeSpace(self.token, self.removeSpaceEntry.get_text())
            self.removeSpaceDialog.hide()
        except xmlrpclib.Fault:
            self.errDialog("\t\tSpace Removal Failed\t\t\nPage either doesn't exist, or you lack permission")

    def callback(self, widget, data=None):
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])

    def removeDialog(self, widget, data=None):
        data.hide()
        
    def errDialog(self, data="None"):
        errorDialog = gtk.Dialog("Error Occurred")
        button = gtk.Button("Ok", gtk.STOCK_OK)
        if data:
            label = gtk.Label(data)
        else:
            label = gtk.labe("Error Occurred")
            
        button.connect("clicked", lambda x: errorDialog.hide())
            
        errorDialog.vbox.pack_start(label, True, True, 0)
        errorDialog.action_area.pack_start(button, True, True, 0)
        
        label.show()
        button.show()
        errorDialog.show()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    ConfluenceGTK()
    main()
