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

class ContentManageMent:
    
    def __init__(self, master=None):
        self.master = master
    
    def contentManagement(self, widget):
        #Remove the current VBox
        self.master.mainWindow.remove(self.master.loginObj.menuVBox)

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
        self.importSpaceRadio = gtk.Button("Import Space")

        #Connect the Buttons to Funcs
        self.updatePageRadio.connect("clicked", self.updatePage)
#        self.updatePostRadio.connect("clicked", self.updatePost)
        self.pageRadio.connect("clicked", self.newPage)
        self.blogRadio.connect("clicked", self.newBlogPost)
        self.addSpaceRadio.connect("clicked", self.newSpace)
        self.removePageRadio.connect("clicked", self.removePage)
#        self.removePostRadio.connect("clicked", self.removeBlogPost)
        self.removeSpaceRadio.connect("clicked", self.removeSpace)
        self.importSpaceRadio.connect("clicked", self.importSpace)

        #Pack All the Radio Buttons
        self.updatePostRadioVBox.pack_start(self.updatePageRadio, False, False, 5)
#        self.updatePostRadioVBox.pack_start(self.updatePostRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.pageRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.blogRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.addSpaceRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.removePageRadio, False, False, 5)
#        self.updatePostRadioVBox.pack_start(self.removePostRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.removeSpaceRadio, False, False, 5)
        self.updatePostRadioVBox.pack_start(self.importSpaceRadio, False, False, 5)

        #Pack the VBox into the HBox so we can pack it into the greater VBox shortly.
        self.contentManageHBoxTop.pack_start(self.updatePostRadioVBox, False, False, 200)
        
        #Now the buttons to direct us from here
        self.returnMainMenuButton = gtk.Button(" Main Menu ")
        self.returnMainMenuButton.connect("clicked", self.master.transToMain, self.contentManagementVBox)
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
        self.importSpaceRadio.show()
        self.returnMainMenuButton.show()
        self.contentManageHBoxBottom.show()
        self.updatePostRadioVBox.show()
        self.contentManageHBoxTop.show()
        self.contentManagementVBox.show()
    
        #Add to Window
        self.master.mainWindow.add(self.contentManagementVBox)        

    def updatePost(self, widget=None):
        print "updatePost"
        pass
    
    def updatePage(self, widget=None):
        self.master.mainWindow.remove(self.contentManagementVBox)
        
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
        self.returnMainMenuButton.connect("clicked", self.master.transToMain, self.updatePageVBox)
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
        self.master.mainWindow.add(self.updatePageVBox)

    def grabContent(self, widget=None):
        try:
            self.pageText = self.master.loginObj.server.confluence1.getPage(self.master.loginObj.token, self.updatePageKey.get_text(), self.updatePagePostTitle.get_text())
            self.updatePageTextBuffer.set_text(self.pageText["content"])
            self.updatePageTextView.set_buffer(self.updatePageTextBuffer)
        except xmlrpclib.Fault:
            self.master.errDialog("\t\tPage Updating Failed\t\t\nPage either doesn't exist, or you lack permission")

    def rpc_updatePage(self, widget=None):
        try:
            startiter, enditer = self.updatePageTextBuffer.get_bounds()
            self.pageText["content"] = self.updatePageTextBuffer.get_text(startiter,enditer)
            result = self.master.loginObj.server.confluence1.storePage(self.master.loginObj.token, self.pageText)
            updatePageDialog = gtk.Dialog("Success", self.master.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.master.removeDialog, updatePageDialog)
            label = gtk.Label("Page updated Successfully")
            updatePageDialog.vbox.pack_start(label, True, True, 0)
            updatePageDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            updatePageDialog.show()
        except xmlrpclib.Fault:
            self.master.errDialog("\t\tPage Updating Failed\t\t\nPage either doesn't exist, or you lack permission")


    def newPage(self, widget=None):
        self.master.mainWindow.remove(self.contentManagementVBox)
        
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
        self.newPageHBox3 = gtk.HBox(False, 0)
        self.newPageKeyLabel = gtk.Label("Space: ")
        self.newPageKey = gtk.Entry()
        self.newPageKey.set_text("Key")
        self.newPageParentLabel = gtk.Label("Parent: ")
        self.newPageParentEntry = gtk.Entry()
        self.newPageParentEntry.set_text("Title of Page")
        self.newPageLabel = gtk.Label("Title: ")
        self.newPagePostTitle = gtk.Entry()
        self.newPageHBox1.pack_start(self.newPageKeyLabel, False, False, 0)
        self.newPageHBox1.pack_start(self.newPageKey, False, False, 0)
        self.newPageHBox1.pack_end(self.newPagePostTitle, False, False, 0)
        self.newPageHBox1.pack_end(self.newPageLabel, False, False, 0)
        self.newPageHBox3.pack_start(self.newPageParentLabel, False, False, 0)
        self.newPageHBox3.pack_start(self.newPageParentEntry, False, False, 0)

        #Submit that shit
        self.returnMainMenuButton = gtk.Button(" Main Menu ")
        self.returnMainMenuButton.connect("clicked", self.master.transToMain, self.newPageVBox)
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
        self.newPageVBox.pack_start(self.newPageHBox3, False, False, 10)
        self.newPageVBox.pack_start(self.newPageScroll, True, True, 0)
        self.newPageVBox.pack_end(self.newPageHBox2, False, False, 10)
        
        #Show it all off
        self.newPageScroll.show()
        self.newPageTextView.show()
        self.newPageVBox.show()
        self.newPageKeyLabel.show()
        self.newPageKey.show()
        self.newPageParentLabel.show()
        self.newPageParentEntry.show()
        self.newPageTitle.show()
        self.newPageLabel.show()
        self.newPagePostTitle.show()
        self.newPageButton.show()
        self.returnMainMenuButton.show()
        self.newPageHBox1.show()
        self.newPageHBox2.show()
        self.newPageHBox3.show()
        self.master.mainWindow.add(self.newPageVBox)

    def rpc_newPage(self, widget=None):
        try:
            startiter, enditer = self.newPageTextBuffer.get_bounds()
            if self.newPageParentEntry.get_text() != "Title of Page":
                tempPage = self.master.loginObj.server.confluence1.getPage(self.master.loginObj.token, self.newPageKey.get_text(), self.newPageParentEntry.get_text())
                newPost = {"title":self.newPagePostTitle.get_text(), "space":self.newPageKey.get_text(), "content":self.newPageTextBuffer.get_text(startiter, enditer), "parentId":tempPage["id"]}
            else:
                newPost = {"title":self.newPagePostTitle.get_text(), "space":self.newPageKey.get_text(), "content":self.newPageTextBuffer.get_text(startiter, enditer)}
            result = self.master.loginObj.server.confluence1.storePage(self.master.loginObj.token, newPost)
            newPageDialog = gtk.Dialog("Success", self.master.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.master.removeDialog, newPageDialog)
            label = gtk.Label("Page created Successfully")
            newPageDialog.vbox.pack_start(label, True, True, 0)
            newPageDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            newPageDialog.show()
        except xmlrpclib.Fault:
            self.master.errDialog("\t\tPage Creation Failed\t\t\nPage either exists, or you lack permission")
    
    def newBlogPost(self, widget=None):
        self.master.mainWindow.remove(self.contentManagementVBox)
        
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
        self.returnMainMenuButton.connect("clicked", self.master.transToMain, self.newPostVBox)
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
        self.master.mainWindow.add(self.newPostVBox)

    def rpc_newPost(self, widget=None, data=None):
        try:
            startiter, enditer = self.newPostTextBuffer.get_bounds()
            newPost = {"title":self.newPostPostTitle.get_text(), "space":self.newPostKey.get_text(), "content":self.newPostTextBuffer.get_text(startiter, enditer)}
            result = self.master.loginObj.server.confluence1.storeBlogEntry(self.master.loginObj.token, newPost)
            newPostDialog = gtk.Dialog("Success", self.master.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.master.removeDialog, newPostDialog)
            label = gtk.Label("Post created Successfully")
            newPostDialog.vbox.pack_start(label, True, True, 0)
            newPostDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            newPostDialog.show()
        except xmlrpclib.Fault:
            self.master.errDialog("\t\tBlog Post Creation Failed\t\t\nTitle either exists, Space doesn't, or you lack permission")


    def newSpace(self, widget=None):
        self.master.mainWindow.remove(self.contentManagementVBox)

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
        self.returnMainMenuButton.connect("clicked", self.master.transToMain, self.newSpaceVBox)

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
        self.master.mainWindow.add(self.newSpaceVBox)

    def rpc_addSpace(self, widget=None, data=None):
        try:
            space = {"key":self.newSpaceKeyEntry.get_text(),"name":self.newSpaceTitleEntry.get_text(),"description":self.newSpaceDescEntry.get_text()}
            result = self.master.loginObj.server.confluence1.addSpace(self.master.loginObj.token, space)
            newPageDialog = gtk.Dialog("Success", self.master.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.master.removeDialog, newPageDialog)
            label = gtk.Label("Space Added Successfully")
            newPageDialog.vbox.pack_start(label, True, True, 0)
            newPageDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            newPageDialog.show()
        except xmlrpclib.Fault:
            self.master.errDialog("\t\tSpace Creation Failed\t\t\nSpace either exists or you lack permission")

    def removePage(self, widget=None):
        self.master.mainWindow.remove(self.contentManagementVBox)

        #Setup our VBox
        self.removePageMainVBox = gtk.VBox(False, 0)
        self.removePageTitle = gtk.Label("Removing Page From Confluence")

        #Return to Main Menu
        self.returnMainMenuButton = ""
        self.returnMainMenuButton = gtk.Button(" Main Menu ")
        self.returnMainMenuButton.connect("clicked", self.master.transToMain, self.removePageMainVBox)

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
        self.master.mainWindow.add(self.removePageMainVBox)

    def rpc_removePage(self, widget=None):
        try:
            page = self.master.loginObj.server.confluence1.getPage(self.master.loginObj.token, self.removePageKeyEntry.get_text(), self.removePageTitleEntry.get_text())
            result = self.master.loginObj.server.confluence1.removePage(self.master.loginObj.token, page["id"])
            newPageDialog = gtk.Dialog("Success", self.master.mainWindow)
            button = gtk.Button("Okay", gtk.STOCK_OK)
            button.connect("clicked", self.master.removeDialog, newPageDialog)
            label = gtk.Label("Page Removed Successfully")
            newPageDialog.vbox.pack_start(label, True, True, 0)
            newPageDialog.action_area.pack_start(button, True, True, 0)
            label.show()
            button.show()
            newPageDialog.show()
        except xmlrpclib.Fault:
            self.master.errDialog("\t\tPage Removal Failed\t\t\nPage either doesn't exist, or you lack permission")

    def removeSpace(self, widget=None):
        self.removeSpaceDialog = gtk.Dialog("Remove Space", self.master.mainWindow)
        button = gtk.Button("Okay", gtk.STOCK_OK)
        cancel = gtk.Button("Cancel", gtk.STOCK_CANCEL)
        self.removeSpaceEntry = gtk.Entry()
        cancel.connect("clicked", self.master.removeDialog, self.removeSpaceDialog)
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
            self.master.loginObj.server.confluence1.removeSpace(self.master.loginObj.token, self.removeSpaceEntry.get_text())
            self.removeSpaceDialog.hide()
        except xmlrpclib.Fault:
            self.master.errDialog("\t\tSpace Removal Failed\t\t\nPage either doesn't exist, or you lack permission")

    def importSpace(self, widget=None):
        self.backupSelector = gtk.FileChooserDialog("Select Zipped XML Backup:",
                                                None,
                                                gtk.FILE_CHOOSER_ACTION_OPEN,
                                                (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                                 gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        
        backupFiles = gtk.FileFilter()
        backupFiles.set_name("zip")
        backupFiles.add_pattern("*.zip")
        self.backupSelector.add_filter(backupFiles)
        
        allFiles = gtk.FileFilter()
        allFiles.set_name("All Files")
        allFiles.add_pattern("*")
        self.backupSelector.add_filter(allFiles)
        
        response = self.backupSelector.run()
        if response == gtk.RESPONSE_OK:
            self.rpc_importSpace()
            self.backupSelector.destroy()
        else:
            self.backupSelector.destroy()
        
    def rpc_importSpace(self, widget=None, data=None):
        try:
            backupFile = open(self.backupSelector.get_filename())
            backup_raw = backupFile.read()
            backup_binary = xmlrpclib.Binary(backup_raw)
            result = self.master.loginObj.server.confluence1.importSpace(self.master.loginObj.token, backup_binary)
            if result:
                self.master.successDialog("Space imported successfully")
            else:
                self.master.errDialog("Failed to import space. Does it exist already?")
        except IOError:
            self.master.errDialog("Failed to open file. Please check Permissions")
        except xmlrpclib.Fault:
            self.master.errDialog("Failed to import space. Please check your permissions")