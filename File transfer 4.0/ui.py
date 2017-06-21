from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime,time,timedelta
import shutil
import os
import sqlite3

root = Tk()
t = datetime.now()

def make_table():
    con = sqlite3.connect('filetransfer.db')
    with con:
            c = con.cursor()
            c.executescript("CREATE TABLE if not exists file_info(FileName TEXT,LastCheck TEXT);")
            c.execute("INSERT INTO file_info (FileName,LastCheck) VALUES (?,?)",(doc_nameA,mod_time))
            con.commit()
        

def pick_fileA():
    global doc_nameA
    global fileA
    fileA = filedialog.askdirectory()
    doc_nameA = os.listdir(fileA)
    fileA_list.delete(0, END)# Just in case there is an other file being shown
    print(fileA)
    show_nameA()


def pick_fileB():
    global doc_nameB
    global fileB
    fileB = filedialog.askdirectory()
    doc_nameB = os.listdir(fileB)
    fileB_list.delete(0, END)# Just in case there is an other file being shown
    print(fileB)
    check_updates()
    show_nameB()

def show_nameA():
    for x in doc_nameA:
        fileA_list.insert(END, str(x))

def show_nameB():
    for x in doc_nameB:
        fileB_list.insert(END, str(x))

def show_mod_time():
    global mod_time
    for m in doc_nameA:
        if m.endswith('.txt'):
            files = (fileA+'\\'+m)
            mod_time = datetime.fromtimestamp(os.stat(files).st_mtime)
            print(mod_time)
            last_check_listbox.insert(END,m,mod_time)

def check_updates():
    for m in doc_nameA:
        if m.endswith('.txt'): #Checks if the file is a .txt document
            files = (fileA+'\\'+m) #Stores the address of the text documents to use later
            mod_time = datetime.fromtimestamp(os.stat(files).st_mtime) #converts this unix timestamp to a datetime object
            time_since_mod = (t - mod_time) # Gets the time diffrence between the current time and the time it was modified
            if time_since_mod > timedelta(days=1): # If time_since_mod is less than 1 day (meaning it was modified that day) -->
                shutil.copy(files,fileB) # It copies the file to dst
                print(m, "has been backed up to: ", fileB)
                show_nameB()
                fileB_list.delete(0, END)
                show_mod_time()
                make_table()
            else:
                print("This file hasnt been changed: ", m)

def manual_updates():
    for m in doc_nameA:
        if m.endswith('.txt'): #Checks if the file is a .txt document
            files = (fileA+'\\'+m) #Stores the address of the text documents to use later
            mod_time = datetime.fromtimestamp(os.stat(files).st_mtime) #converts this unix timestamp to a datetime object
            time_since_mod = (t - mod_time) # Gets the time diffrence between the current time and the time it was modified
            if time_since_mod != timedelta(seconds = 0): # If time_since_mod is less than 1 day (meaning it was modified that day) -->
                shutil.copy(files,fileB) # It copies the file to dst
                print(m, "has been backed up to: ", fileB)
                fileB_list.delete(0, END)
                show_nameB()
                show_mod_time()
    

label = Label(root, text = "File updates")
label.grid(row = 0, column = 0) 

work_file = Button(root, text = "Work file", command = pick_fileA)
work_file.grid(row = 1, column = 0)


backup_file = Button(root, text = "Back up file", command = pick_fileB)
backup_file.grid(row = 2, column = 0)


check = Button(root, text = "Save", command = manual_updates)
check.grid(row = 3, column = 0)

##scroll_barA = Scrollbar(root)
##scroll_barA.grid(row = 6, column = 3, columnspan = 2 )
##
##scroll_barB = Scrollbar(root)
##scroll_barB.grid(row = 6, column = 7, columnspan = 2)

fileA_label = Label(root, text = 'File A (Work Files)')
fileA_label.grid(row = 1, column = 1)
fileA_list = Listbox(root)
fileA_list.grid(row = 2, column = 1)

    

fileB_label = Label(root, text = 'File B (Backup files)')
fileB_label.grid(row = 1, column = 2)
fileB_list = Listbox(root)
fileB_list.grid(row = 2, column = 2)



last_check_label = Label(root, text = "Last check time")
last_check_label.grid(row = 4, column = 1)
last_check_listbox = Listbox(root, height = 4, width = 40)
last_check_listbox.grid(row = 5, column = 1, columnspan = 3)



'''yscrollcommand = scroll_barA.set'''
##scroll_barA.config(command = fileA_list.yview)
##scroll_barB.config(command = fileB_list.yview)

mainloop()

