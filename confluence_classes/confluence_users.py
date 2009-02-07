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

class UserManageMent:
    
    def __init__(self, master=None):
        self.master = master
        
    def randomPassword(self, length=8, chars=string.letters + string.digits):
        return ''.join([choice(chars) for i in range(length)])

    def userManagement(self, widget):
        #Remove the current VBox
        self.master.mainWindow.remove(self.master.loginObj.menuVBox)

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
        self.bulkAddUsersRadio = gtk.Button("Add Bulk Users Via CSV")
        self.listAllUsersRadio = gtk.Button("List All Users")

        #Connect the Buttons to Funcs
        self.addUserRadio.connect("clicked", self.addUser)
        self.rmUserRadio.connect("clicked", self.removeUser)
        self.addGroupRadio.connect("clicked", self.addGroup)
        self.rmGroupRadio.connect("clicked", self.removeGroup)
        self.addToGroupRadio.connect("clicked", self.addToGroup)
        self.rmFromGroupRadio.connect("clicked", self.removeFromGroup)
        self.bulkAddUsersRadio.connect("clicked", self.bulkAddUsers)
        self.listAllUsersRadio.connect("clicked", self.listAllUsers)

        #Pack All the Radio Buttons
        self.updatePostRadioVBox.pack_start(self.addUserRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.rmUserRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.addGroupRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.rmGroupRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.addToGroupRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.rmFromGroupRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.bulkAddUsersRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.listAllUsersRadio, False, False, 5)

        #Pack the VBox into the HBox so we can pack it into the greater VBox shortly.
        self.userManageHBoxTop.pack_start(self.updatePostRadioVBox, False, False, 200)
        
        #Now the buttons to direct us from here
        self.returnMainMenuButton = gtk.Button(" Main Menu ")
        self.returnMainMenuButton.connect("clicked", self.master.transToMain, self.userManagementVBox)
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
        self.bulkAddUsersRadio.show()
        self.returnMainMenuButton.show()
        self.userManageHBoxBottom.show()
        self.updatePostRadioVBox.show()
        self.listAllUsersRadio.show()
        self.userManageHBoxTop.show()
        self.userManagementVBox.show()
    
        #Add to Window
        self.master.mainWindow.add(self.userManagementVBox)
        
    def addUser(self, widget=None, data=None):
        self.addUserDia = gtk.Dialog("Add User", self.master.mainWindow)
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
        cancel.connect("clicked", self.master.removeDialog, self.addUserDia)
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
            result = self.master.loginObj.server.confluence1.addUser(self.master.loginObj.token, userDict, self.passEntry.get_text())
            userDialog = gtk.Dialog("Success", self.master.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.master.removeDialog, userDialog)
            label = gtk.Label("User '%s' Added Successfully" % self.userEntry.get_text())
            userDialog.vbox.pack_start(label, True, True, 0)
            userDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            userDialog.show()
        except xmlrpclib.Fault:
            self.master.errDialog("           User Add Failed \n User Likely Exists Already              ")
    
    def removeUser(self, widget=None, data=None):
        self.rmUserDia = gtk.Dialog("Remove User", self.master.mainWindow)
        okButton = gtk.Button("Submit", gtk.STOCK_OK)
        cancel = gtk.Button("Cancel", gtk.STOCK_CANCEL)
        userLabel = gtk.Label("Username: ")
        self.userEntry = gtk.Entry()
        
        #Buttons
        okButton.connect("clicked", self.rpc_removeUser)
        cancel.connect("clicked", self.master.removeDialog, self.rmUserDia)
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
            result = self.master.loginObj.server.confluence1.removeUser(self.master.loginObj.token, self.userEntry.get_text())
            userDialog = gtk.Dialog("Success", self.master.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.master.removeDialog, userDialog)
            label = gtk.Label("User '%s' Removed Successfully" % self.userEntry.get_text())
            userDialog.vbox.pack_start(label, True, True, 0)
            userDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            userDialog.show()
        except xmlrpclib.Fault:
            self.master.errDialog("           User removal failed.\n User likely doesn't exist              ")
    
    def addGroup(self, widget=None, data=None):
        self.addGroupDia = gtk.Dialog("Add Group", self.master.mainWindow)
        okButton = gtk.Button("Submit", gtk.STOCK_OK)
        cancel = gtk.Button("Cancel", gtk.STOCK_CANCEL)
        groupLabel = gtk.Label("Group Name: ")
        self.groupEntry = gtk.Entry()
        
        #Buttons
        okButton.connect("clicked", self.rpc_addGroup)
        cancel.connect("clicked", self.master.removeDialog, self.addGroupDia)
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
            result = self.master.loginObj.server.confluence1.addGroup(self.master.loginObj.token, self.groupEntry.get_text())
            userDialog = gtk.Dialog("Success", self.master.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.master.removeDialog, userDialog)
            label = gtk.Label("Group '%s' Added Successfully" % self.groupEntry.get_text())
            userDialog.vbox.pack_start(label, True, True, 0)
            userDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            userDialog.show()
        except xmlrpclib.Fault:
            self.master.errDialog("           Group Addition Failed. \n You either lack the proper permissions, or the group exists.              ")
    
    def removeGroup(self, widget=None, data=None):
        self.rmGroupDia = gtk.Dialog("Remove Group", self.master.mainWindow)
        okButton = gtk.Button("Submit", gtk.STOCK_OK)
        cancel = gtk.Button("Cancel", gtk.STOCK_CANCEL)
        groupLabel = gtk.Label("Group Name: ")
        self.groupEntry = gtk.Entry()
        
        #Buttons
        okButton.connect("clicked", self.rpc_removeGroup)
        cancel.connect("clicked", self.master.removeDialog, self.rmGroupDia)
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
            result = self.master.loginObj.server.confluence1.removeGroup(self.master.loginObj.token, self.groupEntry.get_text(), "")
            userDialog = gtk.Dialog("Success", self.master.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.master.removeDialog, userDialog)
            label = gtk.Label("Group '%s' Removed Successfully" % self.groupEntry.get_text())
            userDialog.vbox.pack_start(label, True, True, 0)
            userDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            userDialog.show()
        except xmlrpclib.Fault:
            self.master.errDialog("           \tGroup Removal Failed. \n You either lack the proper permissions, or the group doesn't exist.              ")
    
    def addToGroup(self, widget=None, data=None):
        self.addUserDia = gtk.Dialog("Add User to Group", self.master.mainWindow)
        okButton = gtk.Button("Submit", gtk.STOCK_OK)
        cancel = gtk.Button("Cancel", gtk.STOCK_CANCEL)
        userLabel = gtk.Label("Username: ")
        self.userEntry = gtk.Entry()
        groupLabel = gtk.Label("Group: ")
        self.groupEntry = gtk.Entry()
        
        #Buttons
        okButton.connect("clicked", self.rpc_addToGroup)
        cancel.connect("clicked", self.master.removeDialog, self.addUserDia)
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
            result = self.master.loginObj.server.confluence1.addUserToGroup(self.master.loginObj.token, self.userEntry.get_text(), self.groupEntry.get_text())
            userDialog = gtk.Dialog("Success", self.master.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.master.removeDialog, userDialog)
            label = gtk.Label("User Added to '%s' Successfully" % self.groupEntry.get_text())
            userDialog.vbox.pack_start(label, True, True, 0)
            userDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            userDialog.show()
        except xmlrpclib.Fault:
            self.master.errDialog("\t\tFailed to add user to Group.\n\t\tPlease check your permission level")
    
    def removeFromGroup(self, widget=None, data=None):
        self.addUserDia = gtk.Dialog("Add User to Group", self.master.mainWindow)
        okButton = gtk.Button("Submit", gtk.STOCK_OK)
        cancel = gtk.Button("Cancel", gtk.STOCK_CANCEL)
        userLabel = gtk.Label("Username: ")
        self.userEntry = gtk.Entry()
        groupLabel = gtk.Label("Group: ")
        self.groupEntry = gtk.Entry()
        
        #Buttons
        okButton.connect("clicked", self.rpc_removeFromGroup)
        cancel.connect("clicked", self.master.removeDialog, self.addUserDia)
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
            result = self.master.loginObj.server.confluence1.removeUserFromGroup(self.master.loginObj.token, self.userEntry.get_text(), self.groupEntry.get_text())
            userDialog = gtk.Dialog("Success", self.master.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.master.removeDialog, userDialog)
            label = gtk.Label("User Removed From '%s' Successfully" % self.groupEntry.get_text())
            userDialog.vbox.pack_start(label, True, True, 0)
            userDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            userDialog.show()
        except xmlrpclib.Fault:
            self.master.errDialog("\t\tFailed to add user to Group.\n\t\tPlease check your permission level")
            
    def bulkAddUsers(self, widget=None, data=None):     
        self.csvSelector = gtk.FileChooserDialog("Select comma-delimited CSV file",
                                                None,
                                                gtk.FILE_CHOOSER_ACTION_OPEN,
                                                (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                                 gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        
        csvFiles = gtk.FileFilter()
        csvFiles.set_name("CSVs")
        csvFiles.add_pattern("*.csv")
        self.csvSelector.add_filter(csvFiles)
        
        allFiles = gtk.FileFilter()
        allFiles.set_name("All Files")
        allFiles.add_pattern("*")
        self.csvSelector.add_filter(allFiles)
        
        response = self.csvSelector.run()
        if response == gtk.RESPONSE_OK:
            self.rpc_bulkAddUsers()
            self.csvSelector.destroy()
        else:
            self.csvSelector.destroy()
        
    def rpc_bulkAddUsers(self, widget=None, data=None):
        try:
            csvFile = csv.reader(open(self.csvSelector.get_filename()))
            for row in csvFile:
                userName = row[0]
                fullName = row[1]
                email = row[2]
                password = self.randomPassword()
                user = {"name":userName,"fullname":fullName,"email":email}
                self.master.loginObj.server.confluence1.addUser(self.master.loginObj.token, user, password)
                for x in row[3:]:
                    self.master.loginObj.server.confluence1.addUserToGroup(self.master.loginObj.token, userName, x)
            self.master.successDialog("\t\tUsers added successfully!\t\t")
        except xmlrpclib.Fault:
                self.master.errDialog("\t\tFailed to add '%s'\t\t\n Please ensure user doesn't already exist" % userName)
        
    def listAllUsers(self, widget=None, data=None):
        self.listUsersDia = gtk.Dialog("Users", self.master.mainWindow)
        self.listUsersDia.set_size_request(300,200)
        okButton = gtk.Button("Close", gtk.STOCK_OK)
        #cancel = gtk.Button("Cancel", gtk.STOCK_CANCEL)
        #usersLabel = gtk.Label("Group Name: ")
        #self.groupEntry = gtk.Entry()
        self.userListScroll = gtk.ScrolledWindow()
        self.userListScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.userView = gtk.TextView()
        self.userView.set_editable(False)
        self.userBuffer = self.userView.get_buffer()
        self.userListScroll.add(self.userView)
        
        #Populate the text box
        users = self.master.loginObj.server.confluence1.getActiveUsers(self.master.loginObj.token, True)
        userString = ""
        for x in users:
            userString += x + "\n"
            
        self.userBuffer.set_text(userString)
        
        #Buttons
        okButton.connect("clicked", self.master.removeDialog, self.listUsersDia)
        self.listUsersDia.action_area.pack_end(okButton, True, True, 5)
        
        #Entries/Labels
        #addGroupHBox = gtk.HBox(False, 0)
        #addGroupHBox.pack_start(groupLabel, True, True, 0)
        #addGroupHBox.pack_end(self.groupEntry, True, True, 0)
        
        #Pack it Up
        self.listUsersDia.vbox.pack_start(self.userListScroll, True, True, 0)
        
        #Show it all off
        okButton.show()
        self.userListScroll.show()
        self.userView.show()
        self.listUsersDia.vbox.show()
        self.listUsersDia.show()
