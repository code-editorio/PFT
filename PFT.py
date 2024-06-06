from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
import random as r
import sqlite3
from datetime import datetime


# SQL connection and table creation
connector = sqlite3.connect('PFT.sqlite')
cur = connector.cursor()


# cur.execute('DROP TABLE IF EXISTS PFT')

try:
    cur.execute('''
    CREATE TABLE PFT (
                ID INTEGER PRIMARY KEY, 
                Type TEXT, 
                Category TEXT, 
                Amount INTEGER,
                Recipient TEXT,
                tDate TEXT,
                Timestamp TEXT)''') #sqlite3 date format is yyyy-mm-dd, but we want dd-mm-yyyy so we leave it as text
except:
    pass

def get_user_details():
    root = Tk()
    root.title("Login")
    root.geometry("200x100")
    # root.resizable(False,False)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(5, weight=1)

    Label(root, text="Username: ").grid(column=1, row=0)
    user_name = Entry(root)
    user_name.grid(row=0, column=2, columnspan=3)
    Label(root, text="Password: ").grid(row=1, column=1)
    password = Entry(root, show="*")
    password.grid(row=1, column=2, columnspan=3)

    def submit():
        global username
        username = user_name.get()
        password_value = password.get()
        if username.strip() == "" or password_value.strip() == "":
            # If either field is empty, show an error message
            error_label.config(text="Please fill in both fields.", fg="red")
        else:
            # If both fields are filled, clear the error message and close the window
            error_label.config(text="")
            root.destroy()
    
    def clear():
        user_name.delete(0, END)
        password.delete(0, END)

    error_label = Label(root, text="", fg="red")
    error_label.grid(row=3, column=1, columnspan=2)

    Button(root, padx=10, text="Submit", command=submit).grid(row=2, column=2)
    Button(root, padx=10, text="Clear", command=clear).grid(row=2, column=3)


    root.mainloop()
    try:
        return username
    except:
        print("Please Enter Your Username and Password")

user = get_user_details()

if user == None:
    quit()


transaction_detail = {}



welcome = Tk()
welcome.title("Personal Finance Tracker")
welcome.geometry("500x500")
welcome.resizable(False,False)



welcome.grid_columnconfigure(0, weight=1)
welcome.grid_columnconfigure(8, weight=1)


Label(welcome, text="").grid()
Label(welcome, text=f'Welcome To Your Personal Finance Tracker {user.lstrip().strip().capitalize()}', font=("Helvetica", 10, "bold underline")).grid(row=0, column=1, columnspan=7, pady=20)

def get_balance():
    balance = 0
    query = 'SELECT sum(Amount) FROM PFT WHERE Type = "Income"'
    try:
        for n in cur.execute(query):
            balance += int(n[0])
    except:
        pass

    query2 = 'SELECT sum(Amount) FROM PFT WHERE Type = "Expense"'
    try:
        for n in cur.execute(query2):
            balance -= int(n[0])
    except:
        pass
    return balance

def get_last_transaction():
    last_transaction = 'SELECT * FROM PFT ORDER BY Timestamp'

    values = []
    [values.append(n) for n in cur.execute(last_transaction)]
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
                #     formatted_dict += f'Source: {value[4]}\n\n'
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
                #     formatted_dict += f'Payee: {value[4]}\n\n'
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
def update_welcome_page():
    balance_label.config(text=f'Current Account Balance: ${get_balance()}')
    transaction_label.config(text=f'Your Last Transaction: \n\n{get_last_transaction()}\n')

