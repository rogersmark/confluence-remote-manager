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

class ConfluenceSearch:
    
    def __init__(self, master=None):
        self.master = master
        
        
    def searchConfluence(self, widget):
        self.master.mainWindow.remove(self.master.loginObj.menuVBox)

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
        self.returnMainMenuButton.connect("clicked", self.master.transToMain, self.searchVBox)
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
        self.master.mainWindow.add(self.searchVBox)

    def rpc_search(self, widget=None, data=None):
        self.searchBuffer.set_text("")
        try:
            results = self.master.loginObj.server.confluence1.search(self.master.loginObj.token, self.searchEntry.get_text(), 50)
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
            self.master.errDialog("Search failed, and can be finicky at times.\nPlease try different search terms")
            
        except:
            self.master.errDialog("\t\tConnection Failed\t\t")