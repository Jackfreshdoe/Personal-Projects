from tkinter import ttk
from tkinter import *
import csv
import sys
import random
import datetime
import tkinter.simpledialog
import time
from tkinter import messagebox
import sqlite3 as sql
import sqlite3
import webbrowser
import atexit
import time
import tkinter.messagebox as tkMessageBox
import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker
import numpy as np


levelofaccess = 0



#-----------------Functions--------------------
#This is deleting all the data from the cache so that we can display new data when we log in
con = sqlite3.connect("codfatherdata.db")
cur = con.cursor()
cur.execute("DELETE FROM cache")
con.commit()

#This is deleting all the data from the temporder table so we can create new temporary orders further on
con = sqlite3.connect("codfatherdata.db")
cur = con.cursor()
cur.execute("DELETE FROM temporder")
con.commit()

#A function used to raise a new frame when it is executed
def raise_frame(frame):
    frame.tkraise()

#A function used to login and display the current user logged into the system
def login():

    global access
    global usernamefromcache
    
    usernameentered = username.get()
    passwordentered = password.get()
    filled = False

    while(filled == False):
        if usernameentered == '' or passwordentered == '':
            messagebox.showinfo('', 'Please enter information into both boxes')
            break
        elif not usernameentered.isalpha():
            messagebox.showinfo('', 'The username must be a word')
            break
        else:
            filled = True
        
    found = 0

    if filled == True:
        #Creating a connection the the database to compare the entry box data to the database data
        con = sql.connect("codfatherdata.db")
        cur = con.cursor()
        statement = f"SELECT username from users WHERE username='{usernameentered}' AND password = '{passwordentered}';"
        cur.execute(f"SELECT access from users WHERE username='{usernameentered}' AND password = '{passwordentered}';")
        result = cur.fetchone();
        cur.execute(statement)
        #If they do not match the data in the database then it will display a messagebox
        if not cur.fetchone():  # An empty result evaluates to False.
            messagebox.showinfo('Login','The Login was a Failure')
            username.set('')
            password.set('')
        else:
            found = 1
            messagebox.showinfo('Login','The login was a success')
            for i in result:
                if i == 'owner':
                    #The data is then temporarely saved in the cache table to be displayed in each of the frames
                    con = sql.connect("codfatherdata.db")
                    cur = con.cursor()
                    cur.execute(f"INSERT INTO cache (username, access) VALUES (?, ?)",
                                (username.get(), i,))
                    con.commit()
                    con = sql.connect("codfatherdata.db")
                    cur = con.cursor()
                    cur.execute(f"SELECT * FROM cache")
                    detailsfound = cur.fetchone();
                    usernamefromcache, access = detailsfound
                    con.commit()

                    #------Labels to Display Username and Access Level-------
                
                
                    usernametodisplay1 = Label(ownerdashboardframe, text = str(usernamefromcache), fg = 'black',bg = 'white')
                    usernametodisplay1.grid(row = 0, column = 6)

                    tiertodisplay1 = Label(ownerdashboardframe, text = str(access), fg = 'black', bg = 'white')
                    tiertodisplay1.grid(row = 1, column = 6)

                    usernametodisplay2 = Label(ownerreviewframe, text = str(usernamefromcache), fg = 'black',bg = 'white')
                    usernametodisplay2.grid(row = 0, column = 6)

                    tiertodisplay2 = Label(ownerreviewframe, text = str(access), fg = 'black', bg = 'white')
                    tiertodisplay2.grid(row = 1, column = 6)

                    usernametodisplay3 = Label(ownerstaffframe, text = str(usernamefromcache), fg = 'black',bg = 'white')
                    usernametodisplay3.grid(row = 0, column = 6)

                    tiertodisplay3 = Label(ownerstaffframe, text = str(access), fg = 'black', bg = 'white')
                    tiertodisplay3.grid(row = 1, column = 6)

                    usernametodisplay4 = Label(ownermenuframe, text = str(usernamefromcache), fg = 'black',bg = 'white')
                    usernametodisplay4.grid(row = 0, column = 6)

                    tiertodisplay4 = Label(ownermenuframe, text = str(access), fg = 'black', bg = 'white')
                    tiertodisplay4.grid(row = 1, column = 6)

                    usernametodisplay5 = Label(ownerorderframe, text = str(usernamefromcache), fg = 'black',bg = 'white')
                    usernametodisplay5.grid(row = 0, column = 6)

                    tiertodisplay5 = Label(ownerorderframe, text = str(access), fg = 'black', bg = 'white')
                    tiertodisplay5.grid(row = 1, column = 6)
                
                    #------End of Labels----------------
                
                    openownerdashboard()
                    levelofaccess = 'owner'
                
                
                elif i == 'staff':
                    con = sql.connect("codfatherdata.db")
                    cur = con.cursor()
                    cur.execute(f"INSERT INTO cache (username, access) VALUES (?, ?)",
                                (username.get(), i,))
                    con.commit()
                    con = sql.connect("codfatherdata.db")
                    cur = con.cursor()
                    cur.execute(f"SELECT * FROM cache")
                    detailsfound = cur.fetchone();
                    usernamefromcache, access = detailsfound
                    con.commit()

                
                    #------Labels to Display Username and Access Level-------
                
                    usernametodisplay1 = Label(staffdashboardframe, text = str(usernamefromcache), fg = 'black',bg = 'white')
                    usernametodisplay1.grid(row = 0, column = 6)

                    tiertodisplay1 = Label(staffdashboardframe, text = str(access), fg = 'black', bg = 'white')
                    tiertodisplay1.grid(row = 1, column = 6)

                    usernametodisplay2 = Label(staffreviewframe, text = str(usernamefromcache), fg = 'black',bg = 'white')
                    usernametodisplay2.grid(row = 0, column = 6)

                    tiertodisplay2 = Label(staffreviewframe, text = str(access), fg = 'black', bg = 'white')
                    tiertodisplay2.grid(row = 1, column = 6)

                    usernametodisplay3 = Label(staffstaffframe, text = str(usernamefromcache), fg = 'black',bg = 'white')
                    usernametodisplay3.grid(row = 0, column = 6)

                    tiertodisplay3 = Label(staffstaffframe, text = str(access), fg = 'black', bg = 'white')
                    tiertodisplay3.grid(row = 1, column = 6)

                    usernametodisplay4 = Label(staffmenuframe, text = str(usernamefromcache), fg = 'black',bg = 'white')
                    usernametodisplay4.grid(row = 0, column = 6)

                    tiertodisplay4 = Label(staffmenuframe, text = str(access), fg = 'black', bg = 'white')
                    tiertodisplay4.grid(row = 1, column = 6)

                    usernametodisplay5 = Label(stafforderframe, text = str(usernamefromcache), fg = 'black',bg = 'white')
                    usernametodisplay5.grid(row = 0, column = 6)

                    tiertodisplay5 = Label(stafforderframe, text = str(access), fg = 'black', bg = 'white')
                    tiertodisplay5.grid(row = 1, column = 6)
                
                    #------End of Labels----------------
                
                    openstaffdashboard()
                    levelofaccess = 'staff'
                
                
                elif i == 'customer':
                    con = sql.connect("codfatherdata.db")
                    cur = con.cursor()
                    cur.execute(f"INSERT INTO cache (username, access) VALUES (?, ?)",
                                (username.get(), i,))
                    con.commit()
                    con = sql.connect("codfatherdata.db")
                    cur = con.cursor()
                    cur.execute(f"SELECT * FROM cache")
                    detailsfound = cur.fetchone();
                    usernamefromcache, access = detailsfound
                    con.commit()

                
                    #------Labels to Display Username and Access Level-------
                
                    usernametodisplay1 = Label(customerdashboardframe, text = str(usernamefromcache), fg = 'black',bg = 'white')
                    usernametodisplay1.grid(row = 0, column = 6)

                    tiertodisplay1 = Label(customerdashboardframe, text = str(access), fg = 'black', bg = 'white')
                    tiertodisplay1.grid(row = 1, column = 6)

                    usernametodisplay2 = Label(customerreviewframe, text = str(usernamefromcache), fg = 'black',bg = 'white')
                    usernametodisplay2.grid(row = 0, column = 6)

                    tiertodisplay2 = Label(customerreviewframe, text = str(access), fg = 'black', bg = 'white')
                    tiertodisplay2.grid(row = 1, column = 6)

                    usernametodisplay3 = Label(customerstaffframe, text = str(usernamefromcache), fg = 'black',bg = 'white')
                    usernametodisplay3.grid(row = 0, column = 6)

                    tiertodisplay3 = Label(customerstaffframe, text = str(access), fg = 'black', bg = 'white')
                    tiertodisplay3.grid(row = 1, column = 6)

                    usernametodisplay4 = Label(customermenuframe, text = str(usernamefromcache), fg = 'black',bg = 'white')
                    usernametodisplay4.grid(row = 0, column = 6)
    
                    tiertodisplay4 = Label(customermenuframe, text = str(access), fg = 'black', bg = 'white')
                    tiertodisplay4.grid(row = 1, column = 6)

                    usernametodisplay5 = Label(customerorderframe, text = str(usernamefromcache), fg = 'black',bg = 'white')
                    usernametodisplay5.grid(row = 0, column = 6)

                    tiertodisplay5 = Label(customerorderframe, text = str(access), fg = 'black', bg = 'white')
                    tiertodisplay5.grid(row = 1, column = 6)
                
                    #------End of Labels----------------
                
                    opencustomerdashboard()
                    levelofaccess = 'customer'
                
    

#This function is used to reload the order frame so when it is opended after adding a new order it will display it
def load_ordertreeview():

    #Reloading the Owner Order treeview
    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM orders')
    data = cursor.fetchall()

    for i in ownerordertreeview.get_children():
        ownerordertreeview.delete(i)

    for row in data:
        ownerordertreeview.insert("",END, values=row)

    for i in customerordertreeview.get_children():
        customerordertreeview.delete(i)

    for row in data:
        customerordertreeview.insert("",END, values=row)

    for i in staffordertreeview.get_children():
        staffordertreeview.delete(i)

    for row in data:
        staffordertreeview.insert("",END, values=row)

    conn.close()

#This functon is used to reload the menutreeviews in each frame
def load_menutreeview():

    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM menu')
    data = cursor.fetchall()

    for i in ownermenutreeview.get_children():
        ownermenutreeview.delete(i)

    for row in data:
        ownermenutreeview.insert("",END, values=row)

    for i in staffmenutreeview.get_children():
        staffmenutreeview.delete(i)

    for row in data:
        staffmenutreeview.insert("",END, values=row)

    for i in customermenutreeview.get_children():
        customermenutreeview.delete(i)

    for row in data:
        customermenutreeview.insert("",END, values=row)

    conn.close()
    
#This function will bring the user back to the loginfram as well as clear the cache frame
def backtologin():
    con = sqlite3.connect("codfatherdata.db")
    cur = con.cursor()
    #Clearing the caches
    cur.execute("DELETE FROM cache")
    cur.execute("DELETE FROM temporder")
    con.commit()
    raise_frame(loginframe)
    root.geometry('400x500')
    username.set('')
    password.set('')

#Command to raise the frame where a new customer can be added
def raise_newcustomerframe():
    raise_frame(newcustomerframe)
    root.geometry('500x500')

#Command used to add the new customer to the database with the according access level
def addnewcustomer():
    
    accesslevel = 'customer'
    #we mus first get the username and password to be entered into the database and then we must add them alongisde the level of access in the next blank
    passwordtoadd = passwordchange.get()
    usernametoadd = usernamechange.get()
    filled = False



        
    while(filled == False):
        if usernametoadd == '' or passwordtoadd == '':
            messagebox.showinfo('Empty Box','Please fill in information into every field')
            break
        elif not usernametoadd.isalpha():
            messagebox.showinfo('', 'The username must be a word')
            break
        elif passwordtoadd.isalpha():
            messagebox.showinfo('','The password must be a word')
            break
        else:
            filled = True

    if filled == True:
        con = sql.connect('codfatherdata.db')
        cur = con.cursor()

        cur.execute(f"SELECT * from Users WHERE Username='{usernametoadd}'")
        registeredusernames = cur.fetchone();
        if registeredusernames is not None:
            Username, password, access = registeredusernames
            messagebox.showinfo('Unable','There is already a user with the username ' + str(Username))

        else:
            con = sql.connect("codfatherdata.db")
            cur = con.cursor()
            cur.execute("INSERT INTO Users (Username, password, access) VALUES (?, ?, ?)",
                    (usernametoadd, passwordtoadd, accesslevel))
            messagebox.showinfo('User added','The User ' + usernametoadd + ' has been added to the database.')
            con.commit()
            
        
    

    


                      


#Functions used to open the Codfather facebook
def opencodfatherfacebook():
    url= 'https://en-gb.facebook.com/Codfatherlisburn/'
    webbrowser.open_new_tab(url)

#This command is used to raise the ownerdashboard frame
def openownerdashboard():
    raise_frame(ownerdashboardframe)
    root.geometry('1150x700')

    #The bar graph is being create here so everytime this frame is raised the table is updated
    con = sql.connect("codfatherdata.db")
    cur = con.cursor()

    # Get data from the 'Rating' column in the 'reviews' table
    ownerreviewsdata = "SELECT Rating FROM reviews"
    ownerdatable = pd.read_sql(ownerreviewsdata, con)

    # Count the number of occurrences of each rating value
    ratings_counts = np.zeros(6)
    for rating in ownerdatable['Rating']:
        index = int(rating)
        ratings_counts[index] += 1

    # Plot the bar chart
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    x = np.arange(6)
    y = ratings_counts
    ax.bar(x, y, width=0.4)
    ax.set_xlabel('Rating')
    ax.set_ylabel('Count')
    ax.set_title('Rating Distribution')
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xticks(x, [str(i) for i in x])
    plt.subplots_adjust(bottom=0.4)

    canvas = FigureCanvasTkAgg(fig, master=ownerdashboardframe)
    canvas.draw()
    canvas.get_tk_widget().grid(row=4, column=0, columnspan = 4)

#Command used to open the owner review frame      
def openownerreviews():
    raise_frame(ownerreviewframe)
    root.geometry('1150x700')

#Command used to open owner staff frame
def openownerStaff():
    raise_frame(ownerstaffframe)
    root.geometry('1150x700')

#Command used to open owner menu frame
def openownermenu():
    raise_frame(ownermenuframe)
    root.geometry('1150x700')

#Command used to open owner order frame
def openownerorder():
    raise_frame(ownerorderframe)
    root.geometry('1150x700')

    load_ordertreeview()
    


def openstaffdashboard():
    raise_frame(staffdashboardframe)
    root.geometry('1150x700')

    #The bar graph is being create here so everytime this frame is raised the table is updated
    con = sql.connect("codfatherdata.db")
    cur = con.cursor()

    # Get data from the 'Rating' column in the 'reviews' table
    staffreviewsdata = "SELECT Rating FROM reviews"
    staffdatable = pd.read_sql(staffreviewsdata, con)

    # Count the number of occurrences of each rating value
    ratings_counts = np.zeros(6)
    for rating in staffdatable['Rating']:
        index = int(rating)
        ratings_counts[index] += 1

    # Plot the bar chart
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    x = np.arange(6)
    y = ratings_counts
    ax.bar(x, y, width=0.4)
    ax.set_xlabel('Rating')
    ax.set_ylabel('Count')
    ax.set_title('Rating Distribution')
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xticks(x, [str(i) for i in x])
    plt.subplots_adjust(bottom=0.4)

    canvas = FigureCanvasTkAgg(fig, master=staffdashboardframe)
    canvas.draw()
    canvas.get_tk_widget().grid(row=4, column=0, columnspan = 4)

def openstaffreviews():
    raise_frame(staffreviewframe)
    root.geometry('1150x700')

def openstaffStaff():
    raise_frame(staffstaffframe)
    root.geometry('1150x700')

def openstaffmenu():
    raise_frame(staffmenuframe)
    root.geometry('1150x700')

def openstafforder():
    raise_frame(stafforderframe)
    root.geometry('1150x700')

    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM orders')
    data = cursor.fetchall()

    for i in staffordertreeview.get_children():
        staffordertreeview.delete(i)

    for row in data:
        staffordertreeview.insert("",END, values=row)

    conn.close()

def opencustomerdashboard():
    raise_frame(customerdashboardframe)
    root.geometry('1150x700')

    #The bar graph is being create here so everytime this frame is raised the table is updated
    con = sql.connect("codfatherdata.db")
    cur = con.cursor()

    # Get data from the 'Rating' column in the 'reviews' table
    customerreviewsdata = "SELECT Rating FROM reviews"
    customerdatable = pd.read_sql(customerreviewsdata, con)

    # Count the number of occurrences of each rating value
    ratings_counts = np.zeros(6)
    for rating in customerdatable['Rating']:
        index = int(rating)
        ratings_counts[index] += 1

    # Plot the bar chart
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    x = np.arange(6)
    y = ratings_counts
    ax.bar(x, y, width=0.4)
    ax.set_xlabel('Rating')
    ax.set_ylabel('Count')
    ax.set_title('Rating Distribution')
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    plt.xticks(x, [str(i) for i in x])
    plt.subplots_adjust(bottom=0.4)

    canvas = FigureCanvasTkAgg(fig, master=customerdashboardframe)
    canvas.draw()
    canvas.get_tk_widget().grid(row=4, column=0, columnspan = 4)

def opencustomerreviews():
    raise_frame(customerreviewframe)
    root.geometry('1150x700')

