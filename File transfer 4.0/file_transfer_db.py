import os
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import sqlite3

con = sqlite3.connect('filetransfer.db')
c = con.cursor()