def add_transaction_page():
    
    welcome.withdraw()
    transaction = Tk()
    transaction.title("Add Transaction")
    transaction.geometry("389x218")
    # transaction.resizable(False,False)

    # Configure the grid to have proper weight for centering
    transaction.grid_columnconfigure(0, weight=1)
    transaction.grid_columnconfigure(1, weight=1)
    transaction.grid_columnconfigure(2, weight=1)
    transaction.grid_columnconfigure(3, weight=1)

    def income_button():

        transaction.grid_columnconfigure(0, weight=1)
        transaction.grid_columnconfigure(1, weight=0)
        transaction.grid_columnconfigure(2, weight=0)
        transaction.grid_columnconfigure(3, weight=0)
        transaction.grid_columnconfigure(4, weight=0)
        transaction.grid_columnconfigure(5, weight=1)


        transaction.geometry("500x319")
        global transaction_type
        transaction_type = 'Income'
        incomes_button.grid_forget()
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

        global transaction_amount
        global transaction_date
        global transaction_source
        global transaction_category

        transaction_amount = None
        transaction_date = None
        transaction_source = None
        transaction_category = None



        def submit(transaction_dict):
            global transaction_amount
            global transaction_date
            global transaction_source
            global transaction_category


            result = messagebox.askokcancel("Confirm Submission", "Are you sure you want to submit this values?")
            error_raised = False

            if result:
                # Validation
                try:
                    transaction_amount = int(amount_input.get())
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
                    transaction_source = source_input.get()
                    transaction_category = selected_option.get()
                except:
                    error_raised = True
                    messagebox.showerror("Error", "Please fill out all options with the right values")


                if transaction_source != None and transaction_source != "" and selected_option.get() != 'Select an option' and error_raised == False:
                    id_numbers =[]
                    sqlstr = 'SELECT ID FROM PFT'

                    for n in cur.execute(sqlstr):
                        id_numbers.append(n[0])
                    while True:
                        transaction_dict['ID'] = r.randint(1000, 9999)
                        if transaction_dict['ID'] not in id_numbers:
                            break
            
                    transaction_dict['Type'] = 'Income'
                    transaction_dict['Category'] = transaction_category
                    transaction_dict['Amount'] = transaction_amount
                    transaction_dict['Recipient'] = transaction_source
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

    def expense_button():

        transaction.grid_columnconfigure(0, weight=1)
        transaction.grid_columnconfigure(1, weight=0)
        transaction.grid_columnconfigure(2, weight=0)
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
        income_category_options = ["Food", "Rent", "Clothing", "Car", "Health", "Others"]


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
                    transaction_amount = int(amount_input.get())
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
                    transaction_dict['Category'] = transaction_category
                    transaction_dict['Amount'] = transaction_amount
                    transaction_dict['Recipient'] = transaction_payee
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
    print('Transaction Page')
    welcome.withdraw() # Temporarily closing the welcoming window

    dash = Tk() # The window for the dashboard
    dash.title('Dashboard') # The window's name
    # dash.geometry() #The size of the window


    






    query = 'SELECT ID, Type, Category, Amount, Recipient, Date FROM PFT;' # SQL code to collect the neccessary data from the database

    # Creation of the complex data structure
    all_transactions_list = [] # Becomes a list of dictionaries [{},{},{}]
    all_transactions_dict = {}

    # Add all the values to the dictionary with their respective meanings, adding that dictionary to a list then clearing that dictionary before starting again on a new row
    for row in cur.execute(query):
        all_transactions_dict['ID'] = row[0]
        all_transactions_dict['Type'] = row[1]
        all_transactions_dict['Category'] = row[2]
        all_transactions_dict['Amount'] = row[3]
        all_transactions_dict['Recipient'] = row[4]
        all_transactions_dict['Date'] = row[5]
        all_transactions_list.append(all_transactions_dict)
        all_transactions_dict = {}




    dash.mainloop()

def delete_transaction_page():
    print('Deletion Page')


Button(welcome, text= 'Add Transaction', command= add_transaction_page).grid(row=4,column=3)
Button(welcome, text= 'Transaction Summary', command= transaction_summary_page).grid(row=4,column=4)
Button(welcome, text= 'Delete Transaction', command= delete_transaction_page).grid(row=4,column=5)


welcome.mainloop()
connector.commit()
connector.close()
