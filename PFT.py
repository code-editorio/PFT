from tkinter import *
from tkinter import messagebox
from tkinter import font
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import random as r
import sqlite3
import matplotlib.pyplot as plt
import re
import pandas as pd


# SQL connection for user_details
connector = sqlite3.connect('PFT.sqlite')
cur = connector.cursor()

def start():
    # SQL connection fo user_details
    ud_connector = sqlite3.connect('details.sqlite')
    ud_cur = ud_connector.cursor()

    form_window = Tk()


    ttk.Label(form_window, text="We need some information before continuing (Yes or No)",  font=("Arial 12 bold")).grid(row=0, pady=20)
    ttk.Label(form_window, text="1. Is this your first time opening this Finance Tracker?").grid(row=1, sticky=W)

    # Variable to hold the selected value
    selected_option = StringVar()
    selected_option.set(1)

    # Radio button giving users the option 2 pick only 1
    yes_radio_1 = ttk.Radiobutton(form_window, text="Yes", variable=selected_option, value="1")
    yes_radio_1.grid(row=2, sticky= W)
    no_radio_1 = ttk.Radiobutton(form_window, text="No", variable=selected_option, value="0")
    no_radio_1.grid(row=3, sticky= W)


    ttk.Label(form_window, text='2. Would you like tester data?').grid(row=4, sticky=W, pady=10)

    # Variable to hold the selected value
    selected_option_2 = StringVar()
    selected_option_2.set(1)

    # Radio button giving users the option 2 pick only 1
    yes_radio_2 = ttk.Radiobutton(form_window, text="Yes", variable=selected_option_2, value="1")
    yes_radio_2.grid(row=5, sticky= W)
    no_radio_2 = ttk.Radiobutton(form_window, text="No", variable=selected_option_2, value="0")
    no_radio_2.grid(row=6, sticky= W)

    def get_old_user_details():

        root = Tk()
        root.title("Login")
        root.geometry("200x100")
        # root.resizable(False,False)

        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(5, weight=1)

        # Widgets to allow users to type thier passswords and username
        Label(root, text="Username: ").grid(column=1, row=0)
        user_name = Entry(root)
        user_name.grid(row=0, column=2, columnspan=3)
        Label(root, text="Password: ").grid(row=1, column=1)
        password = Entry(root, show="*")
        password.grid(row=1, column=2, columnspan=3)

        def submit():

            global username # Username to be used in other places
            username = user_name.get() # Get the username
            password_value = password.get() # Get the password
            ud_dict = dict() # Dictionary for all the usernames and password

            # Get the username and password from the database ordering by timstamp incase of later implementation of forgot password
            for v in ud_cur.execute('''SELECT * FROM user_details
                                    ORDER BY timestamp'''): 
                ud_dict[v[3]] = v[4] # Update the dictionary
            
            try:
                user_pass = ud_dict[username.strip()] # Check to see if the username has a password which would verify if it is a real username
            except:
                # show an error message if there is no username of that database
                error_label.config(text="Please fill in both fields correctly.", fg="red")
            try:
                if password_value == user_pass: # If the password given by the user is equal to the password for that user in the database then continue
                    # If both fields are filled correctly, clear the error message and close the window
                    error_label.config(text="")
                    root.destroy()
                else:
                    error_label.config(text="Username or Password Incorrect.", fg="red") # Else show them an error
            except:
                pass # In the case an error shows up from there being no password given
        
        def clear():
            user_name.delete(0, END)
            password.delete(0, END)

        error_label = Label(root, text="", fg="red")
        error_label.grid(row=3, column=1, columnspan=3)

        Button(root, padx=10, text="Submit", command=submit).grid(row=2, column=2)
        Button(root, padx=10, text="Clear", command=clear).grid(row=2, column=3)


        root.mainloop()
        try:
            return username # Try to return the username from this function
        except:
            messagebox.showerror("Error", "Please Enter Your Username and Password") # If an error occurs ask the user to give us details.

    def registering():
        # Create the main window
        registeration = Tk()
        registeration.title("Registration Page")
        registeration.geometry("400x200")

        # Define variables to hold the entered values
        first_name_var = StringVar()
        last_name_var = StringVar()
        username_var = StringVar()
        password_var = StringVar()
        email_var = StringVar()


        # Create entry fields and labels for username, password, and email
        # First Name
        first_name_label = ttk.Label(registeration, text="First Name") # ttk. Looks better so we use it here and through out registration process
        first_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="W")
        first_name_entry = ttk.Entry(registeration, textvariable=first_name_var)
        first_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Last Name
        last_name_label = ttk.Label(registeration, text="Last Name") # ttk. Looks better so we use it here and through out registration process
        last_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="W")
        last_name_entry = ttk.Entry(registeration, textvariable=last_name_var)
        last_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # Username
        username_label = ttk.Label(registeration, text="Username") # ttk. Looks better so we use it here and through out registration process
        username_label.grid(row=2, column=0, padx=10, pady=5, sticky="W")
        username_entry = ttk.Entry(registeration, textvariable=username_var)
        username_entry.grid(row=2, column=1, padx=10, pady=5)

        # Password
        password_label = ttk.Label(registeration, text="Password")
        password_label.grid(row=3, column=0, padx=10, pady=5, sticky="W")
        password_entry = ttk.Entry(registeration, textvariable=password_var, show='*')
        password_entry.grid(row=3, column=1, padx=10, pady=5)

        # Show Password
        def toggle_password():
            if password_entry.cget('show') == '': # Check to see if the password is currently visible
                password_entry.config(show='*') # Make it hidden
            else:
                password_entry.config(show='') # Make it visible

        show_password_var = BooleanVar() # variable to hold the value of the checkbutton
        show_password_checkbutton = ttk.Checkbutton(registeration, text="Show Password", variable=show_password_var, command=toggle_password)
        show_password_checkbutton.grid(row=3, column=2, padx=10, pady=5)

        # Email
        email_label = ttk.Label(registeration, text="Email")
        email_label.grid(row=4, column=0, padx=10, pady=5, sticky="W")
        email_entry = ttk.Entry(registeration, textvariable=email_var)
        email_entry.grid(row=4, column=1, padx=10, pady=5)

        # Function to handle form submission
        def submit():
            # Store the values somewhere
            first_name = first_name_var.get()
            last_name = last_name_var.get()
            username = username_var.get()
            password = password_var.get()
            email = email_var.get()

            # if all the entry widgets have values then store it into the database
            if username.strip() and password.strip() and email.strip() and first_name.strip() and last_name.strip():
                ud_cur.execute('''
                            INSERT INTO user_details (first_name, last_name, username, password, email, timestamp)
                            VALUES (?, ?, ?, ?, ?, ?)''', (first_name.strip(), last_name.strip(), username.strip(), password, email.strip(), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                messagebox.showinfo('Thank You', 'Details Saved Successfully') # Thank the user for joining the community

                # Clear the entries after submission
                first_name_var.set("")
                last_name_var.set("")
                username_var.set("")
                password_var.set("")
                email_var.set("")

                # Save the database
                ud_connector.commit()
                registeration.destroy()
            else:
                messagebox.showerror('Error', 'Please fill out the form!') # Show an error message
        
            

        # Add a submit button
        submit_button = ttk.Button(registeration, text="Submit", command=submit)
        submit_button.grid(row=5, columnspan=2, pady=20)

        # Run the main event loop
        registeration.mainloop()
        




    def done():
        choice_one, choice_two = selected_option.get(), selected_option_2.get()
        form_window.destroy()
        global user

        if choice_one == "1": # User picks yes meaning its their first time opening the PFT so new database and registration page implemented here
            registering()
            user = get_old_user_details()
            cur.execute('DROP TABLE IF EXISTS PFT')
            cur.execute('''
            CREATE TABLE PFT (
                        ID INTEGER PRIMARY KEY, 
                        Type TEXT, 
                        Category TEXT, 
                        Amount NUMERIC,
                        Recipient TEXT,
                        tDate TEXT,
                        Timestamp TEXT)''') #sqlite3 date format is yyyy-mm-dd, but we want dd-mm-yyyy so we leave it as text  
        else: # User already has data in the database so they should use the most recent username and password
            try:
                user = get_old_user_details()
            except:
                quit() # if the user isnt able to give this data and closes the page or something that would cause an error, end the program

        if choice_two == "1": # If user wants to start the tester data
            fhand = open('test_data.txt', 'r').read() # read through the whole file as one. File is an SQL code
            try:
                cur.execute(fhand.strip("\n")) # Exceute the SQL code
            except:
                pass

        else:
            fhand = open('test_data.txt', 'r').readlines() # Read the file line by line

            # Get the ID of each tester transaction
            for v in fhand:
                try:
                    id = v[1:5]
                    id = int(id)
                except:
                    continue # First line is includes insert and not the ID so skip it
                cur.execute('''DELETE FROM PFT WHERE ID = ? ''',(id,)) # Delete those rows with these specific ID's
        connector.commit()
        

    Button(form_window, text="Submit", command= done).grid(row=7, pady=10)


    form_window.mainloop()


# Function to help convert date into a more presentable format for the PFT
def tkinter_date_conversion(sql_date):
    date_obj = datetime.strptime(sql_date, '%Y-%m-%d') # Convert sql format to datetime object
    tkinter_date = date_obj.strftime('%d/%m/%Y') # Convert datetime object to standard format
    return tkinter_date

# Function to help convert date into the sql default format
def sql_date_conversion(tkinter_date):
    date_obj = datetime.strptime(tkinter_date, '%d/%m/%Y') # Convert tkinter format to datetime object
    sql_date = date_obj.strftime('%Y-%m-%d') # Convert datetime object to SQL standard format
    return sql_date

start()

transaction_detail = {}

try: # Try to check if user widget has an actual value
    if not user:
        quit() # If the widget does not have a value then quit the whole program
except: # Except is used in the case where the form window is closed which causes prblems in our code
    valid = False # If that happens then use another way to quit the program 
try:
    if not valid: # if the program is no longer valid to be executed
        quit() # quit the program
except:
    pass

welcome = Tk()
welcome.title("Personal Finance Tracker")
welcome.geometry("500x500")
welcome.resizable(False,False) # Increasing the size or reducing the size of the window spoils the design. The widget stays in the center but doesnt look as good as it is right now



welcome.grid_columnconfigure(0, weight=1)
welcome.grid_columnconfigure(8, weight=1)


Label(welcome, text="").grid()
Label(welcome, text=f'Welcome To Your Personal Finance Tracker {user.lstrip().strip().capitalize()}', font=("Helvetica", 10, "bold underline")).grid(row=0, column=1, columnspan=7, pady=20)

def get_balance():
    balance = 0

    # Run SQL queries to get sum of amount from the database where the type is income and add to balance
    query = 'SELECT sum(Amount) FROM PFT WHERE Type = "Income"'
    try:
        for n in cur.execute(query):
            balance += float(n[0])
    except:
        pass

    # Run SQL queries to get sum of amount from the database where the type is expense and subtract from balance
    query2 = 'SELECT sum(Amount) FROM PFT WHERE Type = "Expense"'
    try:
        for n in cur.execute(query2):
            balance -= float(n[0])
    except:
        pass
    return balance

def get_last_transaction():
    # Run SQL query to get all the values from the database ordered by when it entered the database

    last_transaction = 'SELECT * FROM PFT ORDER BY Timestamp'

    values = []
    [values.append(n) for n in cur.execute(last_transaction)] # add it all to a list
    # Get the most recent transaction which is the last transaction of the list
    try:
        value = values[-1]
    except:
        value = None

    # To make it look more presentable
    formatted_dict = ""
    if value != None:
        formatted_dict = ""
        if value[1] == 'Income':
            for v in range(6):
                if v == 0:
                    formatted_dict += f'ID: {value[0]}\n\n'
                elif v == 1:
                    formatted_dict += f'Type: {value[1]}\n\n'
                elif v == 2:
                    formatted_dict += f'Category: {value[2]}\n\n'
                elif v == 3:
                    formatted_dict += f'Amount: $ {value[3]}\n\n'
                # elif v == 4:
                #     formatted_dict += f'Source: {value[4]}\n\n' # The Source was not asked for in the question
                elif v == 5:
                    tdate = value[5]
                    last_transaction_date = datetime.strptime(tdate, "%Y-%m-%d") # Convert the string to a datetime object
                    new_date_format = last_transaction_date.strftime("%d/%m/%Y") # Format the datetime object to the desired format 'dd/mm/yyyy'
                    formatted_dict += f'Date: {new_date_format}'
        elif value[1] == 'Expense':
            for v in range(6):
                if v == 0:
                    formatted_dict += f'ID: {value[0]}\n\n'
                elif v == 1:
                    formatted_dict += f'Type: {value[1]}\n\n'
                elif v == 2:
                    formatted_dict += f'Category: {value[2]}\n\n'
                elif v == 3:
                    formatted_dict += f'Amount: $ {value[3]}\n\n'
                # elif v == 4:
                    # formatted_dict += f'Payee: {value[4]}\n\n' # The Payee was not asked for in the question
                elif v == 5:
                    tdate = value[5]
                    last_transaction_date = datetime.strptime(tdate, "%Y-%m-%d") # Convert the string to a datetime object
                    new_date_format = last_transaction_date.strftime("%d/%m/%Y") # Format the datetime object to the desired format 'dd/mm/yyyy'
                    formatted_dict += f'Date: {new_date_format}'
    else:
        formatted_dict = "None"

    return formatted_dict

balance_label = Label(welcome, text = f'Current Account Balance: $ {get_balance()}')
balance_label.grid(row=2,column=2, columnspan=5)
transaction_label = Label(welcome, text= f'Your Last Transaction: \n\n{get_last_transaction()}\n')
transaction_label.grid(row=3,column=3, columnspan=5)
def update_welcome_page(): # To automatically update the values of the main window (welcoming window)
    balance_label.config(text=f'Current Account Balance: ${get_balance()}')
    transaction_label.config(text=f'Your Last Transaction: \n\n{get_last_transaction()}\n')

def add_transaction_page(): # Adding transactions whether income or expense
    
    welcome.withdraw()
    transaction = Tk()
    transaction.title("Add Transaction")
    transaction.geometry("389x218")
    transaction.resizable(False,False)

    # Configure the grid to have proper weight for centering
    transaction.grid_columnconfigure(0, weight=1)
    transaction.grid_columnconfigure(1, weight=1)
    transaction.grid_columnconfigure(2, weight=1)
    transaction.grid_columnconfigure(3, weight=1)

    def income_button():

        transaction.grid_columnconfigure(0, weight=1)
        transaction.grid_columnconfigure(1, weight=0)
        transaction.grid_columnconfigure(2, weight=0) # Centers the values with weight 0
        transaction.grid_columnconfigure(3, weight=0)
        transaction.grid_columnconfigure(4, weight=0)
        transaction.grid_columnconfigure(5, weight=1)


        transaction.geometry("500x319")
        global transaction_type # Will be used in other functions
        transaction_type = 'Income'
        incomes_button.grid_forget() # grid_forget used to clear the buttons on the transaction page
        expenses_button.grid_forget()
        transaction_type_label.grid_forget()
        Label(transaction, text='Please Fill Out The Details', font=("Helvetica", 10, "bold underline")).grid(row=0, column=0, columnspan=6, pady=10)

        # Tkinter variable to hold the selected option
        selected_option = StringVar(transaction)
        selected_option.set("Select an option")  # Default Value


        # List of options for the dropdown menu
        income_category_options = ["Salary", "Pension", "Interest", "Others"]


        Label(transaction, text='Category:').grid(row=1, column=1)
        # The dropdown menu next to the Entry box
        categories = OptionMenu(transaction, selected_option, *income_category_options) # The star helps with going over the list without having to do loops or comprehension
        categories.grid(row=1, column=2, columnspan=3)


        Label(transaction, text='Amount ($):').grid(row=2, column=1)
        amount_input = Entry(transaction)
        amount_input.grid(row=2, column=2, pady=20, columnspan=3)

        Label(transaction, text='Date (dd/mm/yyyy):').grid(row=3, column=1)
        # Create a DateEntry widget
        date_input = DateEntry(transaction, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern="dd/mm/yyyy")
        date_input.grid(row=3, column=2,  columnspan=3)

        Label(transaction, text='Source:').grid(row=4, column=1)
        source_input = Entry(transaction)
        source_input.grid(row=4, column=2, pady=20, columnspan=3)


        def clear():
            amount_input.delete(0, END)
            source_input.delete(0,END)
            selected_option.set("Select an option")  # Default Value

        # Global variable to be used in other functions
        global transaction_amount 
        global transaction_date
        global transaction_source
        global transaction_category

        # Initially set to None
        transaction_amount = None
        transaction_date = None
        transaction_source = None
        transaction_category = None



        def submit(transaction_dict):
            # global variables allowing us to use it everywhere
            global transaction_amount
            global transaction_date
            global transaction_source
            global transaction_category


            result = messagebox.askokcancel("Confirm Submission", "Are you sure you want to submit this values?")
            error_raised = False

            if result:
                # Validation
                try:
                    transaction_amount =float(amount_input.get())
                except:
                    error_raised = True
                    messagebox.showerror("Error", "Invalid Amount Format") # Amount must be a float for better precision
                
                try:
                    if transaction_amount < 0:
                        error_raised = True
                        messagebox.showerror("Error", "Amount must be greater than 0") # No negative numbers
                except:
                    pass

                try:
                    tkinter_date = date_input.get()
                    date_obj = datetime.strptime(tkinter_date, '%d/%m/%Y') # Convert tkinter format to datetime object and save it
                    transaction_date = date_obj.strftime('%Y-%m-%d') # Convert datetime object to SQL standard format and save it
                    transaction_source = source_input.get() # Save the source
                    transaction_category = selected_option.get() # Save the category
                except:
                    error_raised = True
                    messagebox.showerror("Error", "Please fill out all options with the right values")

                # Make sure all the data needed to add transaction into the database is filled out and correct
                if transaction_source != None and transaction_source != "" and selected_option.get() != 'Select an option' and error_raised == False:
                    id_numbers =[]
                    sqlstr = 'SELECT ID FROM PFT'

                    # Making sure there is no repeated ID value
                    for n in cur.execute(sqlstr):
                        id_numbers.append(n[0])
                    while True:
                        transaction_dict['ID'] = r.randint(1000, 9999)
                        if transaction_dict['ID'] not in id_numbers:
                            break
                    
                    # Saving the valeus into a dictionary
                    transaction_dict['Type'] = 'Income'
                    transaction_dict['Category'] = transaction_category.capitalize()
                    transaction_dict['Amount'] = transaction_amount
                    transaction_dict['Recipient'] = transaction_source.capitalize()
                    transaction_dict['Date'] = transaction_date
                    # Insert the transaction into the database
                    cur.execute('''
                    INSERT INTO PFT (ID, Type, Category, Amount, Recipient, tDate, Timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', (transaction_dict['ID'], transaction_dict['Type'], 
                                                      transaction_dict['Category'], transaction_dict['Amount'], 
                                                      transaction_dict['Recipient'], transaction_dict['Date'],
                                                      datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    
                    connector.commit()  # Save the changes to the database
                    # transaction_list.append(transaction_detail)
                    transaction_dict = {}
                    update_welcome_page() # Update the welcoming page with the right values
                    clear() # Clear the values of the widgets
                    transaction.destroy() # Close the transaction page
                    welcome.deiconify() # deiconify used to temporarily close window
                else:
                    messagebox.showerror("Error", "Please fill out all options with the right values")
            else:
                pass

        
        def exit_window():
            result = messagebox.askokcancel("Confirm Exit", "Are you sure you want to exit this page?")
            if result:
                transaction.destroy()
                welcome.deiconify()
            else:
                pass

    
        Button(transaction, text='Submit', width=8, command= lambda : submit(transaction_detail)).grid(row=5,column=2)
        Button(transaction, text='Clear', width=8, command=clear).grid(row=5,column=3)
        Button(transaction, text='Exit', width=8, command=exit_window).grid(row=5,column=4)

    def expense_button(): # Follows the same process as income just with a few changes

        transaction.grid_columnconfigure(0, weight=1)
        transaction.grid_columnconfigure(1, weight=0)
        transaction.grid_columnconfigure(2, weight=0) # Centering col 1 - 4 
        transaction.grid_columnconfigure(3, weight=0)
        transaction.grid_columnconfigure(4, weight=0)
        transaction.grid_columnconfigure(5, weight=1)


        transaction.geometry("500x319")
        global transaction_type
        transaction_type = 'Expense'
        incomes_button.grid_forget()
        expenses_button.grid_forget()
        transaction_type_label.grid_forget()
        Label(transaction, text='Please Fill Out The Details', font=("Helvetica", 10, "bold underline")).grid(row=0, column=0, columnspan=6, pady=10)

        # Tkinter variable to hold the selected option
        selected_option = StringVar(transaction)
        selected_option.set("Select an option")  # Default Value


        # List of options for the dropdown menu
        income_category_options = ["Food", "Rent", "Clothing", "Car", "Health", "Others"] # options for expenses


        Label(transaction, text='Category:').grid(row=1, column=1)
        # The dropdown menu next to the Entry box
        categories = OptionMenu(transaction, selected_option, *income_category_options) # The star helps with going over the list without having to do loops or comprehension
        categories.grid(row=1, column=2, columnspan=3)


        Label(transaction, text='Amount ($):').grid(row=2, column=1)
        amount_input = Entry(transaction)
        amount_input.grid(row=2, column=2, pady=20, columnspan=3)

        Label(transaction, text='Date (dd/mm/yyyy):').grid(row=3, column=1)
        # Create a DateEntry widget
        date_input = DateEntry(transaction, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern = "dd/mm/yyyy")
        date_input.grid(row=3, column=2,  columnspan=3)

        Label(transaction, text='Payee:').grid(row=4, column=1)
        payee_input = Entry(transaction)
        payee_input.grid(row=4, column=2, pady=20, columnspan=3)


        def clear():
            amount_input.delete(0, END)
            payee_input.delete(0,END)
            selected_option.set("Select an option")  # Default Value

        global transaction_amount
        global transaction_date
        global transaction_payee
        global transaction_category

        transaction_amount = None
        transaction_date = None
        transaction_payee = None
        transaction_category = None



        def submit(transaction_dict):
            global transaction_amount
            global transaction_date
            global transaction_payee
            global transaction_category

            error_raised = False
            result = messagebox.askokcancel("Confirm Submission", "Are you sure you want to submit this values?")

            if result:
                try:
                    transaction_amount = float(amount_input.get())
                except:
                    error_raised = True
                    messagebox.showerror("Error", "Invalid Amount Format")

                try:
                    if transaction_amount < 0:
                        error_raised = True
                        messagebox.showerror("Error", "Amount must be greater than 0")
                except:
                    pass
                
                try:
                    tkinter_date = date_input.get()
                    date_obj = datetime.strptime(tkinter_date, '%d/%m/%Y') # Convert tkinter format to datetime object
                    transaction_date = date_obj.strftime('%Y-%m-%d') # Convert datetime object to SQL standard format
                    transaction_payee = payee_input.get()
                    transaction_category = selected_option.get()
                except:
                    error_raised = True
                    messagebox.showerror("Error", "Please fill out all options with the right values")

                if transaction_payee != None and transaction_payee != "" and selected_option.get() != 'Select an option' and error_raised == False:
                    id_numbers =[]
                    sqlstr = 'SELECT ID FROM PFT'

                    for n in cur.execute(sqlstr):
                        id_numbers.append(n[0])
                    while True:
                        transaction_dict['ID'] = r.randint(1000, 9999)
                        if transaction_dict['ID'] not in id_numbers:
                            break
            
                    transaction_dict['Type'] = 'Expense'
                    transaction_dict['Category'] = transaction_category.capitalize()
                    transaction_dict['Amount'] = transaction_amount
                    transaction_dict['Recipient'] = transaction_payee.capitalize()
                    transaction_dict['Date'] = transaction_date

                    # Insert the transaction into the database
                    cur.execute('''
                    INSERT INTO PFT (ID, Type, Category, Amount, Recipient, tDate, Timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', (transaction_dict['ID'], transaction_dict['Type'], transaction_dict['Category'], 
                                                   transaction_dict['Amount'], transaction_dict['Recipient'], transaction_dict['Date'],
                                                   datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    
                    connector.commit()  # Save the changes to the database
                    # transaction_list.append(transaction_detail)
                    transaction_dict = {}
                    update_welcome_page()
                    clear()
                    transaction.destroy()
                    welcome.deiconify()
                else:
                    messagebox.showerror("Error", "Please fill out all options with the right values")
            else:
                pass

        
        def exit_window():
            result = messagebox.askokcancel("Confirm Exit", "Are you sure you want to exit this page?")
            if result:
                transaction.destroy()
                welcome.deiconify()
            else:
                pass


        Button(transaction, text='Submit', width=8, command= lambda : submit(transaction_detail)).grid(row=5,column=2)
        Button(transaction, text='Clear', width=8, command=clear).grid(row=5,column=3)
        Button(transaction, text='Exit', width=8, command=exit_window).grid(row=5,column=4)



    transaction_type_label = Label(transaction, text='What Type of Transaction?', font=("Helvetica", 10, "bold underline"))
    transaction_type_label.grid(row=0, column=0, columnspan=4, pady=10)
    incomes_button = Button(transaction, text='Income', width=10, command= income_button)
    incomes_button.grid(row=1, column=1)
    expenses_button = Button(transaction, text='Expense', width=10,  command=expense_button)
    expenses_button.grid(row=1, column=2)

    transaction.mainloop()

def transaction_summary_page():
    welcome.withdraw() # Temporarily closing the welcoming window

    dash = Tk() # The window for the dashboard
    dash.title('Dashboard') # The window's name
    dash.geometry('1080x800') #The size of the window will become full screen

    dash.grid_columnconfigure(0,weight=1) # Centering the entire window
    dash.grid_columnconfigure(8,weight=1) # Centering the entire window


    # Row 1
    # Start Time
    Label(dash, text="From: ", font="10").grid(row=1,column=1,pady=5,)
    start_date_input = DateEntry(dash, width=20, background='darkblue', foreground='white', borderwidth=2, date_pattern="dd/mm/yyyy")
    start_date_input.grid(row=1, column=2, sticky=W, padx=0) # Using sticky for better design

    #End Time
    Label(dash, text="To: ", font="10").grid(row=1,column=3,pady=5)
    end_date_input = DateEntry(dash, width=20, background='darkblue', foreground='white', borderwidth=2, date_pattern="dd/mm/yyyy")
    end_date_input.grid(row=1, column=4, sticky=W) # Using sticky for better design

    # Type
    Label(dash, text="Type: ", font="10").grid(row=1,column=5)
    # Dropdown procedure
    type_options = ["Income", "Expense"]
    drop_down = ttk.Combobox(dash, values=type_options, width=20)
    drop_down.set("Income or Expense")
    drop_down.grid(row=1, column=6, sticky=W)

    # Row 2
    # Category
    Label(dash, text="Category: ", font="10").grid(row=2,column=1)
    category_options = ["None"]
    category_choice = ttk.Combobox(dash, values=category_options,width=23)
    category_choice.grid(row=2, column=2, sticky=W)

    # Changing the category values when the Type changes
    def update_second_dropdown(event):
        selected_option = drop_down.get()
        if selected_option == "Income": # If the dropdown widget for type is at Income
            new_options = ["Salary", "Pension", "Interest", "Others"] # Then change this widget to the types of income
        elif selected_option == "Expense": # Do the same for Expense
            new_options = ["Food", "Rent", "Clothing", "Car", "Health", "Others"]
        else:
            new_options = ["None"] # If its neither then set the widget to none
        category_choice['values'] = new_options
        if new_options:
            category_choice.set(new_options[0]) 
        else:
            category_choice.set("None")



    drop_down.bind("<<ComboboxSelected>>", update_second_dropdown) # Bind the updating function to the dropdown

    # Source or Payee
    Label(dash, text="Recipient: ", font="10").grid(row=2,column=3)
    recipient_choice = Entry(dash, width=23)
    recipient_choice.grid(row=2, column=4, sticky=W)


    read_only_text = Text(dash, width=90, height=10, wrap='word', font=('Arial', 12)) # The text box for inserting the transactions
    read_only_text.grid(row=3, column=1, columnspan=6, pady=20)
    # Disable the Text widget to make it read-only
    read_only_text.config(state='disabled')


    def show(): # The process to show the user the data they want
        # Disable the Text widget to make it read-only
        read_only_text.config(state='normal')

        read_only_text.delete("1.0", END) # Clear the text already there before adding new ones

        try: # Try to get the data from the widgets
            start_tDate = sql_date_conversion(start_date_input.get()) # Start Date
            end_tDate = sql_date_conversion(end_date_input.get()) # Ending Date
            utype = drop_down.get() # Type (Income or Expense)
            category = category_choice.get().strip() # Category
            recipient = recipient_choice.get().strip() # Payee or Source
        except:
            pass
        if utype == "Income or Expense":
            messagebox.showerror("Sorry", "You need to pick a Type")
        if utype.lower() == "income" and recipient == "":

            query = f'''
                SELECT ID, Type, Category, Amount, Recipient, tDate FROM PFT
                WHERE tDate BETWEEN ? AND ? AND
                Category == ? AND
                Type == "Income"
                ORDER BY Timestamp;
            ''' # SQL code to collect the neccessary data from the database

            # Creation of the complex data structure
            all_transactions_list = [] # Becomes a list of dictionaries [{},{},{}] with the for loop below
            all_transactions_dict = {}

            # Add all the values to the dictionary with their respective meanings, adding that dictionary to a list then clearing that dictionary before starting again on a new row
            for row in cur.execute(query, (start_tDate, end_tDate, category.capitalize())):
                all_transactions_dict['ID'] = row[0]
                all_transactions_dict['Type'] = row[1]
                all_transactions_dict['Category'] = row[2]
                all_transactions_dict['Amount'] = row[3]
                all_transactions_dict['Recipient'] = row[4]
                all_transactions_dict['Date'] = tkinter_date_conversion(row[5])
                all_transactions_list.append(all_transactions_dict)
                all_transactions_dict = {}
        elif utype.lower() == "expense" and recipient == "":
            query = f'''
                SELECT ID, Type, Category, Amount, Recipient, tDate FROM PFT
                WHERE tDate BETWEEN ? AND ? AND
                Category == ? AND
                Type == "Expense"
                ORDER BY Timestamp;
            ''' # SQL code to collect the neccessary data from the database

            # Creation of the complex data structure
            all_transactions_list = [] # Becomes a list of dictionaries [{},{},{}] with the for loop below
            all_transactions_dict = {}

            # Add all the values to the dictionary with their respective meanings, adding that dictionary to a list then clearing that dictionary before starting again on a new row
            for row in cur.execute(query, (start_tDate, end_tDate, category.capitalize())):
                all_transactions_dict['ID'] = row[0]
                all_transactions_dict['Type'] = row[1]
                all_transactions_dict['Category'] = row[2]
                all_transactions_dict['Amount'] = row[3]
                all_transactions_dict['Recipient'] = row[4]
                all_transactions_dict['Date'] = tkinter_date_conversion(row[5])
                all_transactions_list.append(all_transactions_dict)
                all_transactions_dict = {}



        count = 1
        try:
            if len(all_transactions_list) > 0:
                for row in all_transactions_list: # Collecting all the transactions in the database and inserting them into the text box in a clean format
                    formatted_text = ', '.join(f"{key}: {value}" for key, value in row.items())
                    read_only_text.insert(END, f'{count} |\t{formatted_text}\n\n')
                    count += 1
            else:
                read_only_text.insert(END, "No Values Match Your Requirements")
        except:
            pass
        # Disable the Text widget to make it read-only
        read_only_text.config(state='disabled')


    def show_all():
        # Enable the Text widget
        read_only_text.config(state='normal')

        read_only_text.delete("1.0", END) # Clear the text already there before adding new ones

        query = f'''SELECT ID, Type, Category, Amount, Recipient, tDate FROM PFT
                    ORDER BY Timestamp;''' # SQL code to collect the neccessary data from the database

        # Creation of the complex data structure
        all_transactions_list = [] # Becomes a list of dictionaries [{},{},{}] with the for loop below
        all_transactions_dict = {}



        # Add all the values to the dictionary with their respective meanings, adding that dictionary to a list then clearing that dictionary before starting again on a new row
        for row in cur.execute(query):
            all_transactions_dict['ID'] = row[0]
            all_transactions_dict['Type'] = row[1]
            all_transactions_dict['Category'] = row[2]
            all_transactions_dict['Amount'] = row[3]
            all_transactions_dict['Recipient'] = row[4]
            all_transactions_dict['Date'] = tkinter_date_conversion(row[5])
            all_transactions_list.append(all_transactions_dict)
            all_transactions_dict = {}

        count = 1
        if len(all_transactions_list) > 0:
            for row in all_transactions_list: # Collecting all the transactions in the database and inserting them into the text box in a clean format
                formatted_text = ', '.join(f"{key}: {value}" for key, value in row.items())
                read_only_text.insert(END, f'{count} |\t{formatted_text}\n\n')
                count += 1
        else:
            read_only_text.insert(END, "You Have No Transactions")

        # Disable the Text widget to make it read-only
        read_only_text.config(state='disabled')

    def printer():

        verification = messagebox.askyesno("Wait", "Are you sure you want to print this data?")

        if verification:

            document_data = read_only_text.get("1.0",END)

            if document_data.strip() == "" or document_data.strip() == "You Have No Transactions":
                messagebox.showerror("Error", "Please Generate Data To Create The Document")
            else:
                # Regular expression to match the values after each colon
                pattern = r':\S*([^,]+)'

                data = list()
                trans_id = list()
                trans_type = list()
                trans_category = list()
                trans_amount = list()
                trans_recipient = list()
                trans_date = list()

                tester = list()
                read_only_data = read_only_text.get("1.0", END).strip("\n").split("\n\n")

                for v in read_only_data:
                    try:
                        tester.append([v.split("\t")[1]]) # Seperating each line by the tab space  1 |\t .... then collecting the value after the tab
                    except:
                        pass
                

                for v in tester:
                    line = ', '.join(v)
                    try:
                        # Find all matches
                        matches = re.findall(pattern, line) # find all the values after the colon and before the comma that seperates each value
                        data.append(matches) # save that value
                    except:
                        pass

                # Print the extracted values
                for match in data:
                    trans_id.append(match[0].strip())
                    trans_type.append(match[1].strip())
                    trans_category.append(match[2].strip())
                    trans_amount.append(match[3].strip())
                    trans_recipient.append(match[4].strip())
                    trans_date.append(match[5].strip())

                csv_data = {
                    "Transaction ID": trans_id,
                    "Transaction Type": trans_type,
                    "Transaction Category": trans_category,
                    "Transaction Amount": trans_amount,
                    "Transaction Recipient": trans_recipient,
                    "Transaction Date": trans_date
                }

                df = pd.DataFrame(csv_data)

                # Export the DataFrame to a CSV file
                # Generate a unique filename using the current timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{user.capitalize()}_PFT_{timestamp}.csv" # eg. David_PFT_2023/02/22_122905

                df.to_csv(filename, index=False) # Create a csv file
                messagebox.showinfo("Thank You", "Statement Printed out Successfully. Please Check Your Folder!") # Notify user process is finished


    def bar():

        # Use SQL queries to collect data from the database for the bar chart.
        # Generate errors if the data needed is not given
        
        if drop_down.get() == "Income or Expense":
            messagebox.showerror("Error", "No data to work with. Try picking a Type")
        else:
            prompt = '''SELECT tDate, 
                        Amount 
                        FROM PFT 
                        WHERE tDate BETWEEN ? AND ? 
                        AND Type == ? 
                        AND Category == ?;'''
            x = []
            y = []

            for v in cur.execute(prompt,(sql_date_conversion(start_date_input.get()),sql_date_conversion(end_date_input.get()), drop_down.get(),category_choice.get())):
                x.append(tkinter_date_conversion(v[0]))
                y.append(v[1])
            
            if len(x) > 0 or len(y) > 0 or len(x) == len(y):
                plt.figure(figsize=(8, 5))  # Adjust figure size
                plt.bar(x, y)
                plt.xticks(rotation=45)  # Rotate x-axis labels to avoid overcrowding
                plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to make room for labels
                plt.title(f'{drop_down.get()} Graph Between {start_date_input.get()} - {end_date_input.get()} for {category_choice.get()}')
                plt.show()
            else:
                messagebox.showinfo("Error", "No data found for this time period and transaction type.")
            
    def pie():

        # Use SQL queries to collect data from the database for the Pie chart.
        # Generate errors if the data needed is not given

        if drop_down.get() == "Income or Expense" or drop_down.get().strip() == "" or drop_down.get().strip() != "Income" and drop_down.get().strip() != "Expense":
            messagebox.showerror("Error", "Please Choose a Type")
        else:
            prompt = '''SELECT 
                        Category, 
                        (SUM(Amount) * 100.0 / (SELECT SUM(Amount) FROM PFT)) AS Percentage 
                        FROM PFT
                        WHERE tDate BETWEEN ? AND ? 
                        AND Type == ?
                        GROUP BY Category;'''
            sizes = []
            label = []

            for v in cur.execute(prompt,(sql_date_conversion(start_date_input.get()),sql_date_conversion(end_date_input.get()), drop_down.get())):
                label.append(v[0]) # label
                sizes.append(round(v[1],2)) # Percentages

            show()
            # plt.figure(figsize=(10, 6))  # Adjust figure size
            plt.pie(sizes,autopct='%1.1f%%', startangle=90) # textprops=dict(color="black"))
            plt.legend(label)
            plt.axis('equal')
            plt.title(drop_down.get())
            plt.show()

    def exiter():
        verification = messagebox.askyesno("Wait", "Are you sure you want to leave this page")
        if verification:
            dash.destroy()
            welcome.deiconify()

    Button(dash, text="Show", font="10", width=10, command= show).grid(row=1,column=7,pady=5)
    Button(dash, text="Show All", font="10", width=10, command= show_all).grid(row=1,column=8,pady=5)
    Button(dash, text="Print", font="10", width=10, command= printer).grid(row=2,column=7,pady=5)
    Button(dash, text="Exit", font="10", width=10, command= exiter).grid(row=2,column=8,pady=5)
    Button(dash, text="Bar Graph", font="10", width=10, command= bar).grid(row=4,column=1,pady=5)
    Button(dash, text="Pie Chart", font="10", width=10, command= pie).grid(row=4,column=2,pady=5)

    dash.mainloop()

def delete_transaction_page():
    welcome.withdraw()
    deletetion_window = Tk()
    deletetion_window.title("Delete Transaction")
    deletetion_window.geometry("800x600")

    deletetion_window.columnconfigure(0, weight=1)
    deletetion_window.columnconfigure(8,weight=1)

    # Create a font with underline and bold
    bold_underlined_font = font.Font(deletetion_window, family="Helvetica", size=12, weight="bold", underline=1) 

    Label(deletetion_window, text="Please Choose a transaction based of its ID", font=bold_underlined_font).grid(row=0, column=1, columnspan=6, pady=20)

    read_only_text = Text(deletetion_window, width=90, height=10, wrap='word', font=('Arial', 12))
    read_only_text.grid(row=1, column=1, padx=5, pady=5, columnspan=6)
    read_only_text.config(state='disabled')

    def present_data():
        read_only_text.config(state='normal')
        read_only_text.delete("1.0", END) # Clear the text already there before adding new ones

        query = f'''SELECT ID, Type, Category, Amount, Recipient, tDate FROM PFT
                    ORDER BY Timestamp;''' # SQL code to collect the neccessary data from the database

        # Creation of the complex data structure
        all_transactions_list = [] # Becomes a list of dictionaries [{},{},{}] with the for loop below
        all_transactions_dict = {}



        # Add all the values to the dictionary with their respective meanings, adding that dictionary to a list then clearing that dictionary before starting again on a new row
        for row in cur.execute(query):
            all_transactions_dict['ID'] = row[0]
            all_transactions_dict['Type'] = row[1]
            all_transactions_dict['Category'] = row[2]
            all_transactions_dict['Amount'] = row[3]
            all_transactions_dict['Recipient'] = row[4]
            all_transactions_dict['Date'] = tkinter_date_conversion(row[5])
            all_transactions_list.append(all_transactions_dict)
            all_transactions_dict = {}

        count = 1
        if len(all_transactions_list) > 0:
            for row in all_transactions_list: # Collecting all the transactions in the database and inserting them into the text box in a clean format
                read_only_text.config(state='normal')
                formatted_text = ', '.join(f"{key}: {value}" for key, value in row.items())
                read_only_text.insert(END, f'{count} |   {formatted_text}\n\n')
                # Disable the Text widget to make it read-only
                read_only_text.config(state='disabled')
                count += 1
        else:
            read_only_text.insert(END, "You Have No Transactions")

    present_data()
    transaction_id = Entry(deletetion_window, width=20)
    transaction_id.grid(row=2, column=4)
    def delete_data():
        verification = messagebox.askyesno("Wait", "Are you sure you want delete this transaction?")
        if verification:
            try:
                deleting_id = int(transaction_id.get())
                if len(deleting_id) == 4:
                    query = 'DELETE FROM PFT WHERE ID == ?;' # SQL code to delete the selected transaction

                    cur.execute(query,(deleting_id,))
                    update_welcome_page()
                    present_data()
                    messagebox.showinfo("Thank You", "Transaction Deleted Succesfully!!")
                else:
                    messagebox.showerror("Error", "Please Input a 4 digit Transaction ID!")
            except:
                messagebox.showerror("Error", "Please Enter a Valid ID")
            connector.commit() # Save the result after deleting the data from the database

    def exiting():
        verification = messagebox.askyesno("Wait", "Are you sure you want to Leave this page?")
        if verification == 'yes':
            deletetion_window.destroy()
            welcome.deiconify()
    Button(deletetion_window, text="Delete Transaction", font=(10), command=delete_data).grid(row=2,column=5, pady=20, sticky=W)
    Button(deletetion_window, text="Exit", font=(10), command=exiting).grid(row=2,column=6, pady=20, sticky=W)

    deletetion_window.mainloop()


Button(welcome, text= 'Add Transaction', command= add_transaction_page).grid(row=4,column=3)
Button(welcome, text= 'Transaction Summary', command= transaction_summary_page).grid(row=4,column=4)
Button(welcome, text= 'Delete Transaction', command= delete_transaction_page).grid(row=4,column=5)


welcome.mainloop()
connector.commit()
connector.close()
