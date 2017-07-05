'''
	This is an explorer for the forge file format used in Assassin's Creed
	The format varies slightly between games and the current implementation will only work
	with Assassin's Creed Unity.
	The forge file format is similar to a zip file in concept however each individual containing
	file can be decompressed individually.
	The 'folders' in the top level of the forge file will from this point on be referred to as datafiles.
	Contained within the datafiles are a variety of files related to that datafile.
'''

# should perhaps work out a way to allow multiple games to be supported
game = 'ACU'
if game == 'ACU':
	from ACUnity.readForge import *
	from ACUnity.decompressDatafile import *
	from ACUnity.readFile import *

from misc import tempFiles
import random
# this should probably be rewritten to not import all
from Tkinter import *
import ttk
import os

# a dictionary containing file ids
# location in the file, size and file name
# this is rebuilt each time the program opens
# fileList = {}

#set up config values
import json
config = json.load(open('AC_Explorer.config'))


top = Tk()

searchLabel = Label(top, text="Find ID:")
searchLabel.grid(row=0, column=0)

fileTree = ttk.Treeview(top)
fileTree.grid(row=1, column=1, columnspan=6, ipadx=150, ipady=300)
fileTree.insert('', 'end', 'ACU', text='ACU')
fileTreeScroll = ttk.Scrollbar(top, orient="vertical", command=fileTree.yview)
fileTreeScroll.grid(row=1, column=0, ipady=300)
fileTree.configure(yscrollcommand=fileTreeScroll.set)

def onClick(event):
	fileID = fileTree.selection()[0]
	if len(fileID.split('|')) == 3 and len(fileTree.get_children(fileID)) == 0:
		decompressDatafile(fileTree, fileList, config, fileID.split('|')[2], fileID.split('|')[1])

fileTree.bind("<<TreeviewSelect>>", onClick)

def onDoubleClick(event):
	fileID = fileTree.selection()[0]
	if len(fileID.split('|')) == 4:
		readFile(fileTree, fileList, config, fileID.split('|')[3])

fileTree.bind("<Double-1>", onDoubleClick)

# fileList is a dictionary of each forge file on the first level and
# each datafile on the second level under each forge file. This is used
# as a cheap way to find the location a file is stored under.
# this function also loads all the forge files and datafiles onto the TK Tree
fileList = readForge(fileTree, config["ACUnityFolder"])

# load all the decompressed files onto the TK Tree
tempFiles.populateTree(fileTree, config)

print 'Done'

def searchFor():
	if search.get() != '':
		fileID = search.get().replace(' ', '').upper()
		readFile(fileTree, fileList, config, fileID)

search = Entry(top)
search.grid(row=0, column=1)
find = Button(top, text = 'Find', command=searchFor)
find.grid(row=0, column=2)

def clearSearch():
	search.delete(0, END)
	
clear = Button(top, text = 'Clear Search', command=clearSearch)
clear.grid(row=0, column=3)

def runcode():
	exec search.get()

runCode = Button(top, text = 'Run Code', command=runcode)
runCode.grid(row=0, column=6)

def info(input=None):
	if search.get() == '' and input == None:
		return
	if search.get() != '':
		fileID = search.get().replace(' ', '').upper()
	if input != None:
		fileID = input.replace(' ', '').upper()
	import tempFiles
	if not tempFiles.exists(config, fileID):
		decompressDatafile(fileTree, fileList, config, fileID)
	if not tempFiles.exists(config, fileID):
		raise Exception()
	print fileID
	print tempFiles.read(config, fileID)
		
infobutton = Button(top, text = 'Info', command=info)
infobutton.grid(row=0, column=8)

top.mainloop()