def opencustomerStaff():
    raise_frame(customerstaffframe)
    root.geometry('1150x700')

def opencustomermenu():
    raise_frame(customermenuframe)
    root.geometry('1150x700')

def opencustomerorder():
    raise_frame(customerorderframe)
    root.geometry('1150x700')

    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM orders')
    data = cursor.fetchall()

    for i in customerordertreeview.get_children():
        customerordertreeview.delete(i)

    for row in data:
        customerordertreeview.insert("",END, values=row)

    conn.close()


#Object Oriented Bubble Sort used to search through the prices in the menu table
class BubbleSort:
    def __init__(self, db_file):
        self.db_file = db_file

    def sort_prices(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT Price FROM menu')
            prices = [row[0] for row in cursor.fetchall()]

            n = len(prices)
            for i in range(n):
                for j in range(n-i-1):
                    if prices[j] > prices[j+1]:
                        prices[j], prices[j+1] = prices[j+1], prices[j]

            return prices
        
def edit_data():
    selected_item = ownerstafftreeview.selection()
    if not selected_item:
        messagebox.showinfo('','You must select a variable to edit before clicking this button')
        return
        
    item_data = ownerstafftreeview.item(selected_item)["values"]
    name, dob, starting_date, staffid = item_data

    newusername.set(name)
    newDOB.set(dob)
    newstartingdate.set(starting_date)

    raise_frame(editingstaffframe)
        
   
def savestaffedits():
    selected_item = ownerstafftreeview.selection()
    item_data = ownerstafftreeview.item(selected_item)["values"]
    name, dob, starting_date, staffid = item_data
    new_name = newusername.get()
    new_dob = newDOB.get()
    new_starting_date = newstartingdate.get()
    filled = False

    while(filled == False):
        if new_name == '' or new_dob == '' or new_starting_date == '':
            messagebox.showinfo('Empty Box','Please fill in information into every field')
            break
        else:
            filled = True

    if filled == True:
        con = sql.connect('codfatherdata.db')
        cur = con.cursor()

        cur.execute(f"SELECT * from Staff WHERE Username='{new_name}'")
        registeredusers = cur.fetchone();
        if registeredusers is not None:
            Username, DOB, starting_date, staffid = registeredusers
            messagebox.showinfo('Unable','There is already a user with the username ' + str(new_name))

        else:
            con = sql.connect("codfatherdata.db")
            cur = con.cursor()
            cur.execute("UPDATE Staff SET Username = ?, DOB = ?, Starting_Date = ? WHERE Username = ? AND DOB = ? AND Starting_Date = ?",(new_name, new_dob, new_starting_date, name, dob, starting_date))
            messagebox.showinfo('User added','The User ' + new_name + ' has been added to the database.')
            con.commit()



def edit_ownermenu():
    selected_item = ownermenutreeview.selection()
    if not selected_item:
        messagebox.showinfo('', 'You must select a variable to edit before clicking this button')
        return
    
    item_data = ownermenutreeview.item(selected_item)["values"]
    item_NO, name, price = item_data

    newname.set(name)
    newprice.set(price)
    
    raise_frame(editingownermenuframe)

def edit_staffmenu():
    selected_item = staffmenutreeview.selection()
    if not selected_item:
        messagebox.showinfo('', 'You must select a variable to edit before clicking this button')
        return
    
    item_data = staffmenutreeview.item(selected_item)["values"]
    item_NO, name, price = item_data

    staffnewname.set(name)
    staffnewprice.set(price)
    
    raise_frame(editingstaffmenuframe)
    
def saveownermenuedits():
    selected_item = ownermenutreeview.selection()
    item_data = ownermenutreeview.item(selected_item)["values"]
    item_NO, name, price = item_data
    new_name = newname.get()
    new_price = newprice.get()
    filled = False

    while(filled == False):
        if new_price.isalpha():
            messagebox.showinfo('','The Price must be a integer')
            break
        if new_name == '' or new_price == '':
            messagebox.showinfo('', 'Please enter information into both boxes')
            break
        else:
            filled = True
            
    

    if filled == True:
        con = sql.connect('codfatherdata.db')
        cur = con.cursor()

        cur.execute(f"SELECT * from menu WHERE Item_NO='{new_name}'")
        registeredusers = cur.fetchone();
        if registeredusers is not None:
            pass
            #item_NO, Name, Price = registeredusers
            #messagebox.showinfo('Unable','There is already an item with the ID ' + str(new_item_NO))

        else:
            con = sql.connect("codfatherdata.db")
            cur = con.cursor()
            cur.execute("UPDATE menu SET Name = ?, Price = ? WHERE Item_NO = ?", (new_name, new_price, item_NO))
            messagebox.showinfo('Item added','The Item ' + new_name + ' has been added to the database.')
            con.commit()

def savestaffmenuedits():
    selected_item = staffmenutreeview.selection()
    item_data = staffmenutreeview.item(selected_item)["values"]
    item_NO, name, price = item_data
    new_name = staffnewname.get()
    new_price = staffnewprice.get()
    filled = False


    while(filled == False):
        if new_price.isalpha():
            messagebox.showinfo('','Price must be an Integer')
            break
        elif new_name == '' or new_price == '':
            messagebox.showinfo('Empty Box','Please fill in information into every field')
            break
        else:
            filled = True

    if filled == True:
        con = sql.connect('codfatherdata.db')
        cur = con.cursor()

        cur.execute(f"SELECT * from menu WHERE Item_NO='{new_name}'")
        registeredusers = cur.fetchone();
        if registeredusers is not None:
            pass
            #item_NO, Name, Price = registeredusers
            #messagebox.showinfo('Unable','There is already an item with the ID ' + str(new_item_NO))

        else:
            con = sql.connect("codfatherdata.db")
            cur = con.cursor()
            cur.execute("UPDATE menu SET Name = ?, Price = ? WHERE Item_NO = ?", (new_name, new_price, item_NO))
            messagebox.showinfo('Item added','The Item ' + new_name + ' has been added to the database.')
            con.commit()

def ownermenuback():
    raise_frame(ownermenuframe)
    root.geometry('1150x700')

    newname.set('')
    newprice.set('')

    load_menutreeview()

def ownerstaffback():
    raise_frame(ownerstaffframe)
    root.geometry('1150x700')

    newname.set('')
    newprice.set('')

    load_menutreeview()
    

def addstaffmember():
    firstnametoadd = newstaffmemberfirstname.get()
    surnametoadd = newstaffmembersurname.get()
    DOBtoadd = newstaffmemberDOB.get()
    startingdatetoadd = newstaffmemberstartingdate.get()
    filled = False
    usernameID = random.randint(0,999)

    usernametoadd = firstnametoadd + " " + surnametoadd

    while(filled == False):
        if firstnametoadd == '' or surnametoadd == '' or DOBtoadd == '' or startingdatetoadd == '':
            messagebox.showinfo('Empty Box',' Please fill in information into every field')
            break
        elif not firstnametoadd.isalpha():
            messagebox.showinfo('','Firstname cannot be a number')
            break
        elif not surnametoadd.isalpha():
            messagebox.showinfo('','Surname cannot be a number')
            break
        elif not re.match(r'\d{2}/\d{2}/\d{2}', DOBtoadd):
            messagebox.showinfo('', 'DOB must be entered in the format dd/mm/yy')
            break
        elif not re.match(r'\d{2}/\d{2}/\d{2}', startingdatetoadd):
            messagebox.showinfo('', 'Starting Date must be entered in the format dd/mm/yy')
            break
        else:
            filled = True

    if filled == True:
        con = sql.connect("codfatherdata.db")
        cur = con.cursor()

        cur.execute(f"SELECT * from Staff WHERE staffID = '{usernameID}'")
        registeredusernames = cur.fetchone();
        if registeredusernames is not None:
            Username, DOB, Starting_Date, staffID = registeredusernames
            messagebox.showinfo('Unable','There is already a Staff member with the ID ' + str(Username))

        else:
            con = sql.connect('codfatherdata.db')
            cur = con.cursor()
            cur.execute("INSERT INTO Staff (Username, DOB, Starting_Date, staffID) VALUES (?, ?, ?, ?)",
                        (usernametoadd, DOBtoadd, startingdatetoadd, usernameID))
            messagebox.showinfo('Member Added','The User ' + usernametoadd + ' has been added to the staff database.')
            con.commit()

            
def savenewadmin():
    accesslevel = 'owner'

    firstnametoadd = newadminfirstname.get()
    surnametoadd = newadminsurname.get()
    passwordtosave = newadminpassword.get()

    usernametosave = firstnametoadd + surnametoadd
    filled = False

    while(filled == False):
        if firstnametoadd == '' or surnametoadd == '' or passwordtosave == '':
            messagebox.showinfo('','Please fill in information into every field')
            break
        elif not firstnametoadd.isalpha():
            messagebox.showinfo('','The firstname cannot be a number')
            break
        elif not surnametoadd.isalpha():
            messagebox.showinfo('','Surname cannot be a number')
            break
        else:
            filled = True

    if filled == True:
        con = sql.connect('codfatherdata.db')
        cur = con.cursor()

        cur.execute(f"SELECT * from Users WHERE Username='{usernametosave}'")
        registeredusernames = cur.fetchone();
        if registeredusernames is not None:
            Username, password, access = registeredusernames
            messagebox.showinfo('Unable','There is already a user with the username ' + str(Username))

        else:
            con = sql.connect("codfatherdata.db")
            cur = con.cursor()
            cur.execute("INSERT INTO Users (Username, password, access) VALUES (?, ?, ?)",
                    (usernametosave, passwordtosave, accesslevel))
            messagebox.showinfo('User added','The User ' + usernametosave + ' has been added to the database.')
            con.commit()
        
    
                                
def addstafflogin():
    accesslevel = 'staff'
    #we must first get the username and password to be entered into the database and then we must add them alongisde the level of access in the next blank
    passwordtoadd = newstaffloginpassword.get()
    usernametoadd = newstaffloginusername.get()
    filled = False

    while(filled == False):
        if usernametoadd == '' or passwordtoadd == '':
            messagebox.showinfo('Empty Box','Please fill in information into every field')
            break
        elif not usernametoadd.isalpha():
            messagebox.showinfo('','The Username must be a word')
            break
        else:
            filled = True

    if filled == True:
        con = sql.connect('codfatherdata.db')
        cur = con.cursor()

        cur.execute(f"SELECT * from Users WHERE Username='{usernametoadd}'")
        registeredusernames = cur.fetchone();
        if registeredusernames is not None:
            Username, password, access = registeredusernames
            messagebox.showinfo('Unable','There is already a user with the username ' + str(Username))

        else:
            con = sql.connect("codfatherdata.db")
            cur = con.cursor()
            cur.execute("INSERT INTO Users (Username, password, access) VALUES (?, ?, ?)",
                    (usernametoadd, passwordtoadd, accesslevel))
            messagebox.showinfo('User added','The User ' + usernametoadd + ' has been added to the database.')
            con.commit()

def opennewstafflogin():
    raise_frame(newstaffloginframe)

def opennewstaffmember():
    raise_frame(newstaffmemberframe)

def addorder():
    raise_frame(newownerorderframe)
    con = sqlite3.connect("codfatherdata.db")
    cur = con.cursor()
    cur.execute("DELETE FROM temporder")
    con.commit()

def addstafforder():
    raise_frame(newstafforderframe)
    con = sqlite3.connect("codfatherdata.db")
    cur = con.cursor()
    cur.execute("DELETE FROM temporder")
    con.commit()

def addcustomerorder():
    raise_frame(newcustomerorderframe)
    con = sqlite3.connect("codfatherdata.db")
    cur = con.cursor()
    cur.execute("DELETE FROM temporder")
    con.commit()

def raisenewreviewframe():
    raise_frame(newreviewframe)
    

def backtoownerstaff():
    raise_frame(ownerstaffframe)
    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Staff')
    staff_data = cursor.fetchall()


    ownerstafftreeview = ttk.Treeview(ownerstaffframe, height = 15, columns = ('Name', 'DOB', 'Starting Date', 'userID'),
                                  show = 'headings')

    ownerstafftreeview.grid(row = 4, column = 0, columnspan = 4)

    ownerstafftreeview.heading('Name',text = 'Name')
    ownerstafftreeview.column('Name',minwidth = 0, width = 150, anchor = 'center')
    ownerstafftreeview.heading('DOB',text = 'DOB')
    ownerstafftreeview.column('DOB',minwidth = 0, width = 130, anchor = 'center')
    ownerstafftreeview.heading('Starting Date',text = 'Starting Date')
    ownerstafftreeview.column('Starting Date',minwidth = 0, width = 130, anchor = 'center')
    ownerstafftreeview.heading('userID', text = 'userID')
    ownerstafftreeview.column('userID',minwidth = 0, width = 130, anchor = 'center')


    ownerstafftreeview.delete(*ownerstafftreeview.get_children())
    for data in staff_data:
        ownerstafftreeview.insert('','end', values=data)


    ttk.Style().theme_use('default')
    ttk.Style().configure('Treeview.heading',background = 'black', foreground = 'white', font = 'Verdana 10 bold')
    ttk.Style().configure('Treeview.Column',font = 'Verdana 10')

    newstaffmemberfirstname.set('')
    newstaffmembersurname.set('')
    newstaffmemberDOB.set('')
    newstaffmemberstartingdate.set('')

    load_menutreeview()

def load_ownerstafftreeview():
    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Staff")
    data = cursor.fetchall()

    for i in ownerstafftreeview.get_children():
        ownerstafftreeview.delete(i)

    for row in data:
        ownerstafftreeview.insert("",END, values=row)

    conn.close()

def load_userlogintreeview():
    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Users WHERE Access IN (?, ?)', ('customer', 'staff'))
    data = cursor.fetchall()

    for i in userlogintreeview.get_children():
        userlogintreeview.delete(i)

    for row in data:
        userlogintreeview.insert("",END, values=row)

    conn.close()



def load_tempordertreeview():

    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM temporder')
    data = cursor.fetchall()

    for i in ownertempordertreeview.get_children():
        ownertempordertreeview.delete(i)

    for row in data:
        ownertempordertreeview.insert("",END, values=row)

    for i in stafftempordertreeview.get_children():
        stafftempordertreeview.delete(i)

    for row in data:
        stafftempordertreeview.insert("",END, values=row)

    for i in customertempordertreeview.get_children():
        customertempordertreeview.delete(i)

    for row in data:
        customertempordertreeview.insert("",END, values=row)

    conn.close()



    
def deletestaffmember():
    selected_item = ownerstafftreeview.selection()
    if not selected_item:
        messagebox.showinfo('','You must select a variable to edit before clicking this button')
        return
    
    item_data = ownerstafftreeview.item(selected_item)["values"]
    name, dob, starting_date, staffID  = item_data
    

    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Staff WHERE Username = ? AND DOB = ? AND Starting_Date = ? AND staffID', (name, dob, starting_date, staffID))
    conn.commit()
    conn.close()

    load_ownerstafftreeview()

    

def raiseuserlogin():
    raise_frame(deleteuserloginframe)
    root.geometry('1150x750')

def deleteuserlogin():
    selected_item = userlogintreeview.selection()
    if not selected_item:
        messagebox.showinfo('','You must select a login to remove before clicking this')
        return

    item_data = userlogintreeview.item(selected_item)["values"]
    username, password, access = item_data

    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Users WHERE Username = ? AND password = ? AND access = ?', (username, password, access))
    conn.commit()
    conn.close()

    load_userlogintreeview()

def backtoreview():
    raise_frame(customerreviewframe)
    root.geometry('1150x700')

    #Here i am reloading all review treeviews to ensure that the new data is displayed
    #Reloading the Customer review treeview
    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM reviews')
    data = cursor.fetchall()

    for i in customerreviewtreeview.get_children():
        customerreviewtreeview.delete(i)

    for row in data:
        customerreviewtreeview.insert("",END, values=row)

    conn.close()
    #Reloading the Staff Review Treeview

    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM reviews')
    data = cursor.fetchall()

    for i in staffreviewtreeview.get_children():
        staffreviewtreeview.delete(i)

    for row in data:
        staffreviewtreeview.insert("",END, values=row)

    conn.close()

    #Reloading the Owner Review Treeview
    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM reviews')
    data = cursor.fetchall()

    for i in ownerreviewtreeview.get_children():
        ownerreviewtreeview.delete(i)

    for row in data:
        ownerreviewtreeview.insert("",END, values=row)

    conn.close()

    


def savereview():
    nametoadd = reviewname.get()
    creationdatetoadd = reviewdate.get()
    ratingtoadd = reviewrating.get()
    commenttoadd = reviewcomment.get()
    newreviewID = random.randint(0,999)
    filled = False

    while(filled == False):
        if nametoadd == '' or creationdatetoadd == '' or ratingtoadd == '' or commenttoadd == '':
            messagebox.showinfo('Empty Box',' Please fill in information into every field')
            break
        elif ratingtoadd not in ['0', '1', '2', '3', '4', '5']:
            messagebox.showinfo('','The Rating must be a number between, and including 0-5 ')
            break
        elif not re.match(r'\d{2}/\d{2}/\d{2}$', creationdatetoadd):
            messagebox.showinfo('', 'Creation Date must be entered in the format dd/mm/yy')
            break
        elif not nametoadd.isalpha():
            messagebox.showinfo('','The Name cannot be just a number')
            break
        else:
            filled = True

    if filled == True:
        con = sql.connect('codfatherdata.db')
        cur = con.cursor()
        cur.execute("INSERT INTO reviews (Name, Date_Made, Rating, Comment, ReviewID) VALUES (?, ?, ?, ?, ?)",
                    (nametoadd, creationdatetoadd, ratingtoadd, commenttoadd, newreviewID))
        messagebox.showinfo('Member Added','The review by the name of ' + nametoadd + ' has been added to the review database.')
        con.commit()

def temp_text(e):
    reviewratingentry.delete(0,"end")

#-------Commands for the New Owner Order frame
def backtoownermenu():
    raise_frame(ownermenuframe)
    root.geometry('1150x700')
    con = sqlite3.connect("codfatherdata.db")
    cur = con.cursor()
    cur.execute("DELETE FROM temporder")
    con.commit()

    load_ordertreeview()
    load_tempordertreeview()

def addownertempitem():
    selected_item = newownerordertreeview.selection()
    if not selected_item:
        messagebox.showinfo('','You must select an item to add before clicking this')
        return

    item_data = newownerordertreeview.item(selected_item)["values"]
    Item_No, Name, Price = item_data

    con = sql.connect('codfatherdata.db')
    cur = con.cursor()
    cur.execute("INSERT INTO temporder (Item_NO, Name, Price) VALUES (?, ?, ?)",
                (Item_No, Name, Price))
    messagebox.showinfo('Member Added','Item has been added')
    con.commit()

    load_tempordertreeview()

def removeitem():
    selected_item = ownertempordertreeview.selection()
    if not selected_item:
        messagebox.showinfo('','You must select an item to remove before clicking this')
        return

    item_data = ownertempordertreeview.item(selected_item)["values"]
    item_no, name, price = item_data

    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM temporder WHERE Item_NO = ? AND Name = ? AND Price = ?', (item_no, name, price))
    conn.commit()
    conn.close()

    load_tempordertreeview()

def removemenuitem():
    selected_item = ownermenutreeview.selection()
    if not selected_item:
        messagebox.showinfo('','You must select an item to remove before clicking this')
        return

    item_data = ownermenutreeview.item(selected_item)["values"]
    item_no, name, price = item_data

    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM menu WHERE Item_NO = ? AND Name = ? AND Price = ?', (item_no, name, price))
    conn.commit()
    conn.close()

    load_menutreeview()

def addneworder():
    firstnametoadd = orderfirstname.get()
    surnametoadd = ordersurname.get()
    dateofdelivery = orderdateofdelivery.get()
    neworderID = random.randint(0,999)
    filled = False

    ordernametosave = firstnametoadd + " " + surnametoadd
    
    total_orderprice = 0
    for row in ownertempordertreeview.get_children():
        price = ownertempordertreeview.item(row)['values'][2]
        total_orderprice += float(price)

    con = sql.connect('codfatherdata.db')
    cur = con.cursor()
    item_nos = []
    cur.execute("SELECT Item_NO FROM temporder")
    rows = cur.fetchall()
    for row in rows:
        item_nos.append(row[0])

    while filled == False:
        if firstnametoadd == '' or surnametoadd == '' or dateofdelivery == '':
            messagebox.showinfo('Empty Box',' Please fill in information into every field')
            break
        elif not firstnametoadd.isalpha():
            messagebox.showinfo('','Firstname must be a word')
            break
        elif not surnametoadd.isalpha():
            messagebox.showinfo('','Surname must be a word')
            break
        elif not re.match(r'\d{2}/\d{2}/\d{2}', dateofdelivery):
            messagebox.showinfo('', 'Date must be entered in the format dd/mm/yy')
        
            break
        else:
            filled = True

    if filled == True:
        date_obj = datetime.datetime.strptime(dateofdelivery, '%d/%m/%Y').strftime('%d/%m/%Y')
        item_nos_str = ','.join(map(str, item_nos))
        cur.execute("INSERT INTO 'orders' (name, date_of_delivery, item_numbers, total_price, orderID) VALUES (?, ?, ?, ?, ?)",
                    (ordernametosave, date_obj, item_nos_str, total_orderprice, neworderID))
        messagebox.showinfo('Order Added', f'The order by the name of {ordernametosave} has been added to the database.')
        con.commit()
        
            

        
#-----Commands for new Staff order frame-----

def backtostaffmenu():
    raise_frame(staffmenuframe)
    root.geometry('1150x700')
    con = sqlite3.connect("codfatherdata.db")
    cur = con.cursor()
    cur.execute("DELETE FROM temporder")
    con.commit()

    load_ordertreeview()

    load_menutreeview()
    load_tempordertreeview()

def addstafftempitem():
    selected_item = newstaffordertreeview.selection()
    if not selected_item:
        messagebox.showinfo('','You must select an item to add before clicking this')
        return

    item_data = newstaffordertreeview.item(selected_item)["values"]
    Item_No, Name, Price = item_data

    con = sql.connect('codfatherdata.db')
    cur = con.cursor()
    cur.execute("INSERT INTO temporder (Item_NO, Name, Price) VALUES (?, ?, ?)",
                (Item_No, Name, Price))
    messagebox.showinfo('Member Added','Item has been added')
    con.commit()

    load_tempordertreeview()

def removestaffitem():
    selected_item = stafftempordertreeview.selection()
    if not selected_item:
        messagebox.showinfo('','You must select an item to remove before clicking this')
        return

    item_data = stafftempordertreeview.item(selected_item)["values"]
    item_no, name, price = item_data

    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM temporder WHERE Item_NO = ? AND Name = ? AND Price = ?', (item_no, name, price))
    conn.commit()
    conn.close()

    load_tempordertreeview()

def addnewstafforder():
    firstnametoadd = stafforderfirstname.get()
    surnametoadd = staffordersurname.get()
    dateofdelivery = stafforderdateofdelivery.get()
    filled = False

    ordernametosave = firstnametoadd + " " + surnametoadd
    
    total_orderprice = 0
    for row in stafftempordertreeview.get_children():
        price = stafftempordertreeview.item(row)['values'][2]
        total_orderprice += float(price)

    con = sql.connect('codfatherdata.db')
    cur = con.cursor()
    item_nos = []
    cur.execute("SELECT Item_NO FROM temporder")
    rows = cur.fetchall()
    for row in rows:
        item_nos.append(row[0])

    while filled == False:
        if firstnametoadd == '' or surnametoadd == '' or dateofdelivery == '':
            messagebox.showinfo('Empty Box',' Please fill in information into every field')
            break
        elif not firstnametoadd.isalpha():
            messagebox.showinfo('','Firstname must be a word')
            break
        elif not surnametoadd.isalpha():
            messagebox.showinfo('','Surname must be a word')
            break
        elif not re.match(r'\d{2}/\d{2}/\d{2}', dateofdelivery):
            messagebox.showinfo('', 'Date must be entered in the format dd/mm/yy')
        
            break
        else:
            filled = True

    if filled == True:
        date_obj = datetime.datetime.strptime(dateofdelivery, '%d/%m/%Y').strftime('%d/%m/%Y')
        item_nos_str = ','.join(map(str, item_nos))
        cur.execute("INSERT INTO 'orders' (name, date_of_delivery, item_numbers, total_price, orderID) VALUES (?, ?, ?, ?, ?)",
                    (ordernametosave, date_obj, item_nos_str, total_orderprice, neworderID))
        messagebox.showinfo('Order Added', f'The order by the name of {ordernametosave} has been added to the database.')
        con.commit()



        
#-----Commands for new customer order frame

def backtocustomermenu():
    raise_frame(customermenuframe)
    root.geometry('1150x700')
    con = sqlite3.connect("codfatherdata.db")
    cur = con.cursor()
    cur.execute("DELETE FROM temporder")
    con.commit()

    load_ordertreeview()

    load_tempordertreeview()

def addcustomertempitem():
    selected_item = newcustomerordertreeview.selection()
    if not selected_item:
        messagebox.showinfo('','You must select a login to remove before clicking this')
        return

    item_data = newcustomerordertreeview.item(selected_item)["values"]
    Item_No, Name, Price = item_data

    con = sql.connect('codfatherdata.db')
    cur = con.cursor()
    cur.execute("INSERT INTO temporder (Item_NO, Name, Price) VALUES (?, ?, ?)",
                (Item_No, Name, Price))
    messagebox.showinfo('Member Added','Item has been added')
    con.commit()

    load_tempordertreeview()

def removecustomeritem():
    selected_item = customertempordertreeview.selection()
    if not selected_item:
        messagebox.showinfo('','You must select an item to remove before clicking this')
        return

    item_data = customertempordertreeview.item(selected_item)["values"]
    item_no, name, price = item_data

    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM temporder WHERE Item_NO = ? AND Name = ? AND Price = ?', (item_no, name, price))
    conn.commit()
    conn.close()

    load_tempordertreeview()

def addnewcustomerorder():
    firstnametoadd = customerorderfirstname.get()
    surnametoadd = customerordersurname.get()
    dateofdelivery = customerorderdateofdelivery.get()
    filled = False

    ordernametosave = firstnametoadd + " " + surnametoadd
    
    total_orderprice = 0
    for row in customertempordertreeview.get_children():
        price = customertempordertreeview.item(row)['values'][2]
        total_orderprice += float(price)

    con = sql.connect('codfatherdata.db')
    cur = con.cursor()
    item_nos = []
    cur.execute("SELECT Item_NO FROM temporder")
    rows = cur.fetchall()
    for row in rows:
        item_nos.append(row[0])

    while filled == False:
        if firstnametoadd == '' or surnametoadd == '' or dateofdelivery == '':
            messagebox.showinfo('Empty Box',' Please fill in information into every field')
            break
        elif not firstnametoadd.isalpha():
            messagebox.showinfo('','Firstname must be a word')
            break
        elif not surnametoadd.isalpha():
            messagebox.showinfo('','Surname must be a word')
            break
        elif not re.match(r'\d{2}/\d{2}/\d{2}', dateofdelivery):
            messagebox.showinfo('', 'Date must be entered in the format dd/mm/yy')
        
            break
        else:
            filled = True

    if filled == True:
        date_obj = datetime.datetime.strptime(dateofdelivery, '%d/%m/%Y').strftime('%d/%m/%Y')
        item_nos_str = ','.join(map(str, item_nos))
        cur.execute("INSERT INTO 'orders' (name, date_of_delivery, item_numbers, total_price, orderID) VALUES (?, ?, ?, ?, ?)",
                    (ordernametosave, date_obj, item_nos_str, total_orderprice, neworderID))
        messagebox.showinfo('Order Added', f'The order by the name of {ordernametosave} has been added to the database.')
        con.commit()

#-----End of Commands for the 3 different order frames------
        
def raiseadditem():
    raise_frame(addnewmenuitemframe)

def addnewitem():
    newitem_number = random.randint(1, 200)
    itemnametoadd = newitemname.get()
    itempricetoadd = newitemprice.get()
    filled = False

    while(filled == False):
        if newitem_number == '' or itemnametoadd == '' or itempricetoadd == '':
            messagebox.showinfo('Empty Box',' Please fill in information into every field')
            break
        elif not itemnametoadd.isalpha():
            messagebox.showinfo('','The Name cannot be just a number')
            break
        elif itempricetoadd.isalpha():
            messagebox.showinfo('','The Price must be a number, not text')
            break
        else:
            filled = True

    if filled == True:
        con = sql.connect('codfatherdata.db')
        cur = con.cursor()
        cur.execute("INSERT INTO menu (Item_NO, Name, Price) VALUES (?, ?, ?)",
                    (newitem_number, itemnametoadd, itempricetoadd))
        messagebox.showinfo('Member Added','The item by the name of ' + itemnametoadd + ' has been added to the menu database.')
        con.commit()

def raisenewadmin():
    raise_frame(newadminframe)
    root.geometry('1150x700')

def load_admintreeview():
    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE access = "owner"')
    admin_data = cursor.fetchall()

    cur = conn.cursor()
    cur.execute('SELECT * FROM cache')
    cache_data = cur.fetchall()

    for i in deladmintreeview.get_children():
        deladmintreeview.delete(i)

    for data in admin_data:
        if (data[0], data[2]) not in [(cache[0], cache[1]) for cache in cache_data]:
            deladmintreeview.insert('','end', values=data)

    conn.close()

    

    
def deleteadmin():
    selected_item = deladmintreeview.selection()
    if not selected_item:
        messagebox.showinfo('','You must select an item to remove before clicking this')
        return

    admin_data = deladmintreeview.item(selected_item)["values"]
    username, password, access_level = admin_data

    conn = sqlite3.connect('codfatherdata.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Users WHERE username = ? AND password = ? AND access = ?', (username, password, access_level))
    conn.commit()
    conn.close()

    load_admintreeview()

    

def raisedeladmin():
    raise_frame(deladminframe)
    root.geometry('1150x700')

    load_admintreeview()
        
#---------------------------------------Main Code----------------
    
root = Tk()
root.resizable(width=False,height=False)
root.geometry('400x500')
root.title('The Codfather')
root.configure(bg = 'white')

#---------Frame-------

loginframe = Frame(root, bg = 'white')


menuframe = Frame(root, bg = 'white')


ownerdashboardframe = Frame(root, bg = 'white')


staffframe = Frame(root, bg = 'white')

customerframe = Frame(root, bg = 'white')

newcustomerframe = Frame(root, bg = 'white')

editingstaffframe = Frame(root, bg = 'white')

editingownermenuframe = Frame(root, bg = 'white')

editingstaffmenuframe = Frame(root, bg = 'white')

newstaffloginframe = Frame(root, bg = 'white')

newstaffmemberframe = Frame(root, bg = 'white')

deleteuserloginframe = Frame(root, bg = 'white')

newreviewframe = Frame(root, bg = 'white')

newownerorderframe = Frame(root, bg = 'white')

newstafforderframe = Frame(root, bg = 'white')

newcustomerorderframe = Frame(root, bg = 'white')

addnewmenuitemframe = Frame(root, bg = 'white')

newadminframe = Frame(root, bg = 'white')

deladminframe = Frame(root, bg = 'white')


#----------Owner Frames-------

ownerdashboardframe = Frame(root, bg = 'white')
ownerreviewframe = Frame(root, bg = 'white')
ownerstaffframe = Frame(root, bg = 'white')
ownermenuframe = Frame(root, bg = 'white')
ownerorderframe = Frame(root, bg = 'white')

#----------Staff Frames-------

staffdashboardframe = Frame(root, bg = 'white')
staffreviewframe = Frame(root, bg = 'white')
staffstaffframe = Frame(root, bg = 'white')
staffmenuframe = Frame(root, bg = 'white')
stafforderframe = Frame(root, bg = 'white')

#-------Customer Frames-------

customerdashboardframe = Frame(root, bg = 'white')
customerreviewframe = Frame(root, bg = 'white')
customerstaffframe = Frame(root, bg = 'white')
customermenuframe = Frame(root, bg = 'white')
customerorderframe = Frame(root, bg = 'white')

for frame in(ownerdashboardframe,ownerreviewframe,ownerstaffframe,ownermenuframe,ownerorderframe):
    frame.grid(row=0,column=0,sticky='news')
    
for frame in(staffdashboardframe,staffreviewframe,staffstaffframe,staffmenuframe,stafforderframe):
    frame.grid(row=0,column=0,sticky='news')

for frame in(customerdashboardframe,customerreviewframe,customerstaffframe,customermenuframe,customerorderframe):
    frame.grid(row=0,column=0,sticky='news')

for frame in(loginframe,menuframe,staffframe,customerframe,newcustomerframe,deladminframe, editingstaffframe, newadminframe, editingownermenuframe, editingstaffmenuframe, newstaffloginframe, newstaffmemberframe, deleteuserloginframe, newreviewframe, newownerorderframe, newstafforderframe, newcustomerorderframe, addnewmenuitemframe):
    frame.grid(row = 0, column = 0, sticky = 'news')


#---------------------------------------Login Frame-------------


filename = 'codfatherlogo.png'
logo = PhotoImage(file = filename)
headerlabel = Label(loginframe, image = logo)
headerlabel.grid(row = 0, column = 0,columnspan=2)
    
usernamelabel = Label(loginframe, text = 'Username: ',font = ('Helvetica',18), fg = '#000C66',bg = 'white')
usernamelabel.config(height = 1, width = 10)
usernamelabel.grid(row = 2, column = 0, sticky = 'N')

username = StringVar()
usernametoget = Entry(loginframe, textvariable = username, fg = 'black', bg = 'white', borderwidth = 2, relief = 'solid')
usernametoget.grid(row = 2, column = 1, sticky = 'N')

passwordlabel = Label(loginframe, text = 'Password: ',font=('Helvetica',18), fg = '#000C66',bg = 'white')
passwordlabel.config(height = 1, width = 10)
passwordlabel.grid(row = 3, column = 0, sticky = 'S')

password = StringVar()
passwordtoget = Entry(loginframe, textvariable = password, fg = 'black',bg = 'white', borderwidth = 2, relief = 'solid')
passwordtoget.grid(row = 3, column = 1, sticky = 'N')
passwordtoget.config(show='•')


loginbutton = Button(loginframe, text = 'Login', command = login, fg = 'black', bg = 'white', borderwidth = 2, relief = 'raised')
loginbutton.config(height = 3, width = 15)
loginbutton.grid(row = 5, column = 1, sticky = 'S', rowspan = 2)

# bind the login function to the return key only within the loginframe
loginframe.bind("<Return>", lambda event: login())




spacer1 = Label(loginframe, text = 'blank',fg='white',bg='white')
spacer1.config(height = 2, width = 5)
spacer1.grid(row = 4, column = 1)

spacer3 = Label(loginframe, text = 'blank',fg='white',bg='white')
spacer3.config(height = 1, width = 5)
spacer3.grid(row = 7, column = 1)#THIS IS IN COLUMN 7 AS THE LOGINBUTTON IS ROWSPAN INTO COLUMN 6

spacer4 = Label(loginframe, text = 'blank', fg = 'white', bg = 'white')
spacer4.config(height = 2, width = 10)
spacer4.grid(row=4,column=0)

newcustomerbutton = Button(loginframe, text = 'New customer?', command = raise_newcustomerframe, bg = ("white"), fg = 'black', font = ('',13,'underline'), relief = 'flat')
newcustomerbutton.config(height = 1, width = 15)
newcustomerbutton.grid(row = 8, column = 1, sticky = 'N')

facebook_image = PhotoImage(file = 'facebooklogo.png')
facebookbutton = Button(loginframe, image = facebook_image, command = opencodfatherfacebook, borderwidth = 8, relief = 'raised')
facebookbutton.config(height=90,width=100)
facebookbutton.grid(row = 5, column = 0, rowspan = 4, sticky = 'E')

#--------------------New Admin Frame----------

newadminfirstnamelabel = Label(newadminframe, text = 'Firstname: ', bg = 'white', fg = 'black')
newadminfirstnamelabel.grid(row = 0, column = 0)

newadminfirstname = StringVar()
newadminfirstnameentry = Entry(newadminframe, textvariable = newadminfirstname, borderwidth = 2, relief = 'solid', fg = 'black', bg = 'white')
newadminfirstnameentry.grid(row = 0, column = 1)

newadminsurnamelabel = Label(newadminframe, text = 'Surname: ', bg = 'white', fg = 'black')
newadminsurnamelabel.grid(row = 1, column = 0)

newadminsurname = StringVar()
newadminsurnameentry = Entry(newadminframe, textvariable = newadminsurname, borderwidth = 2, relief = 'solid', fg = 'black', bg = 'white')
newadminsurnameentry.grid(row = 1, column = 1)


newadminpasswordlabel = Label(newadminframe, text = 'Password: ', bg = 'white', fg = 'black')
newadminpasswordlabel.grid(row = 2, column = 0)

newadminpassword = StringVar()
newadminpasswordentry = Entry(newadminframe, textvariable = newadminpassword, borderwidth = 2, relief = 'solid', fg = 'black', bg = 'white')
newadminpasswordentry.grid(row = 2, column = 1)

newadminback_btn = Button(newadminframe, text = 'Back', command = backtoownerstaff, fg = 'black', bg = 'white')
newadminback_btn.config(height = 3, width = 10)
newadminback_btn.grid(row = 3, column = 0)

newadminsave_btn = Button(newadminframe, text = 'Add Admin', command = savenewadmin, fg = 'black', bg = 'white')
newadminsave_btn.config(height = 3, width = 10)
newadminsave_btn.grid(row = 3, column = 1, sticky = 'E')


#---------------------Deleting Admin Frame--------------------------------------------

conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM Users WHERE access = "owner"')
admin_data = cursor.fetchall()

cur = conn.cursor()
cur.execute('SELECT * FROM cache')
cache_data = cur.fetchall()

deladmintreeview = ttk.Treeview(deladminframe, height = 15, columns = ('Username', 'Password', 'Access Level'),
                                  show = 'headings')

deladmintreeview.grid(row = 0, column = 0, columnspan = 4, rowspan = 2)

deladmintreeview.heading('Username',text = 'Username')
deladmintreeview.column('Username',minwidth = 0, width = 150, anchor = 'center')
deladmintreeview.heading('Password',text = 'Password')
deladmintreeview.column('Password',minwidth = 0, width = 180, anchor = 'center')
deladmintreeview.heading('Access Level',text = 'Access Level')
deladmintreeview.column('Access Level',minwidth = 0, width = 130, anchor = 'center')


for data in admin_data:
    if (data[0], data[2]) not in [(cache[0], cache[1]) for cache in cache_data]:
        deladmintreeview.insert('','end', values=data)


deladminback_btn = Button(deladminframe, text = 'Back', command = backtoownerstaff, fg = 'black', bg = 'white')
deladminback_btn.config(height = 3, width = 10)
deladminback_btn.grid(row = 2, column = 0)

deladmindel_btn = Button(deladminframe, text = 'Delete', command = deleteadmin, fg = 'black', bg = 'white')
deladmindel_btn.config(height = 3, width = 10)
deladmindel_btn.grid(row = 2, column = 1)

#--------------------Editing Staff Frame------------------------------------
editingstaffframespacer = Label(editingstaffframe, text = '')
editingstaffframespacer.grid(row=0,column=0)

newusernamelabel = Label(editingstaffframe, text = 'New Username: ', fg = 'black', bg = 'white')
newusernamelabel.grid(row = 1,column = 0)

newusername = StringVar()
newstaffusername = Entry(editingstaffframe, textvariable = newusername, fg = 'black', bg = 'white', borderwidth = 2, relief = 'solid')
newstaffusername.grid(row = 1, column = 1, sticky = 'N')

newDOBlabel = Label(editingstaffframe, text = 'New DOB: ', fg = 'black', bg = 'white')
newDOBlabel.grid(row = 2, column = 0, sticky = 'N')

newDOB = StringVar()
newstaffDOB = Entry(editingstaffframe, textvariable = newDOB, fg = 'black', bg = 'white', borderwidth = 2, relief = 'solid')
newstaffDOB.grid(row = 2, column = 1)

newstartingdatelabel = Label(editingstaffframe, text = 'New Starting Date', fg = 'black', bg = 'white')
newstartingdatelabel.grid(row= 3, column = 0)

newstartingdate = StringVar()
newstaffstartingdate = Entry(editingstaffframe, textvariable = newstartingdate, fg = 'black', bg = 'white', borderwidth = 2, relief = 'solid')
newstaffstartingdate.grid(row = 3, column = 1)

savestaffeditbutton = Button(editingstaffframe,text = 'Save', command = savestaffedits, fg='black',bg='white')
savestaffeditbutton.config(height=3,width=5)
savestaffeditbutton.grid(row=4,column=1)

staffeditorbackbutton = Button(editingstaffframe,text = 'Back', command = ownerstaffback, fg = 'black', bg = 'white')
staffeditorbackbutton.config(width = 5, height = 3)
staffeditorbackbutton.grid(row = 4, column = 0)

#--------Editing Owner Menu Frame-----------

editingownermenuframespacer = Label(editingownermenuframe, text = '')
editingownermenuframespacer.grid(row= 0, column = 0)


newnamelabel = Label(editingownermenuframe, text = 'New Name: ', fg = 'black', bg = 'white')
newnamelabel.grid(row = 2, column = 0, sticky = 'N')

newname = StringVar()
newnameentry = Entry(editingownermenuframe, textvariable = newname, fg = 'black', bg = 'white', borderwidth = 2, relief = 'solid')
newnameentry.grid(row = 2, column = 1)

newpricelabel = Label(editingownermenuframe, text = 'New Price: ', fg = 'black', bg = 'white')
newpricelabel.grid(row= 3, column = 0)

newprice = StringVar()
newitemprice = Entry(editingownermenuframe, textvariable = newprice, fg = 'black', bg = 'white', borderwidth = 2, relief = 'solid')
newitemprice.grid(row = 3, column = 1)

savemenueditbutton = Button(editingownermenuframe,text = 'Save', command = saveownermenuedits, fg='black',bg='white')
savemenueditbutton.config(height=3,width=5)
savemenueditbutton.grid(row=4,column=1)

menueditorbackbutton = Button(editingownermenuframe,text = 'Back', command = ownermenuback, fg = 'black', bg = 'white')
menueditorbackbutton.config(width = 5, height =3)
menueditorbackbutton.grid(row = 4, column = 0)

#--------Editing Staff Menu Frame----------

staffeditingstaffmenuframespacer = Label(editingstaffmenuframe, text = '')
staffeditingstaffmenuframespacer.grid(row= 0, column = 0)

staffnewnamelabel = Label(editingstaffmenuframe, text = 'New Name: ', fg = 'black', bg = 'white')
staffnewnamelabel.grid(row = 2, column = 0, sticky = 'N')

staffnewname = StringVar()
staffnewnameentry = Entry(editingstaffmenuframe, textvariable = staffnewname, fg = 'black', bg = 'white', borderwidth = 2, relief = 'solid')
staffnewnameentry.grid(row = 2, column = 1)

staffnewpricelabel = Label(editingstaffmenuframe, text = 'New Price: ', fg = 'black', bg = 'white')
staffnewpricelabel.grid(row= 3, column = 0)

staffnewprice = StringVar()
staffnewitemprice = Entry(editingstaffmenuframe, textvariable = staffnewprice, fg = 'black', bg = 'white', borderwidth = 2, relief = 'solid')
staffnewitemprice.grid(row = 3, column = 1)

staffsavemenueditbutton = Button(editingstaffmenuframe,text = 'Save', command = savestaffmenuedits, fg='black',bg='white')
staffsavemenueditbutton.config(height=3,width=5)
staffsavemenueditbutton.grid(row=4,column=1)

staffmenueditorbackbutton = Button(editingstaffmenuframe,text = 'Back', command = backtostaffmenu, fg = 'black', bg = 'white')
staffmenueditorbackbutton.config(width = 5, height =3)
staffmenueditorbackbutton.grid(row = 4, column = 0)

#--------Adding Staff Login Frame---------

newstafflogintitle = Label(newstaffloginframe, text = 'New Staff Login', fg = 'blue', bg ='white', font = ('Helvetica',30, 'bold',  'underline'))
newstafflogintitle.config(height=2,width=20)
newstafflogintitle.grid(row=0,column=0,columnspan=3)

newstafflogininstructions = Label(newstaffloginframe, text = '•Please enter the Username and Password you would like to assign.', fg = 'red', bg ='white', font = ('Helvetica',10,'bold'))
newstafflogininstructions.config(height=4,width=60)
newstafflogininstructions.grid(row=1,column=0,columnspan = 2, sticky = 'W')

newstaffloginusernamelabel = Label(newstaffloginframe, text = 'Username: ', fg = 'black', bg = 'white')
newstaffloginusernamelabel.config(height = 3)
newstaffloginusernamelabel.grid(row = 2, column = 0, sticky = 'W')

newstaffloginusername = StringVar()
newstaffloginusernameentry = Entry(newstaffloginframe, textvariable = newstaffloginusername, fg = 'black', bg = 'white', borderwidth = 2, relief = 'solid')
newstaffloginusernameentry.grid(row = 2, column = 1, sticky = 'W')

newstaffloginpasswordlabel = Label(newstaffloginframe, text = 'Password: ', fg ='black',bg='white')
newstaffloginpasswordlabel.config(height = 3)
newstaffloginpasswordlabel.grid( row = 3, column = 0, sticky = 'W')

newstaffloginpassword = StringVar()
newstaffloginpasswordentry = Entry(newstaffloginframe, textvariable = newstaffloginpassword, fg = 'black',bg = 'white', borderwidth = 2, relief = 'solid')
newstaffloginpasswordentry.grid(row = 3, column = 1, sticky = 'W')



newstaffloginspacer = Label(newstaffloginframe, text = 'blank', fg = 'white', bg = 'white')
newstaffloginspacer.config(height = 3)
newstaffloginspacer.grid(row = 4, column = 0)

newstaffloginbutton = Button(newstaffloginframe, text = 'Add Staff Login', command = addstafflogin, fg = 'black', bg = 'white')
newstaffloginbutton.config(height = 3,width = 15)
newstaffloginbutton.grid(row = 5, column = 1, sticky = 'W')

newstaffloginbackbutton = Button(newstaffloginframe, text = 'Back', command = openownerStaff, fg = 'black',bg='white')
newstaffloginbackbutton.config(height = 3, width = 15)
newstaffloginbackbutton.grid(row = 5, column = 0, sticky = 'W')

#--------Adding Staff Member Frame---------

newstaffmembertitle = Label(newstaffmemberframe, text = 'New Staff Member', fg = 'blue', bg ='white', font = ('Helvetica',30, 'bold',  'underline'))
newstaffmembertitle.config(height=2,width=20)
newstaffmembertitle.grid(row=0,column=0,columnspan=3)

newstaffmemberinstructions = Label(newstaffmemberframe, text = '•Enter the Firstname, Surname, DOB and starting Date', fg = 'red', bg ='white', font = ('Helvetica',10,'bold'))
newstaffmemberinstructions.config(height=4,width=60)
newstaffmemberinstructions.grid(row=1,column=0,columnspan = 2, sticky = 'W')

newstaffmemberfirstnamelabel = Label(newstaffmemberframe, text = 'Firstname: ', fg = 'black', bg = 'white')
newstaffmemberfirstnamelabel.config(height = 3)
newstaffmemberfirstnamelabel.grid(row = 2, column = 0, sticky = 'W')

newstaffmemberfirstname = StringVar()
newstaffmemberfirstnameentry = Entry(newstaffmemberframe, textvariable = newstaffmemberfirstname, fg = 'black', bg = 'white', borderwidth = 2, relief = 'solid')
newstaffmemberfirstnameentry.grid(row = 2, column = 1)

newstaffmembersurname = Label(newstaffmemberframe, text = 'Surname: ', fg = 'black', bg = 'white')
newstaffmembersurname.config(height = 3)
newstaffmembersurname.grid(row = 3, column = 0, sticky = 'W')

newstaffmembersurname = StringVar()
newstaffmembersurnameentry = Entry(newstaffmemberframe, textvariable = newstaffmembersurname, fg = 'black', bg = 'white', borderwidth = 2, relief = 'solid')
newstaffmembersurnameentry.grid(row = 3, column = 1)

newstaffmemberDOBlabel = Label(newstaffmemberframe, text = 'DOB: ', fg ='black',bg='white')
newstaffmemberDOBlabel.config(height = 3)
newstaffmemberDOBlabel.grid( row = 4, column = 0, sticky = 'W')

newstaffmemberDOB = StringVar()
newstaffmemberDOBentry = Entry(newstaffmemberframe, textvariable = newstaffmemberDOB, fg = 'black',bg = 'white', borderwidth = 2, relief = 'solid')
newstaffmemberDOBentry.grid(row = 4, column = 1)

newstaffmemberstartingdatelabel = Label(newstaffmemberframe, text = 'Starting Date: ', fg = 'black', bg = 'white')
newstaffmemberstartingdatelabel.config(height = 3)
newstaffmemberstartingdatelabel.grid(row = 5, column = 0, sticky = 'W')

newstaffmemberstartingdate = StringVar()
newstaffmemberstartingdateentry = Entry(newstaffmemberframe, textvariable = newstaffmemberstartingdate, fg = 'black', bg = 'white', borderwidth = 2, relief = 'solid')
newstaffmemberstartingdateentry.grid(row = 5, column = 1)



newstaffmemberspacer = Label(newstaffmemberframe, text = 'blank', fg = 'white', bg = 'white')
newstaffmemberspacer.config(height = 3)
newstaffmemberspacer.grid(row = 6, column = 0)

newstaffmemberbutton = Button(newstaffmemberframe, text = 'Add Staff Member', command = addstaffmember, fg = 'black', bg = 'white')
newstaffmemberbutton.config(height = 3,width = 15)
newstaffmemberbutton.grid(row = 7, column = 1, sticky = 'W')

newstaffmemberbackbutton = Button(newstaffmemberframe, text = 'Back', command = backtoownerstaff, fg = 'black',bg='white')
newstaffmemberbackbutton.config(height = 3, width = 15)
newstaffmemberbackbutton.grid(row = 7, column = 0, sticky = 'W')

#-------------Deleting Staff Login Frame---------------


conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM Users WHERE Access IN (?, ?)', ('customer', 'staff'))
user_data = cursor.fetchall()

userlogintreeview = ttk.Treeview(deleteuserloginframe, height = 15, columns = ('Username', 'Password', 'Access Level'),
                                  show = 'headings')

userlogintreeview.grid(row = 0, column = 0, columnspan = 4)

userlogintreeview.heading('Username',text = 'Username')
userlogintreeview.column('Username',minwidth = 0, width = 150, anchor = 'center')
userlogintreeview.heading('Password',text = 'Password')
userlogintreeview.column('Password',minwidth = 0, width = 180, anchor = 'center')
userlogintreeview.heading('Access Level',text = 'Access Level')
userlogintreeview.column('Access Level',minwidth = 0, width = 130, anchor = 'center')


for data in user_data:
    userlogintreeview.insert('','end', values=data)



#Basic code behind it to be able to use for other treeviews
#scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=treeview.yview)
#scrollbar.grid(row=0, column=4, sticky=(NS, W, E))
#treeview.configure(yscrollcommand=scrollbar.set)


ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'black', foreground = 'white', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')

informationlabel = Label(deleteuserloginframe, text = 'On the left are all the current logins in the system.', fg = 'black', bg = 'white')
informationlabel.grid(row = 0, column = 5)

deleteuserbackbtn = Button(deleteuserloginframe, text = 'Back', command = backtoownerstaff, fg = 'black', bg = 'white')
deleteuserbackbtn.grid(row = 1, column = 1)

deleteuserbtn = Button(deleteuserloginframe, text = 'Delete Login', command = deleteuserlogin, fg = 'black', bg = 'white')
deleteuserbtn.grid(row = 1, column = 2)

#------------------newreviewframe--------

#name,date,rating,comment

reviewtitle = Label(newreviewframe, text = 'New Review', fg = 'blue', bg ='white', font = ('Helvetica',30, 'bold',  'underline'))
reviewtitle.grid(row = 0, column=0)

reviewnamelabel = Label(newreviewframe, text = 'Name: ', fg = 'black', bg = 'white')
reviewnamelabel.grid(row = 1, column = 0, sticky = 'W')

reviewname = StringVar()
reviewnameentry = Entry(newreviewframe, textvariable = reviewname, fg = 'black', bg = 'white')
reviewnameentry.grid(row = 1, column = 1)

reviewdatelabel = Label(newreviewframe, text = 'Creation Date: ', fg = 'black', bg = 'white')
reviewdatelabel.grid(row = 2, column = 0, sticky = 'W')

reviewdate = StringVar()
reviewdateentry = Entry(newreviewframe, textvariable = reviewdate, fg = 'black', bg = 'white')
reviewdateentry.grid(row = 2, column = 1)

reviewratinglabel = Label(newreviewframe, text = 'Rating: ', fg = 'black', bg = 'white')
reviewratinglabel.grid(row = 3, column = 0, sticky = 'W')

reviewrating = StringVar()
reviewratingentry = Entry(newreviewframe, textvariable = reviewrating, fg = 'black', bg = 'white')
reviewratingentry.insert(0,'0-5')
reviewratingentry.grid(row = 3, column = 1)

reviewratingentry.bind("<FocusIn>", temp_text)

reviewcommentlabel = Label(newreviewframe, text = 'Comment: ', fg = 'black', bg = 'white')
reviewcommentlabel.grid(row = 4, column = 0, sticky = 'W')

reviewcomment = StringVar()
reviewcommententry = Entry(newreviewframe, textvariable = reviewcomment, fg = 'black', bg = 'white')
reviewcommententry.grid(row = 4, column = 1)

reviewbackbtn = Button(newreviewframe, text = 'Back', command = backtoreview, fg = 'black', bg = 'white')
reviewbackbtn.grid(row = 5, column = 0)

reviewsavebtn = Button(newreviewframe, text = 'Add Review', command = savereview, fg = 'black', bg = 'white')
reviewsavebtn.grid(row = 5, column = 1)
#--------------Owner New Order Frame-----------------------------

conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM menu')
order_data = cursor.fetchall()


newownerordertreeview = ttk.Treeview(newownerorderframe, height = 15, columns = ('Item Number', 'Name', 'Price'),
                                  show = 'headings')

newownerordertreeview.grid(row = 0, column = 0, columnspan = 4, rowspan = 2)

newownerordertreeview.heading('Item Number',text = 'Item Number')
newownerordertreeview.column('Item Number',minwidth = 0, width = 150, anchor = 'center')
newownerordertreeview.heading('Name',text = 'Name')
newownerordertreeview.column('Name',minwidth = 0, width = 130, anchor = 'center')
newownerordertreeview.heading('Price',text = 'Price')
newownerordertreeview.column('Price',minwidth = 0, width = 130, anchor = 'center')

newownerordertreeview.delete(*newownerordertreeview.get_children())
for data in order_data:
    newownerordertreeview.insert('','end', values=data)


ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'black', foreground = 'white', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')


neworderspacer = Label(newownerorderframe, text = '')
neworderspacer.config(width = 5)
neworderspacer.grid(row = 0,column = 5)



#This is the treeview where all the items added to the order will be stored, they can be removed or saved to the file
conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM temporder')
temporder_data = cursor.fetchall()

ownertempordertreeview = ttk.Treeview(newownerorderframe, height = 15, columns = ('Item Number', 'Name', 'Price'),
                                  show = 'headings')

ownertempordertreeview.grid(row = 0, column = 6, columnspan = 4, rowspan = 2)

ownertempordertreeview.heading('Item Number',text = 'Item Number')
ownertempordertreeview.column('Item Number',minwidth = 0, width = 150, anchor = 'center')
ownertempordertreeview.heading('Name',text = 'Name')
ownertempordertreeview.column('Name',minwidth = 0, width = 130, anchor = 'center')
ownertempordertreeview.heading('Price',text = 'Price')
ownertempordertreeview.column('Price',minwidth = 0, width = 130, anchor = 'center')

ownertempordertreeview.delete(*ownertempordertreeview.get_children())
for data in temporder_data:
    ownertempordertreeview.insert('','end', values=data)



ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'white', foreground = 'black', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')


neworderbackbtn = Button(newownerorderframe, text = 'Back',command = backtoownermenu, fg = 'black', bg = 'white')
neworderbackbtn.grid(row = 2, column = 0)

addtempitembtn = Button(newownerorderframe, text = 'Add Item', command = addownertempitem, fg = 'black', bg = 'white')
addtempitembtn.grid(row = 2, column = 1, sticky = 'E')

neworderspacer = Label(newownerorderframe, text = '')
neworderspacer.grid(row = 2, column = 3, rowspan = 3)

removeitembtn = Button(newownerorderframe, text = 'Remove Item',command = removeitem, fg = 'black', bg = 'white')
removeitembtn.grid(row = 2, column = 6)

additembtn = Button(newownerorderframe, text = 'Add Order', command = addneworder, fg = 'black', bg = 'white')
additembtn.grid(row=7, column = 1)

neworderspacer2 = Label(newownerorderframe, text = '')
neworderspacer2.grid(row = 3, column = 0)

orderfirstnamelabel = Label(newownerorderframe, text = 'Firstname: ', fg = 'black', bg = 'white')
orderfirstnamelabel.grid(row = 4, column = 0)

orderfirstname = StringVar()
orderfirstnameentry = Entry(newownerorderframe, textvariable = orderfirstname, fg = 'black', bg = 'white')
orderfirstnameentry.grid(row = 4, column = 1)

ordersurnamelabel = Label(newownerorderframe, text = 'Surname: ', fg = 'black', bg = 'white')
ordersurnamelabel.grid(row = 5, column = 0)

ordersurname = StringVar()
ordersurnameentry = Entry(newownerorderframe, textvariable = ordersurname, fg = 'black', bg = 'white')
ordersurnameentry.grid(row = 5, column = 1)

orderdateofdeliverylabel = Label(newownerorderframe, text = 'Date of Delivery: ', fg = 'black', bg = 'white')
orderdateofdeliverylabel.grid(row = 6, column = 0)

orderdateofdelivery = StringVar()
orderdateofdeliveryentry = Entry(newownerorderframe, textvariable = orderdateofdelivery, fg = 'black', bg = 'white')
orderdateofdeliveryentry.grid(row = 6, column = 1)

#--------------Staff New Order Frame---------------

conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM menu')
order_data = cursor.fetchall()


newstaffordertreeview = ttk.Treeview(newstafforderframe, height = 15, columns = ('Item Number', 'Name', 'Price'),
                                  show = 'headings')

newstaffordertreeview.grid(row = 0, column = 0, columnspan = 4, rowspan = 2)

newstaffordertreeview.heading('Item Number',text = 'Item Number')
newstaffordertreeview.column('Item Number',minwidth = 0, width = 150, anchor = 'center')
newstaffordertreeview.heading('Name',text = 'Name')
newstaffordertreeview.column('Name',minwidth = 0, width = 130, anchor = 'center')
newstaffordertreeview.heading('Price',text = 'Price')
newstaffordertreeview.column('Price',minwidth = 0, width = 130, anchor = 'center')

newstaffordertreeview.delete(*newstaffordertreeview.get_children())
for data in order_data:
    newstaffordertreeview.insert('','end', values=data)


ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'black', foreground = 'white', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')


newstafforderspacer = Label(newstafforderframe, text = '')
newstafforderspacer.config(width = 5)
newstafforderspacer.grid(row = 0,column = 5)



#This is the treeview where all the items added to the order will be stored, they can be removed or saved to the file
conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM temporder')
temporder_data = cursor.fetchall()

stafftempordertreeview = ttk.Treeview(newstafforderframe, height = 15, columns = ('Item Number', 'Name', 'Price'),
                                  show = 'headings')

stafftempordertreeview.grid(row = 0, column = 6, columnspan = 4, rowspan = 2)

stafftempordertreeview.heading('Item Number',text = 'Item Number')
stafftempordertreeview.column('Item Number',minwidth = 0, width = 150, anchor = 'center')
stafftempordertreeview.heading('Name',text = 'Name')
stafftempordertreeview.column('Name',minwidth = 0, width = 130, anchor = 'center')
stafftempordertreeview.heading('Price',text = 'Price')
stafftempordertreeview.column('Price',minwidth = 0, width = 130, anchor = 'center')

stafftempordertreeview.delete(*stafftempordertreeview.get_children())
for data in temporder_data:
    stafftempordertreeview.insert('','end', values=data)



ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'white', foreground = 'black', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')


staffneworderbackbtn = Button(newstafforderframe, text = 'Back',command = backtostaffmenu, fg = 'black', bg = 'white')
staffneworderbackbtn.grid(row = 2, column = 0)

staffaddtempitembtn = Button(newstafforderframe, text = 'Add Item', command = addstafftempitem, fg = 'black', bg = 'white')
staffaddtempitembtn.grid(row = 2, column = 1, sticky = 'E')

staffneworderspacer = Label(newstafforderframe, text = '')
staffneworderspacer.grid(row = 2, column = 3, rowspan = 3)

staffremoveitembtn = Button(newstafforderframe, text = 'Remove Item',command = removestaffitem, fg = 'black', bg = 'white')
staffremoveitembtn.grid(row = 2, column = 6)

staffadditembtn = Button(newstafforderframe, text = 'Add Order', command = addnewstafforder, fg = 'black', bg = 'white')
staffadditembtn.grid(row=7, column = 1)

staffneworderspacer2 = Label(newstafforderframe, text = '')
staffneworderspacer2.grid(row = 3, column = 0)

stafforderfirstnamelabel = Label(newstafforderframe, text = 'Firstname: ', fg = 'black', bg = 'white')
stafforderfirstnamelabel.grid(row = 4, column = 0)

stafforderfirstname = StringVar()
stafforderfirstnameentry = Entry(newstafforderframe, textvariable = stafforderfirstname, fg = 'black', bg = 'white')
stafforderfirstnameentry.grid(row = 4, column = 1)

staffordersurnamelabel = Label(newstafforderframe, text = 'Surname: ', fg = 'black', bg = 'white')
staffordersurnamelabel.grid(row = 5, column = 0)

staffordersurname = StringVar()
staffordersurnameentry = Entry(newstafforderframe, textvariable = staffordersurname, fg = 'black', bg = 'white')
staffordersurnameentry.grid(row = 5, column = 1)

stafforderdateofdeliverylabel = Label(newstafforderframe, text = 'Date of Delivery: ', fg = 'black', bg = 'white')
stafforderdateofdeliverylabel.grid(row = 6, column = 0)

stafforderdateofdelivery = StringVar()
stafforderdateofdeliveryentry = Entry(newstafforderframe, textvariable = stafforderdateofdelivery, fg = 'black', bg = 'white')
stafforderdateofdeliveryentry.grid(row = 6, column = 1)


#--------------Customer New Order Frame-----------

conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM menu')
order_data = cursor.fetchall()


newcustomerordertreeview = ttk.Treeview(newcustomerorderframe, height = 15, columns = ('Item Number', 'Name', 'Price'),
                                  show = 'headings')

newcustomerordertreeview.grid(row = 0, column = 0, columnspan = 4, rowspan = 2)

newcustomerordertreeview.heading('Item Number',text = 'Item Number')
newcustomerordertreeview.column('Item Number',minwidth = 0, width = 150, anchor = 'center')
newcustomerordertreeview.heading('Name',text = 'Name')
newcustomerordertreeview.column('Name',minwidth = 0, width = 130, anchor = 'center')
newcustomerordertreeview.heading('Price',text = 'Price')
newcustomerordertreeview.column('Price',minwidth = 0, width = 130, anchor = 'center')

newcustomerordertreeview.delete(*newcustomerordertreeview.get_children())
for data in order_data:
    newcustomerordertreeview.insert('','end', values=data)


ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'black', foreground = 'white', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')


newcustomerorderspacer = Label(newcustomerorderframe, text = '')
newcustomerorderspacer.config(width = 5)
newcustomerorderspacer.grid(row = 0,column = 5)



#This is the treeview where all the items added to the order will be stored, they can be removed or saved to the file
conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM temporder')
temporder_data = cursor.fetchall()

customertempordertreeview = ttk.Treeview(newcustomerorderframe, height = 15, columns = ('Item Number', 'Name', 'Price'),
                                  show = 'headings')

customertempordertreeview.grid(row = 0, column = 6, columnspan = 4, rowspan = 2)

customertempordertreeview.heading('Item Number',text = 'Item Number')
customertempordertreeview.column('Item Number',minwidth = 0, width = 150, anchor = 'center')
customertempordertreeview.heading('Name',text = 'Name')
customertempordertreeview.column('Name',minwidth = 0, width = 130, anchor = 'center')
customertempordertreeview.heading('Price',text = 'Price')
customertempordertreeview.column('Price',minwidth = 0, width = 130, anchor = 'center')

customertempordertreeview.delete(*customertempordertreeview.get_children())
for data in temporder_data:
    customertempordertreeview.insert('','end', values=data)



ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'white', foreground = 'black', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')


customerneworderbackbtn = Button(newcustomerorderframe, text = 'Back',command = backtocustomermenu, fg = 'black', bg = 'white')
customerneworderbackbtn.grid(row = 2, column = 0)

customeraddtempitembtn = Button(newcustomerorderframe, text = 'Add Item', command = addcustomertempitem, fg = 'black', bg = 'white')
customeraddtempitembtn.grid(row = 2, column = 1, sticky = 'E')

customerneworderspacer = Label(newcustomerorderframe, text = '')
staffneworderspacer.grid(row = 2, column = 3, rowspan = 3)

customerremoveitembtn = Button(newcustomerorderframe, text = 'Remove Item',command = removecustomeritem, fg = 'black', bg = 'white')
customerremoveitembtn.grid(row = 2, column = 6)

customeradditembtn = Button(newcustomerorderframe, text = 'Add Order', command = addnewcustomerorder, fg = 'black', bg = 'white')
customeradditembtn.grid(row=7, column = 1)

customerneworderspacer2 = Label(newcustomerorderframe, text = '')
customerneworderspacer2.grid(row = 3, column = 0)

customerorderfirstnamelabel = Label(newcustomerorderframe, text = 'Firstname: ', fg = 'black', bg = 'white')
customerorderfirstnamelabel.grid(row = 4, column = 0)

customerorderfirstname = StringVar()
customerorderfirstnameentry = Entry(newcustomerorderframe, textvariable = customerorderfirstname, fg = 'black', bg = 'white')
customerorderfirstnameentry.grid(row = 4, column = 1)

customerordersurnamelabel = Label(newcustomerorderframe, text = 'Surname: ', fg = 'black', bg = 'white')
customerordersurnamelabel.grid(row = 5, column = 0)

customerordersurname = StringVar()
customerordersurnameentry = Entry(newcustomerorderframe, textvariable = customerordersurname, fg = 'black', bg = 'white')
customerordersurnameentry.grid(row = 5, column = 1)

customerorderdateofdeliverylabel = Label(newcustomerorderframe, text = 'Date of Delivery: ', fg = 'black', bg = 'white')
customerorderdateofdeliverylabel.grid(row = 6, column = 0)

customerorderdateofdelivery = StringVar()
customerorderdateofdeliveryentry = Entry(newcustomerorderframe, textvariable = customerorderdateofdelivery, fg = 'black', bg = 'white')
customerorderdateofdeliveryentry.grid(row = 6, column = 1)


#------------addnewmenuitemframe-----------

newitem_number = random.randint(1, 1000)

newitem_namelabel = Label(addnewmenuitemframe, text = 'New Item Name: ', fg = 'black', bg = 'white')
newitem_namelabel.grid(row = 0, column = 0)

newitemname = StringVar()
newitemnameentry = Entry(addnewmenuitemframe, textvariable = newitemname, fg = 'black', bg = 'white')
newitemnameentry.grid(row = 0, column = 1)

newitem_pricelabel = Label(addnewmenuitemframe, text = 'New Item Price: ', fg = 'black', bg = 'white')
newitem_pricelabel.grid(row = 1, column = 0)

newitemprice = StringVar()
newitempriceentry = Entry(addnewmenuitemframe, textvariable = newitemprice, fg = 'black', bg = 'white')
newitempriceentry.grid(row = 1, column = 1)

newmenuitemback_btn = Button(addnewmenuitemframe, text = 'Back', command = backtoownermenu, fg = 'black', bg = 'white')
newmenuitemback_btn.grid(row = 2, column = 0)

newmenuitemadd_btn = Button(addnewmenuitemframe, text = 'Add Item', command = addnewitem, fg = 'black', bg = 'white')
newmenuitemadd_btn.grid(row = 2, column = 1)

#-------------------Owner Dashboard frame--------------------------


dashboardbutton1 = Button(ownerdashboardframe, text = 'Dashboard', command = openownerdashboard, fg = 'black', bg = 'white')
dashboardbutton1.config(height = 10, width = 20)
dashboardbutton1.grid(row = 0, column = 0, rowspan = 3)

reviewsbutton1 = Button(ownerdashboardframe, text = 'Reviews',command = openownerreviews, fg = 'black',bg = 'white')
reviewsbutton1.config(height = 10, width = 20)
reviewsbutton1.grid(row = 0, column = 1, rowspan = 3)

Staffbutton1 = Button(ownerdashboardframe, text = 'Staff',command = openownerStaff, fg = 'black',bg = 'white')
Staffbutton1.config(height = 10, width = 20)
Staffbutton1.grid(row = 0, column = 2, rowspan = 3)

menubutton1 = Button(ownerdashboardframe, text = 'Menu',command = openownermenu, fg = 'black',bg='white')
menubutton1.config(height = 10, width = 20)
menubutton1.grid(row = 0, column = 3, rowspan = 3)

orderbutton1 = Button(ownerdashboardframe, text = 'Order',command = openownerorder, fg = 'black', bg = 'white')
orderbutton1.config(height = 10, width = 20)
orderbutton1.grid(row = 0, column = 4, rowspan = 3)

usernametodisplaylabel1 = Label(ownerdashboardframe, text = 'Username: ', fg = 'black',bg= 'white')
usernametodisplaylabel1.config(height = 1)
usernametodisplaylabel1.grid(row = 0, column = 5)

accounttypetodisplay1 = Label(ownerdashboardframe, text = 'Account Type: ',fg='black',bg='white')
accounttypetodisplay1.config(height = 3)
accounttypetodisplay1.grid(row = 1, column = 5)

logoutbutton1 = Button(ownerdashboardframe, text = 'Logout', command = backtologin, fg = 'black',bg = 'white',font = ('',13,'underline'), relief = 'flat')
logoutbutton1.config(height = 1, width = 10)
logoutbutton1.grid(row = 2, column = 5)

ownerdashboardlabel = Label(ownerdashboardframe, text = 'Dashboard', fg = 'black', bg = 'white', font = ('',13,'underline'))
ownerdashboardlabel.grid(row = 3, column = 0)






#--------Owner Review Frame-------

dashboardbutton2 = Button(ownerreviewframe, text = 'Dashboard', command = openownerdashboard, fg = 'black', bg = 'white')
dashboardbutton2.config(height = 10, width = 20)
dashboardbutton2.grid(row = 0, column = 0, rowspan = 3)

reviewsbutton2 = Button(ownerreviewframe, text = 'Reviews',command = openownerreviews, fg = 'black',bg = 'white')
reviewsbutton2.config(height = 10, width = 20)
reviewsbutton2.grid(row = 0, column = 1, rowspan = 3)

Staffbutton2 = Button(ownerreviewframe, text = 'Staff',command = openownerStaff, fg = 'black',bg = 'white')
Staffbutton2.config(height = 10, width = 20)
Staffbutton2.grid(row = 0, column = 2, rowspan = 3)

menubutton2 = Button(ownerreviewframe, text = 'Menu',command = openownermenu, fg = 'black',bg='white')
menubutton2.config(height = 10, width = 20)
menubutton2.grid(row = 0, column = 3, rowspan = 3)

orderbutton2 = Button(ownerreviewframe, text = 'Order',command = openownerorder, fg = 'black', bg = 'white')
orderbutton2.config(height = 10, width = 20)
orderbutton2.grid(row = 0, column = 4, rowspan = 3)

usernametodisplaylabel2 = Label(ownerreviewframe, text = 'Username: ', fg = 'black',bg= 'white')
usernametodisplaylabel2.config(height = 1)
usernametodisplaylabel2.grid(row = 0, column = 5)

accounttypetodisplay2 = Label(ownerreviewframe, text = 'Account Type: ',fg='black',bg='white')
accounttypetodisplay2.config(height = 3)
accounttypetodisplay2.grid(row = 1, column = 5)

logoutbutton2 = Button(ownerreviewframe, text = 'Logout', command = backtologin, fg = 'black',bg = 'white',font = ('',13,'underline'), relief = 'flat')
logoutbutton2.config(height = 1, width = 10)
logoutbutton2.grid(row = 2, column = 5)

ownerreviewlabel = Label(ownerreviewframe, text = 'Reviews', fg = 'black', bg = 'white', font = ('',13,'underline'))
ownerreviewlabel.grid(row = 3, column = 0)


conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM reviews')
review_data = cursor.fetchall()

ownerreviewtreeview = ttk.Treeview(ownerreviewframe, height = 15, columns = ('Name', 'Creation Date', 'Rating', 'Comment', 'ReviewID'),
                                  show = 'headings')

ownerreviewtreeview.grid(row = 4, column = 0, columnspan = 5)

ownerreviewtreeview.heading('Name',text = 'Name')
ownerreviewtreeview.column('Name',minwidth = 0, width = 150, anchor = 'center')
ownerreviewtreeview.heading('Creation Date',text = 'Creation Date')
ownerreviewtreeview.column('Creation Date',minwidth = 0, width = 180, anchor = 'center')
ownerreviewtreeview.heading('Rating',text = 'Rating')
ownerreviewtreeview.column('Rating',minwidth = 0, width = 130, anchor = 'center')
ownerreviewtreeview.heading('Comment',text = 'Comment')
ownerreviewtreeview.column('Comment',minwidth = 0, width = 150, anchor = 'center')
ownerreviewtreeview.heading('ReviewID',text = 'ReviewID')
ownerreviewtreeview.column('ReviewID',minwidth = 0, width = 150, anchor = 'center')

for data in review_data:
    ownerreviewtreeview.insert('','end', values=data)


ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'black', foreground = 'white', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')

#--------Owner Staff Frame------

dashboardbutton3 = Button(ownerstaffframe, text = 'Dashboard', command = openownerdashboard, fg = 'black', bg = 'white')
dashboardbutton3.config(height = 10, width = 20)
dashboardbutton3.grid(row = 0, column = 0, rowspan = 3)

reviewsbutton3 = Button(ownerstaffframe, text = 'Reviews',command = openownerreviews, fg = 'black',bg = 'white')
reviewsbutton3.config(height = 10, width = 20)
reviewsbutton3.grid(row = 0, column = 1, rowspan = 3)

Staffbutton3 = Button(ownerstaffframe, text = 'Staff',command = openownerStaff, fg = 'black',bg = 'white')
Staffbutton3.config(height = 10, width = 20)
Staffbutton3.grid(row = 0, column = 2, rowspan = 3)

menubutton3 = Button(ownerstaffframe, text = 'Menu',command = openownermenu, fg = 'black',bg='white')
menubutton3.config(height = 10, width = 20)
menubutton3.grid(row = 0, column = 3, rowspan = 3)

orderbutton3 = Button(ownerstaffframe, text = 'Order',command = openownerorder, fg = 'black', bg = 'white')
orderbutton3.config(height = 10, width = 20)
orderbutton3.grid(row = 0, column = 4, rowspan = 3)

usernametodisplaylabel3 = Label(ownerstaffframe, text = 'Username: ', fg = 'black',bg= 'white')
usernametodisplaylabel3.config(height = 1)
usernametodisplaylabel3.grid(row = 0, column = 5)

accounttypetodisplay3 = Label(ownerstaffframe, text = 'Account Type: ',fg='black',bg='white')
accounttypetodisplay3.config(height = 3)
accounttypetodisplay3.grid(row = 1, column = 5)

logoutbutton3 = Button(ownerstaffframe, text = 'Logout', command = backtologin, fg = 'black',bg = 'white',font = ('',13,'underline'), relief = 'flat')
logoutbutton3.config(height = 1, width = 10)
logoutbutton3.grid(row = 2, column = 5)

ownerstafflabel = Label(ownerstaffframe, text = 'Staff', fg = 'black', bg = 'white', font = ('',13,'underline'))
ownerstafflabel.grid(row = 3, column = 0)


conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM Staff')
staff_data = cursor.fetchall()


ownerstafftreeview = ttk.Treeview(ownerstaffframe, height = 15, columns = ('Name', 'DOB', 'Starting Date', 'userID'),
                                  show = 'headings')

ownerstafftreeview.grid(row = 4, column = 0, columnspan = 4)

ownerstafftreeview.heading('Name',text = 'Name')
ownerstafftreeview.column('Name',minwidth = 0, width = 150, anchor = 'center')
ownerstafftreeview.heading('DOB',text = 'DOB')
ownerstafftreeview.column('DOB',minwidth = 0, width = 130, anchor = 'center')
ownerstafftreeview.heading('Starting Date',text = 'Starting Date')
ownerstafftreeview.column('Starting Date',minwidth = 0, width = 130, anchor = 'center')
ownerstafftreeview.heading('userID', text = 'userID')
ownerstafftreeview.column('userID',minwidth = 0, width = 130, anchor = 'center')


ownerstafftreeview.delete(*ownerstafftreeview.get_children())
for data in staff_data:
    ownerstafftreeview.insert('','end', values=data)


ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'black', foreground = 'white', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')


edit_button = Button(ownerstaffframe, text="Edit", command=edit_data, fg = 'black', bg = 'white')
edit_button.config(height = 3, width = 10)
edit_button.grid(row=4, column=4, sticky = 'N')

addstaffmember_btn = Button(ownerstaffframe, text = 'Add Staff Member', command = opennewstaffmember, fg = 'black', bg = 'white')
addstaffmember_btn.config(height = 3, width = 20)
addstaffmember_btn.grid(row = 4, column = 4)

addstafflogin_btn = Button(ownerstaffframe, text = 'Add Staff Login', command = opennewstafflogin, fg = 'black', bg = 'white')
addstafflogin_btn.config(height = 3, width = 20)
addstafflogin_btn.grid(row = 4, column = 4, sticky = 'S')

deletestaffmember_btn = Button(ownerstaffframe, text = 'Remove Staff Member', command = deletestaffmember, fg = 'black', bg = 'white')
deletestaffmember_btn.config(height = 3, width = 16)
deletestaffmember_btn.grid(row = 5, column = 1)

deleteuserlogin_btn = Button(ownerstaffframe, text = 'Remove User Login', command = raiseuserlogin, fg ='black', bg = 'white')
deleteuserlogin_btn.config(height = 3, width = 15)
deleteuserlogin_btn.grid(row = 5, column = 2)

addnewadmin_btn = Button(ownerstaffframe, text = 'Add Admin', command = raisenewadmin, fg = 'black', bg = 'white')
addnewadmin_btn.config(height = 3, width = 10)
addnewadmin_btn.grid(row = 4, column = 5, sticky = 'N')

deladmin_btn = Button(ownerstaffframe, text = 'Delete Admin', command = raisedeladmin, fg = 'black', bg = 'white')
deladmin_btn.config(height = 3, width = 10)
deladmin_btn.grid(row = 4, column = 5, sticky = 'E')

#--------Owner Menu Frame------

dashboardbutton4 = Button(ownermenuframe, text = 'Dashboard', command = openownerdashboard, fg = 'black', bg = 'white')
dashboardbutton4.config(height = 10, width = 20)
dashboardbutton4.grid(row = 0, column = 0, rowspan = 3)

reviewsbutton4 = Button(ownermenuframe, text = 'Reviews',command = openownerreviews, fg = 'black',bg = 'white')
reviewsbutton4.config(height = 10, width = 20)
reviewsbutton4.grid(row = 0, column = 1, rowspan = 3)

Staffbutton4 = Button(ownermenuframe, text = 'Staff',command = openownerStaff, fg = 'black',bg = 'white')
Staffbutton4.config(height = 10, width = 20)
Staffbutton4.grid(row = 0, column = 2, rowspan = 3)

menubutton4 = Button(ownermenuframe, text = 'Menu',command = openownermenu, fg = 'black',bg='white')
menubutton4.config(height = 10, width = 20)
menubutton4.grid(row = 0, column = 3, rowspan = 3)

orderbutton4 = Button(ownermenuframe, text = 'Order',command = openownerorder, fg = 'black', bg = 'white')
orderbutton4.config(height = 10, width = 20)
orderbutton4.grid(row = 0, column = 4, rowspan = 3)

usernametodisplaylabel4 = Label(ownermenuframe, text = 'Username: ', fg = 'black',bg= 'white')
usernametodisplaylabel4.config(height = 1)
usernametodisplaylabel4.grid(row = 0, column = 5)

accounttypetodisplay4 = Label(ownermenuframe, text = 'Account Type: ',fg='black',bg='white')
accounttypetodisplay4.config(height = 3)
accounttypetodisplay4.grid(row = 1, column = 5)

logoutbutton4 = Button(ownermenuframe, text = 'Logout', command = backtologin, fg = 'black',bg = 'white',font = ('',13,'underline'), relief = 'flat')
logoutbutton4.config(height = 1, width = 10)
logoutbutton4.grid(row = 2, column = 5)

ownermenulabel = Label(ownermenuframe, text = 'Menu', fg = 'black', bg = 'white', font = ('',13,'underline'))
ownermenulabel.grid(row = 3, column = 0)




conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM menu')
menu_data = cursor.fetchall()


ownermenutreeview = ttk.Treeview(ownermenuframe, height = 15, columns = ('Item Number', 'Name', 'Price'),
                                  show = 'headings')

ownermenutreeview.grid(row = 4, column = 0, columnspan = 4, rowspan = 2)

ownermenutreeview.heading('Item Number',text = 'Item Number')
ownermenutreeview.column('Item Number',minwidth = 0, width = 150, anchor = 'center')
ownermenutreeview.heading('Name',text = 'Name')
ownermenutreeview.column('Name',minwidth = 0, width = 130, anchor = 'center')
ownermenutreeview.heading('Price',text = 'Price')
ownermenutreeview.column('Price',minwidth = 0, width = 130, anchor = 'center')

ownermenutreeview.delete(*ownermenutreeview.get_children())
for data in menu_data:
    ownermenutreeview.insert('','end', values=data)


ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'black', foreground = 'white', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')

editmenu_button = Button(ownermenuframe, text="Edit", command=edit_ownermenu, fg = 'black', bg = 'white')
editmenu_button.config(height = 1, width = 10)
editmenu_button.grid(row=4, column=3)

additem_btn = Button(ownermenuframe, text = 'Add Item', command = raiseadditem, fg = 'black', bg = 'white')
additem_btn.config(height = 1, width = 10)
additem_btn.grid(row = 4, column = 3, sticky = 'S')

delitem_btn = Button(ownermenuframe, text = 'Remove Item', command = removemenuitem, fg = 'black', bg = 'white')
delitem_btn.config(height = 1, width = 10)
delitem_btn.grid(row = 5, column = 3)

addorder_button = Button(ownermenuframe, text = 'Add New Order', command = addorder, fg = 'black', bg = 'white')
addorder_button.config(height = 1, width = 10)
addorder_button.grid(row = 5, column = 3, sticky = 'S')

#--------Owner Order frame-------

dashboardbutton5 = Button(ownerorderframe, text = 'Dashboard', command = openownerdashboard, fg = 'black', bg = 'white')
dashboardbutton5.config(height = 10, width = 20)
dashboardbutton5.grid(row = 0, column = 0, rowspan = 3)

reviewsbutton5 = Button(ownerorderframe, text = 'Reviews',command = openownerreviews, fg = 'black',bg = 'white')
reviewsbutton5.config(height = 10, width = 20)
reviewsbutton5.grid(row = 0, column = 1, rowspan = 3)

Staffbutton5 = Button(ownerorderframe, text = 'Staff',command = openownerStaff, fg = 'black',bg = 'white')
Staffbutton5.config(height = 10, width = 20)
Staffbutton5.grid(row = 0, column = 2, rowspan = 3)

menubutton5 = Button(ownerorderframe, text = 'Menu',command = openownermenu, fg = 'black',bg='white')
menubutton5.config(height = 10, width = 20)
menubutton5.grid(row = 0, column = 3, rowspan = 3)

orderbutton5 = Button(ownerorderframe, text = 'Order',command = openownerorder, fg = 'black', bg = 'white')
orderbutton5.config(height = 10, width = 20)
orderbutton5.grid(row = 0, column = 4, rowspan = 3)

usernametodisplaylabel5 = Label(ownerorderframe, text = 'Username: ', fg = 'black',bg= 'white')
usernametodisplaylabel5.config(height = 1)
usernametodisplaylabel5.grid(row = 0, column = 5)

accounttypetodisplay5 = Label(ownerorderframe, text = 'Account Type: ',fg='black',bg='white')
accounttypetodisplay5.config(height = 3)
accounttypetodisplay5.grid(row = 1, column = 5)

logoutbutton5 = Button(ownerorderframe, text = 'Logout', command = backtologin, fg = 'black',bg = 'white',font = ('',13,'underline'), relief = 'flat')
logoutbutton5.config(height = 1, width = 10)
logoutbutton5.grid(row = 2, column = 5)

ownerorderlabel = Label(ownerorderframe, text = 'Order', fg = 'black', bg = 'white', font = ('',13,'underline'))
ownerorderlabel.grid(row = 3, column = 0)


conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM orders')
order_data = cursor.fetchall()

ownerordertreeview = ttk.Treeview(ownerorderframe, height = 15, columns = ('Name', 'Date Of Delivery', 'Item Numbers', 'Total Price', 'OrderID'),
                                  show = 'headings')

ownerordertreeview.grid(row = 4, column = 0, columnspan = 5)

ownerordertreeview.heading('Name',text = 'Name')
ownerordertreeview.column('Name',minwidth = 0, width = 150, anchor = 'center')
ownerordertreeview.heading('Date Of Delivery',text = 'Date of Delivery')
ownerordertreeview.column('Date Of Delivery',minwidth = 0, width = 180, anchor = 'center')
ownerordertreeview.heading('Item Numbers',text = 'Item Numbers')
ownerordertreeview.column('Item Numbers',minwidth = 0, width = 130, anchor = 'center')
ownerordertreeview.heading('Total Price',text = 'Total Price')
ownerordertreeview.column('Total Price',minwidth = 0, width = 150, anchor = 'center')
ownerordertreeview.heading('OrderID',text = 'OrderID')
ownerordertreeview.column('OrderID',minwidth = 0, width = 150, anchor = 'center')

for data in order_data:
    ownerordertreeview.insert('','end', values=data)


ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'black', foreground = 'white', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')


#-------------------Staff Dashboard Frame------------------------------

dashboardbutton1 = Button(staffdashboardframe, text = 'Dashboard', command = openstaffdashboard, fg = 'black', bg = 'white')
dashboardbutton1.config(height = 10, width = 20)
dashboardbutton1.grid(row = 0, column = 0, rowspan = 3)

reviewsbutton1 = Button(staffdashboardframe, text = 'Reviews',command = openstaffreviews, fg = 'black',bg = 'white')
reviewsbutton1.config(height = 10, width = 20)
reviewsbutton1.grid(row = 0, column = 1, rowspan = 3)

Staffbutton1 = Button(staffdashboardframe, text = 'Staff',command = openstaffStaff, fg = 'black',bg = 'white')
Staffbutton1.config(height = 10, width = 20)
Staffbutton1.grid(row = 0, column = 2, rowspan = 3)

menubutton1 = Button(staffdashboardframe, text = 'Menu',command = openstaffmenu, fg = 'black',bg='white')
menubutton1.config(height = 10, width = 20)
menubutton1.grid(row = 0, column = 3, rowspan = 3)

orderbutton1 = Button(staffdashboardframe, text = 'Order',command = openstafforder, fg = 'black', bg = 'white')
orderbutton1.config(height = 10, width = 20)
orderbutton1.grid(row = 0, column = 4, rowspan = 3)

usernametodisplay1 = Label(staffdashboardframe, text = 'Username: ', fg = 'black',bg= 'white')
usernametodisplay1.config(height = 1, width = 10)
usernametodisplay1.grid(row = 0, column = 5)

accounttypetodisplay1 = Label(staffdashboardframe, text = 'Account Type: ',fg='black',bg='white')
accounttypetodisplay1.config(height = 3, width = 10)
accounttypetodisplay1.grid(row = 1, column = 5)

logoutbutton1 = Button(staffdashboardframe, text = 'Logout', command = backtologin, fg = 'black',bg = 'white',font = ('',13,'underline'), relief = 'flat')
logoutbutton1.config(height = 1, width = 10)
logoutbutton1.grid(row = 2, column = 5)

staffdashboardlabel = Label(staffdashboardframe, text = 'Dashboard', fg = 'black', bg = 'white', font = ('',13,'underline'))
staffdashboardlabel.grid(row = 3, column = 0)

#-----Staff Review Frame------

dashboardbutton2 = Button(staffreviewframe, text = 'Dashboard', command = openstaffdashboard, fg = 'black', bg = 'white')
dashboardbutton2.config(height = 10, width = 20)
dashboardbutton2.grid(row = 0, column = 0, rowspan = 3)

reviewsbutton2 = Button(staffreviewframe, text = 'Reviews',command = openstaffreviews, fg = 'black',bg = 'white')
reviewsbutton2.config(height = 10, width = 20)
reviewsbutton2.grid(row = 0, column = 1, rowspan = 3)

Staffbutton2 = Button(staffreviewframe, text = 'Staff',command = openstaffStaff, fg = 'black',bg = 'white')
Staffbutton2.config(height = 10, width = 20)
Staffbutton2.grid(row = 0, column = 2, rowspan = 3)

menubutton2 = Button(staffreviewframe, text = 'Menu',command = openstaffmenu, fg = 'black',bg='white')
menubutton2.config(height = 10, width = 20)
menubutton2.grid(row = 0, column = 3, rowspan = 3)

orderbutton2 = Button(staffreviewframe, text = 'Order',command = openstafforder, fg = 'black', bg = 'white')
orderbutton2.config(height = 10, width = 20)
orderbutton2.grid(row = 0, column = 4, rowspan = 3)

usernametodisplay2 = Label(staffreviewframe, text = 'Username: ', fg = 'black',bg= 'white')
usernametodisplay2.config(height = 1, width = 10)
usernametodisplay2.grid(row = 0, column = 5)

accounttypetodisplay2 = Label(staffreviewframe, text = 'Account Type: ',fg='black',bg='white')
accounttypetodisplay2.config(height = 3, width = 10)
accounttypetodisplay2.grid(row = 1, column = 5)

logoutbutton2 = Button(staffreviewframe, text = 'Logout', command = backtologin, fg = 'black',bg = 'white',font = ('',13,'underline'), relief = 'flat')
logoutbutton2.config(height = 1, width = 10)
logoutbutton2.grid(row = 2, column = 5)

staffreviewlabel = Label(staffreviewframe, text = 'Reviews', fg = 'black', bg = 'white', font = ('',13,'underline'))
staffreviewlabel.grid(row = 3, column = 0)



conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM reviews')
review_data = cursor.fetchall()

staffreviewtreeview = ttk.Treeview(staffreviewframe, height = 15, columns = ('Name', 'Creation Date', 'Rating', 'Comment', 'ReviewID'),
                                  show = 'headings')

staffreviewtreeview.grid(row = 4, column = 0, columnspan = 5)

staffreviewtreeview.heading('Name',text = 'Name')
staffreviewtreeview.column('Name',minwidth = 0, width = 150, anchor = 'center')
staffreviewtreeview.heading('Creation Date',text = 'Creation Date')
staffreviewtreeview.column('Creation Date',minwidth = 0, width = 180, anchor = 'center')
staffreviewtreeview.heading('Rating',text = 'Rating')
staffreviewtreeview.column('Rating',minwidth = 0, width = 130, anchor = 'center')
staffreviewtreeview.heading('Comment',text = 'Comment')
staffreviewtreeview.column('Comment',minwidth = 0, width = 150, anchor = 'center')
staffreviewtreeview.heading('ReviewID',text = 'ReviewID')
staffreviewtreeview.column('ReviewID',minwidth = 0, width = 150, anchor = 'center')

for data in review_data:
    staffreviewtreeview.insert('','end', values=data)



ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'black', foreground = 'white', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')

#-----Staff Staff Frame------

dashboardbutton3 = Button(staffstaffframe, text = 'Dashboard', command = openstaffdashboard, fg = 'black', bg = 'white')
dashboardbutton3.config(height = 10, width = 20)
dashboardbutton3.grid(row = 0, column = 0, rowspan = 3)

reviewsbutton3 = Button(staffstaffframe, text = 'Reviews',command = openstaffreviews, fg = 'black',bg = 'white')
reviewsbutton3.config(height = 10, width = 20)
reviewsbutton3.grid(row = 0, column = 1, rowspan = 3)

Staffbutton3 = Button(staffstaffframe, text = 'Staff',command = openstaffStaff, fg = 'black',bg = 'white')
Staffbutton3.config(height = 10, width = 20)
Staffbutton3.grid(row = 0, column = 2, rowspan = 3)

menubutton3 = Button(staffstaffframe, text = 'Menu',command = openstaffmenu, fg = 'black',bg='white')
menubutton3.config(height = 10, width = 20)
menubutton3.grid(row = 0, column = 3, rowspan = 3)

orderbutton3 = Button(staffstaffframe, text = 'Order',command = openstafforder, fg = 'black', bg = 'white')
orderbutton3.config(height = 10, width = 20)
orderbutton3.grid(row = 0, column = 4, rowspan = 3)

usernametodisplay3 = Label(staffstaffframe, text = 'Username: ', fg = 'black',bg= 'white')
usernametodisplay3.config(height = 1, width = 10)
usernametodisplay3.grid(row = 0, column = 5)

accounttypetodisplay3 = Label(staffstaffframe, text = 'Account Type: ',fg='black',bg='white')
accounttypetodisplay3.config(height = 3, width = 10)
accounttypetodisplay3.grid(row = 1, column = 5)

logoutbutton3 = Button(staffstaffframe, text = 'Logout', command = backtologin, fg = 'black',bg = 'white',font = ('',13,'underline'), relief = 'flat')
logoutbutton3.config(height = 1, width = 10)
logoutbutton3.grid(row = 2, column = 5)

staffstafflabel = Label(staffstaffframe, text = 'Staff', fg = 'black', bg = 'white', font = ('',13,'underline'))
staffstafflabel.grid(row = 3, column = 0)

conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM Staff')
staff_data = cursor.fetchall()

staffstafftreeview = ttk.Treeview(staffstaffframe, height = 15, columns = ('Name', 'DOB', 'Starting Date', 'userID'),
                                  show = 'headings')

staffstafftreeview.grid(row = 4, column = 0, columnspan = 4)

staffstafftreeview.heading('Name',text = 'Name')
staffstafftreeview.column('Name',minwidth = 0, width = 150, anchor = 'center')
staffstafftreeview.heading('DOB',text = 'DOB')
staffstafftreeview.column('DOB',minwidth = 0, width = 130, anchor = 'center')
staffstafftreeview.heading('Starting Date',text = 'Starting Date')
staffstafftreeview.column('Starting Date',minwidth = 0, width = 130, anchor = 'center')
staffstafftreeview.heading('userID', text = 'userID')
staffstafftreeview.column('userID',minwidth = 0, width = 130, anchor = 'center')

for data in staff_data:
    staffstafftreeview.insert('','end', values=data)


ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'black', foreground = 'white', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')

#-----Staff Menu Frame------

dashboardbutton4 = Button(staffmenuframe, text = 'Dashboard', command = openstaffdashboard, fg = 'black', bg = 'white')
dashboardbutton4.config(height = 10, width = 20)
dashboardbutton4.grid(row = 0, column = 0, rowspan = 3)

reviewsbutton4 = Button(staffmenuframe, text = 'Reviews',command = openstaffreviews, fg = 'black',bg = 'white')
reviewsbutton4.config(height = 10, width = 20)
reviewsbutton4.grid(row = 0, column = 1, rowspan = 3)

Staffbutton4 = Button(staffmenuframe, text = 'Staff',command = openstaffStaff, fg = 'black',bg = 'white')
Staffbutton4.config(height = 10, width = 20)
Staffbutton4.grid(row = 0, column = 2, rowspan = 3)

menubutton4 = Button(staffmenuframe, text = 'Menu',command = openstaffmenu, fg = 'black',bg='white')
menubutton4.config(height = 10, width = 20)
menubutton4.grid(row = 0, column = 3, rowspan = 3)

orderbutton4 = Button(staffmenuframe, text = 'Order',command = openstafforder, fg = 'black', bg = 'white')
orderbutton4.config(height = 10, width = 20)
orderbutton4.grid(row = 0, column = 4, rowspan = 3)

usernametodisplay4 = Label(staffmenuframe, text = 'Username: ', fg = 'black',bg= 'white')
usernametodisplay4.config(height = 1, width = 10)
usernametodisplay4.grid(row = 0, column = 5)

accounttypetodisplay4 = Label(staffmenuframe, text = 'Account Type: ',fg='black',bg='white')
accounttypetodisplay4.config(height = 3, width = 10)
accounttypetodisplay4.grid(row = 1, column = 5)

logoutbutton4 = Button(staffmenuframe, text = 'Logout', command = backtologin, fg = 'black',bg = 'white',font = ('',13,'underline'), relief = 'flat')
logoutbutton4.config(height = 1, width = 10)
logoutbutton4.grid(row = 2, column = 5)

staffmenulabel = Label(staffmenuframe, text = 'Menu', fg = 'black', bg = 'white', font = ('',13,'underline'))
staffmenulabel.grid(row = 3, column = 0)

conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM menu')
menu_data = cursor.fetchall()


staffmenutreeview = ttk.Treeview(staffmenuframe, height = 15, columns = ('Item Number', 'Name', 'Price'),
                                  show = 'headings')

staffmenutreeview.grid(row = 4, column = 0, columnspan = 4, rowspan = 2)

staffmenutreeview.heading('Item Number',text = 'Item Number')
staffmenutreeview.column('Item Number',minwidth = 0, width = 150, anchor = 'center')
staffmenutreeview.heading('Name',text = 'Name')
staffmenutreeview.column('Name',minwidth = 0, width = 130, anchor = 'center')
staffmenutreeview.heading('Price',text = 'Price')
staffmenutreeview.column('Price',minwidth = 0, width = 130, anchor = 'center')

staffmenutreeview.delete(*staffmenutreeview.get_children())
for data in menu_data:
    staffmenutreeview.insert('','end', values=data)

ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'black', foreground = 'white', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')

editmenu_btn = Button(staffmenuframe, text = 'Edit Item', command = edit_staffmenu, fg = 'black', bg = 'white')
editmenu_btn.config(height = 1, width = 10)
editmenu_btn.grid(row = 4, column = 3)


addorder_button = Button(staffmenuframe, text = 'Add New Order', command = addstafforder, fg = 'black', bg = 'white')
addorder_button.config(height = 1, width = 10)
addorder_button.grid(row = 5, column = 3)

#-----Staff order Frame------

dashboardbutton5 = Button(stafforderframe, text = 'Dashboard', command = openstaffdashboard, fg = 'black', bg = 'white')
dashboardbutton5.config(height = 10, width = 20)
dashboardbutton5.grid(row = 0, column = 0, rowspan = 3)

reviewsbutton5 = Button(stafforderframe, text = 'Reviews',command = openstaffreviews, fg = 'black',bg = 'white')
reviewsbutton5.config(height = 10, width = 20)
reviewsbutton5.grid(row = 0, column = 1, rowspan = 3)

Staffbutton5 = Button(stafforderframe, text = 'Staff',command = openstaffStaff, fg = 'black',bg = 'white')
Staffbutton5.config(height = 10, width = 20)
Staffbutton5.grid(row = 0, column = 2, rowspan = 3)

menubutton5 = Button(stafforderframe, text = 'Menu',command = openstaffmenu, fg = 'black',bg='white')
menubutton5.config(height = 10, width = 20)
menubutton5.grid(row = 0, column = 3, rowspan = 3)

orderbutton5 = Button(stafforderframe, text = 'Order',command = openstafforder, fg = 'black', bg = 'white')
orderbutton5.config(height = 10, width = 20)
orderbutton5.grid(row = 0, column = 4, rowspan = 3)

usernametodisplay5 = Label(stafforderframe, text = 'Username: ', fg = 'black',bg= 'white')
usernametodisplay5.config(height = 1, width = 10)
usernametodisplay5.grid(row = 0, column = 5)

accounttypetodisplay5 = Label(stafforderframe, text = 'Account Type: ',fg='black',bg='white')
accounttypetodisplay5.config(height = 3, width = 10)
accounttypetodisplay5.grid(row = 1, column = 5)

logoutbutton5 = Button(stafforderframe, text = 'Logout', command = backtologin, fg = 'black',bg = 'white',font = ('',13,'underline'), relief = 'flat')
logoutbutton5.config(height = 1, width = 10)
logoutbutton5.grid(row = 2, column = 5)

stafforderlabel = Label(stafforderframe, text = 'Order', fg = 'black', bg = 'white', font = ('',13,'underline'))
stafforderlabel.grid(row = 3, column = 0)

conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM orders')
order_data = cursor.fetchall()

staffordertreeview = ttk.Treeview(stafforderframe, height = 15, columns = ('Name', 'Date Of Delivery', 'Item Numbers', 'Total Price', 'OrderID'),
                                  show = 'headings')

staffordertreeview.grid(row = 4, column = 0, columnspan = 5)

staffordertreeview.heading('Name',text = 'Name')
staffordertreeview.column('Name',minwidth = 0, width = 150, anchor = 'center')
staffordertreeview.heading('Date Of Delivery',text = 'Date of Delivery')
staffordertreeview.column('Date Of Delivery',minwidth = 0, width = 180, anchor = 'center')
staffordertreeview.heading('Item Numbers',text = 'Item Numbers')
staffordertreeview.column('Item Numbers',minwidth = 0, width = 130, anchor = 'center')
staffordertreeview.heading('Total Price',text = 'Total Price')
staffordertreeview.column('Total Price',minwidth = 0, width = 150, anchor = 'center')
staffordertreeview.heading('OrderID',text = 'OrderID')
staffordertreeview.column('OrderID',minwidth = 0, width = 150, anchor = 'center')

for data in order_data:
    staffordertreeview.insert('','end', values=data)


#-------------------Customer Dashboard frame------------------------------

dashboardbutton1 = Button(customerdashboardframe, text = 'Dashboard', command = opencustomerdashboard, fg = 'black', bg = 'white')
dashboardbutton1.config(height = 10, width = 20)
dashboardbutton1.grid(row = 0, column = 0, rowspan = 3)

reviewsbutton1 = Button(customerdashboardframe, text = 'Reviews',command = opencustomerreviews, fg = 'black',bg = 'white')
reviewsbutton1.config(height = 10, width = 20)
reviewsbutton1.grid(row = 0, column = 1, rowspan = 3)

Staffbutton1 = Button(customerdashboardframe, text = 'Staff',command = opencustomerStaff, fg = 'black',bg = 'white')
Staffbutton1.config(height = 10, width = 20)
Staffbutton1.grid(row = 0, column = 2, rowspan = 3)

menubutton1 = Button(customerdashboardframe, text = 'Menu',command = opencustomermenu, fg = 'black',bg='white')
menubutton1.config(height = 10, width = 20)
menubutton1.grid(row = 0, column = 3, rowspan = 3)

orderbutton1 = Button(customerdashboardframe, text = 'Order',command = opencustomerorder, fg = 'black', bg = 'white')
orderbutton1.config(height = 10, width = 20)
orderbutton1.grid(row = 0, column = 4, rowspan = 3)

usernametodisplay1 = Label(customerdashboardframe, text = 'Username: ', fg = 'black',bg= 'white')
usernametodisplay1.config(height = 1, width = 10)
usernametodisplay1.grid(row = 0, column = 5)

accounttypetodisplay1 = Label(customerdashboardframe, text = 'Account Type: ',fg='black',bg='white')
accounttypetodisplay1.config(height = 3, width = 10)
accounttypetodisplay1.grid(row = 1, column = 5)

logoutbutton1 = Button(customerdashboardframe, text = 'Logout', command = backtologin, fg = 'black',bg = 'white',font = ('',13,'underline'), relief = 'flat')
logoutbutton1.config(height = 1, width = 10)
logoutbutton1.grid(row = 2, column = 5)

customerdashboardlabel = Label(customerdashboardframe, text = 'Dashboard', fg = 'black', bg = 'white', font = ('',13,'underline'))
customerdashboardlabel.grid(row = 3, column = 0)


#---Customer Review Frame-----

dashboardbutton2 = Button(customerreviewframe, text = 'Dashboard', command = opencustomerdashboard, fg = 'black', bg = 'white')
dashboardbutton2.config(height = 10, width = 20)
dashboardbutton2.grid(row = 0, column = 0, rowspan = 3)

reviewsbutton2 = Button(customerreviewframe, text = 'Review',command = opencustomerreviews, fg = 'black',bg = 'white')
reviewsbutton2.config(height = 10, width = 20)
reviewsbutton2.grid(row = 0, column = 1, rowspan = 3)

Staffbutton2 = Button(customerreviewframe, text = 'Staff',command = opencustomerStaff, fg = 'black',bg = 'white')
Staffbutton2.config(height = 10, width = 20)
Staffbutton2.grid(row = 0, column = 2, rowspan = 3)

menubutton2 = Button(customerreviewframe, text = 'Menu',command = opencustomermenu, fg = 'black',bg='white')
menubutton2.config(height = 10, width = 20)
menubutton2.grid(row = 0, column = 3, rowspan = 3)

orderbutton2 = Button(customerreviewframe, text = 'Order',command = opencustomerorder, fg = 'black', bg = 'white')
orderbutton2.config(height = 10, width = 20)
orderbutton2.grid(row = 0, column = 4, rowspan = 3)

usernametodisplay2 = Label(customerreviewframe, text = 'Username: ', fg = 'black',bg= 'white')
usernametodisplay2.config(height = 1, width = 10)
usernametodisplay2.grid(row = 0, column = 5)

accounttypetodisplay2 = Label(customerreviewframe, text = 'Account Type: ',fg='black',bg='white')
accounttypetodisplay2.config(height = 3, width = 10)
accounttypetodisplay2.grid(row = 1, column = 5)

logoutbutton2 = Button(customerreviewframe, text = 'Logout', command = backtologin, fg = 'black',bg = 'white',font = ('',13,'underline'), relief = 'flat')
logoutbutton2.config(height = 1, width = 10)
logoutbutton2.grid(row = 2, column = 5)

customerreviewlabel = Label(customerreviewframe, text = 'Review', fg = 'black', bg = 'white', font = ('',13,'underline'))
customerreviewlabel.grid(row = 3, column = 0)


conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM reviews')
review_data = cursor.fetchall()

customerreviewtreeview = ttk.Treeview(customerreviewframe, height = 15, columns = ('Name', 'Creation Date', 'Rating', 'Comment', 'ReviewID'),
                                  show = 'headings')

customerreviewtreeview.grid(row = 4, column = 0, columnspan = 5, rowspan = 3)

customerreviewtreeview.heading('Name',text = 'Name')
customerreviewtreeview.column('Name',minwidth = 0, width = 150, anchor = 'center')
customerreviewtreeview.heading('Creation Date',text = 'Creation Date')
customerreviewtreeview.column('Creation Date',minwidth = 0, width = 180, anchor = 'center')
customerreviewtreeview.heading('Rating',text = 'Rating')
customerreviewtreeview.column('Rating',minwidth = 0, width = 130, anchor = 'center')
customerreviewtreeview.heading('Comment',text = 'Comment')
customerreviewtreeview.column('Comment',minwidth = 0, width = 150, anchor = 'center')
customerreviewtreeview.heading('ReviewID',text = 'ReviewID')
customerreviewtreeview.column('ReviewID',minwidth = 0, width = 150, anchor = 'center')

for data in review_data:
    customerreviewtreeview.insert('','end', values=data)

ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'black', foreground = 'white', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')


reviewinformationlabel = Label(customerreviewframe, text = 'On the left are all the current reviews.', fg = 'black', bg = 'white')
reviewinformationlabel.config(height = 2)
reviewinformationlabel.grid(row = 4, column = 5, columnspan = 3)

                       
createreviewbutton = Button(customerreviewframe, text = 'Create New Review', command = raisenewreviewframe, fg = 'black', bg = 'white')
createreviewbutton.config(height = 1, width = 15)
createreviewbutton.grid(row = 5, column = 5)

#-----------------Customer Staff Frame-----

dashboardbutton3 = Button(customerstaffframe, text = 'Dashboard', command = opencustomerdashboard, fg = 'black', bg = 'white')
dashboardbutton3.config(height = 10, width = 20)
dashboardbutton3.grid(row = 0, column = 0, rowspan = 3)

reviewsbutton3 = Button(customerstaffframe, text = 'Review',command = opencustomerreviews, fg = 'black',bg = 'white')
reviewsbutton3.config(height = 10, width = 20)
reviewsbutton3.grid(row = 0, column = 1, rowspan = 3)

Staffbutton3 = Button(customerstaffframe, text = 'Staff',command = opencustomerStaff, fg = 'black',bg = 'white')
Staffbutton3.config(height = 10, width = 20)
Staffbutton3.grid(row = 0, column = 2, rowspan = 3)

menubutton3 = Button(customerstaffframe, text = 'Menu',command = opencustomermenu, fg = 'black',bg='white')
menubutton3.config(height = 10, width = 20)
menubutton3.grid(row = 0, column = 3, rowspan = 3)

orderbutton3 = Button(customerstaffframe, text = 'Order',command = opencustomerorder, fg = 'black', bg = 'white')
orderbutton3.config(height = 10, width = 20)
orderbutton3.grid(row = 0, column = 4, rowspan = 3)

usernametodisplay3 = Label(customerstaffframe, text = 'Username: ', fg = 'black',bg= 'white')
usernametodisplay3.config(height = 1, width = 10)
usernametodisplay3.grid(row = 0, column = 5)

accounttypetodisplay3 = Label(customerstaffframe, text = 'Account Type: ',fg='black',bg='white')
accounttypetodisplay3.config(height = 3, width = 10)
accounttypetodisplay3.grid(row = 1, column = 5)

logoutbutton3 = Button(customerstaffframe, text = 'Logout', command = backtologin, fg = 'black',bg = 'white',font = ('',13,'underline'), relief = 'flat')
logoutbutton3.config(height = 1, width = 10)
logoutbutton3.grid(row = 2, column = 5)

customerstafflabel = Label(customerstaffframe, text = 'Staff', fg = 'black', bg = 'white', font = ('',13,'underline'))
customerstafflabel.grid(row = 3, column = 0)


conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM Staff')
staff_data = cursor.fetchall()

customerstafftreeview = ttk.Treeview(customerstaffframe, height = 15, columns = ('Name', 'DOB', 'Starting Date', 'userID'),
                                  show = 'headings')

customerstafftreeview.grid(row = 4, column = 0, columnspan = 4)

customerstafftreeview.heading('Name',text = 'Name')
customerstafftreeview.column('Name',minwidth = 0, width = 150, anchor = 'center')
customerstafftreeview.heading('DOB',text = 'DOB')
customerstafftreeview.column('DOB',minwidth = 0, width = 130, anchor = 'center')
customerstafftreeview.heading('Starting Date',text = 'Starting Date')
customerstafftreeview.column('Starting Date',minwidth = 0, width = 130, anchor = 'center')
customerstafftreeview.heading('userID', text = 'userID')
customerstafftreeview.column('userID',minwidth = 0, width = 130, anchor = 'center')

for data in staff_data:
    customerstafftreeview.insert('','end', values=data)



ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'black', foreground = 'white', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')

#---Customer Menu Frame------

dashboardbutton4 = Button(customermenuframe, text = 'Dashboard', command = opencustomerdashboard, fg = 'black', bg = 'white')
dashboardbutton4.config(height = 10, width = 20)
dashboardbutton4.grid(row = 0, column = 0, rowspan = 3)

reviewsbutton4 = Button(customermenuframe, text = 'Review',command = opencustomerreviews, fg = 'black',bg = 'white')
reviewsbutton4.config(height = 10, width = 20)
reviewsbutton4.grid(row = 0, column = 1, rowspan = 3)

Staffbutton4 = Button(customermenuframe, text = 'Staff',command = opencustomerStaff, fg = 'black',bg = 'white')
Staffbutton4.config(height = 10, width = 20)
Staffbutton4.grid(row = 0, column = 2, rowspan = 3)

menubutton4 = Button(customermenuframe, text = 'Menu',command = opencustomermenu, fg = 'black',bg='white')
menubutton4.config(height = 10, width = 20)
menubutton4.grid(row = 0, column = 3, rowspan = 3)

orderbutton4 = Button(customermenuframe, text = 'Order',command = opencustomerorder, fg = 'black', bg = 'white')
orderbutton4.config(height = 10, width = 20)
orderbutton4.grid(row = 0, column = 4, rowspan = 3)

usernametodisplay4 = Label(customermenuframe, text = 'Username: ', fg = 'black',bg= 'white')
usernametodisplay4.config(height = 1, width = 10)
usernametodisplay4.grid(row = 0, column = 5)

accounttypetodisplay4 = Label(customermenuframe, text = 'Account Type: ',fg='black',bg='white')
accounttypetodisplay4.config(height = 3, width = 10)
accounttypetodisplay4.grid(row = 1, column = 5)

logoutbutton4 = Button(customermenuframe, text = 'Logout', command = backtologin, fg = 'black',bg = 'white',font = ('',13,'underline'), relief = 'flat')
logoutbutton4.config(height = 1, width = 10)
logoutbutton4.grid(row = 2, column = 5)

customermenulabel = Label(customermenuframe, text = 'Menu', fg = 'black', bg = 'white', font = ('',13,'underline'))
customermenulabel.grid(row = 3, column = 0)



conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM menu')
menu_data = cursor.fetchall()


customermenutreeview = ttk.Treeview(customermenuframe, height = 15, columns = ('Item Number', 'Name', 'Price'),
                                  show = 'headings')

customermenutreeview.grid(row = 4, column = 0, columnspan = 4, rowspan = 2)

customermenutreeview.heading('Item Number',text = 'Item Number')
customermenutreeview.column('Item Number',minwidth = 0, width = 150, anchor = 'center')
customermenutreeview.heading('Name',text = 'Name')
customermenutreeview.column('Name',minwidth = 0, width = 130, anchor = 'center')
customermenutreeview.heading('Price',text = 'Price')
customermenutreeview.column('Price',minwidth = 0, width = 130, anchor = 'center')

customermenutreeview.delete(*customermenutreeview.get_children())
for data in menu_data:
    customermenutreeview.insert('','end', values=data)
    

ttk.Style().theme_use('default')
ttk.Style().configure('Treeview.heading',background = 'black', foreground = 'white', font = 'Verdana 10 bold')
ttk.Style().configure('Treeview.Column',font = 'Verdana 10')

addorder_button = Button(customermenuframe, text = 'Add New Order', command = addcustomerorder, fg = 'black', bg = 'white')
addorder_button.config(height = 1, width = 10)
addorder_button.grid(row = 4, column = 3)

#---Customer order Frame-----

dashboardbutton5 = Button(customerorderframe, text = 'Dashboard', command = opencustomerdashboard, fg = 'black', bg = 'white')
dashboardbutton5.config(height = 10, width = 20)
dashboardbutton5.grid(row = 0, column = 0, rowspan = 3)

reviewsbutton5 = Button(customerorderframe, text = 'Review',command = opencustomerreviews, fg = 'black',bg = 'white')
reviewsbutton5.config(height = 10, width = 20)
reviewsbutton5.grid(row = 0, column = 1, rowspan = 3)

Staffbutton5 = Button(customerorderframe, text = 'Staff',command = opencustomerStaff, fg = 'black',bg = 'white')
Staffbutton5.config(height = 10, width = 20)
Staffbutton5.grid(row = 0, column = 2, rowspan = 3)

menubutton5 = Button(customerorderframe, text = 'Menu',command = opencustomermenu, fg = 'black',bg='white')
menubutton5.config(height = 10, width = 20)
menubutton5.grid(row = 0, column = 3, rowspan = 3)

orderbutton5 = Button(customerorderframe, text = 'Order',command = opencustomerorder, fg = 'black', bg = 'white')
orderbutton5.config(height = 10, width = 20)
orderbutton5.grid(row = 0, column = 4, rowspan = 3)

usernametodisplay5 = Label(customerorderframe, text = 'Username: ', fg = 'black',bg= 'white')
usernametodisplay5.config(height = 1, width = 10)
usernametodisplay5.grid(row = 0, column = 5)

accounttypetodisplay5 = Label(customerorderframe, text = 'Account Type: ',fg='black',bg='white')
accounttypetodisplay5.config(height = 3, width = 10)
accounttypetodisplay5.grid(row = 1, column = 5)

logoutbutton5 = Button(customerorderframe, text = 'Logout', command = backtologin, fg = 'black',bg = 'white',font = ('',13,'underline'), relief = 'flat')
logoutbutton5.config(height = 1, width = 10)
logoutbutton5.grid(row = 2, column = 5)

customerorderlabel = Label(customerorderframe, text = 'Order', fg = 'black', bg = 'white', font = ('',13,'underline'))
customerorderlabel.grid(row = 3, column = 0)


conn = sqlite3.connect('codfatherdata.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM orders')
order_data = cursor.fetchall()

customerordertreeview = ttk.Treeview(customerorderframe, height = 15, columns = ('Name', 'Date Of Delivery', 'Item Numbers', 'Total Price', 'OrderID'),
                                  show = 'headings')

customerordertreeview.grid(row = 4, column = 0, columnspan = 5)

customerordertreeview.heading('Name',text = 'Name')
customerordertreeview.column('Name',minwidth = 0, width = 150, anchor = 'center')
customerordertreeview.heading('Date Of Delivery',text = 'Date of Delivery')
customerordertreeview.column('Date Of Delivery',minwidth = 0, width = 180, anchor = 'center')
customerordertreeview.heading('Item Numbers',text = 'Item Numbers')
customerordertreeview.column('Item Numbers',minwidth = 0, width = 130, anchor = 'center')
customerordertreeview.heading('Total Price',text = 'Total Price')
customerordertreeview.column('Total Price',minwidth = 0, width = 150, anchor = 'center')
customerordertreeview.heading('OrderID',text = 'OrderID')
customerordertreeview.column('OrderID',minwidth = 0, width = 150, anchor = 'center')

for data in order_data:
    customerordertreeview.insert('','end', values=data)

#----------------------New member Frame-------------------------------
title = Label(newcustomerframe, text = 'New Customer', fg = 'blue', bg ='white', font = ('Helvetica',30, 'bold',  'underline'))
title.config(height=2,width=20)
title.grid(row=0,column=0,columnspan=3)

instructions = Label(newcustomerframe, text = '•Please enter the Username and Password you would like to use.', fg = 'red', bg ='white', font = ('Helvetica',10,'bold'))
instructions.config(height=4,width=60)
instructions.grid(row=1,column=0,columnspan = 2, sticky = 'W')

usernamelabel = Label(newcustomerframe, text = 'Username: ', fg = 'black', bg = 'white')
usernamelabel.config(height = 3)
usernamelabel.grid(row = 2, column = 0, sticky = 'W')

usernamechange = StringVar()
usernametochange = Entry(newcustomerframe, textvariable = usernamechange, fg = 'black', bg = 'white', borderwidth = 2, relief = 'solid')
usernametochange.grid(row = 2, column = 1, sticky = 'W')

passwordlabel = Label(newcustomerframe, text = 'Password: ', fg ='black',bg='white')
passwordlabel.config(height = 3)
passwordlabel.grid( row = 3, column = 0, sticky = 'W')

passwordchange = StringVar()
passwordtochange = Entry(newcustomerframe, textvariable = passwordchange, fg = 'black',bg = 'white', borderwidth = 2, relief = 'solid')
passwordtochange.grid(row = 3, column = 1, sticky = 'W')



spacer5 = Label(newcustomerframe, text = 'blank', fg = 'white', bg = 'white')
spacer5.config(height = 3)
spacer5.grid(row = 4, column = 0)

newcustomerbutton = Button(newcustomerframe, text = 'Add New Customer', command = addnewcustomer, fg = 'black', bg = 'white')
newcustomerbutton.config(height = 3,width = 15)
newcustomerbutton.grid(row = 5, column = 1, sticky = 'W')

newcustomerbackbutton = Button(newcustomerframe, text = 'Back', command = backtologin, fg = 'black',bg='white')
newcustomerbackbutton.config(height = 3, width = 15)
newcustomerbackbutton.grid(row = 5, column = 0, sticky = 'W')


#-----------------------------------------------------------------------------------

raise_frame(loginframe)
root.mainloop()


