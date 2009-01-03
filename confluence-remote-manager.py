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
import csv
from random import choice
import string
import xmlrpclib
from xmlrpclib import Server
from confluence_classes import *

#server = Server("http://localhost:8080/rpc/xmlrpc")

class ConfluenceGTK:

    def quit(self, widget=None, data=None):
        if self.loginObj.token != "":
            self.loginObj.server.confluence1.logout(self.loginObj.token)
                        
        gtk.main_quit()

    def __init__(self):
        self.mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.mainWindow.set_size_request(600,500)
        self.mainWindow.set_title("Confluence Remote Updater")
        self.mainWindow.connect("delete_event", lambda w,e: self.quit())
        self.mainWindow.set_border_width(20)
        self.loginObj = confluence_login.ConfluenceLogin(self)
        self.searchObj = confluence_search.ConfluenceSearch(self)
        self.userObj = confluence_users.UserManageMent(self)
        self.contentObj = confluence_content.ContentManageMent(self)
        self.mainWindow.show()

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
        
    def successDialog(self, data="None"):
        successDia = gtk.Dialog("Success")
        button = gtk.Button("Ok", gtk.STOCK_OK)
        if data:
            label = gtk.Label(data)
        else:
            label = gtk.labe("Error Occurred")
            
        button.connect("clicked", lambda x: successDia.hide())
        
        successDia.vbox.pack_start(label, True, True, 0)
        successDia.action_area.pack_start(button, True, True, 0)
        
        label.show()
        button.show()
        successDia.show()
        
    def transToMain(self, widget=None, data=None):
        self.mainWindow.remove(data)
        self.loginObj.launchPad()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    ConfluenceGTK()
    main()
