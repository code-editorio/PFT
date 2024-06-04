from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
import random as r


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
    return username

user = get_user_details()
balance = 0
transaction_details = [{'ID': 3232, 'Type': 'Income', 'Category': 'Pension', 'Amount': 12444, "Date": "09/09/2009"}]
transaction_detail = {}

def transaction_page():

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


        transaction.geometry("500x219")
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

        Label(transaction, text='Date (dd/mm/yy):').grid(row=3, column=1)
        # Create a DateEntry widget
        date_input = DateEntry(transaction, width=12, background='darkblue', foreground='white', borderwidth=2)
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



        def submit(transaction_list, transaction_dict):
            global transaction_amount
            global transaction_date
            global transaction_source
            global transaction_category


            result = messagebox.askokcancel("Confirm Submission", "Are you sure you want to submit this values?")

            if result:
                try:
                    transaction_amount = int(amount_input.get())
                except:
                    messagebox.showerror("Error", "Invalid Amount Format")

                try:
                    transaction_date = date_input.get()
                    transaction_source = source_input.get()
                    transaction_category = selected_option.get()
                except:
                    messagebox.showerror("Error", "Please fill out all options with the right values")

                if transaction_source != None and transaction_source != "" and selected_option.get() != 'Select an option':
                    id_numbers =[]
                    for n in transaction_list:
                        values = n['ID']
                        id_numbers.append(values)
                    while True:
                        transaction_dict['ID'] = r.randint(1000, 9999)
                        if transaction_detail['ID'] not in id_numbers:
                            break
            
                    transaction_dict['Type'] = 'Income'
                    transaction_dict['Category'] = transaction_category
                    transaction_dict['Amount'] = transaction_amount
                    transaction_dict['Date'] = transaction_date
                    transaction_list.append(transaction_detail)
                    transaction_dict = {}
                    clear()
                else:
                    messagebox.showerror("Error", "Please fill out all options with the right values")
            else:
                pass
            print(transaction_list)

        
        def exit_window():
            result = messagebox.askokcancel("Confirm Exit", "Are you sure you want to exit this page?")
            if result:
                transaction.destroy()
            else:
                pass


        Button(transaction, text='Submit', width=8, command= lambda : submit(transaction_details, transaction_detail)).grid(row=5,column=2)
        Button(transaction, text='Clear', width=8, command=clear).grid(row=5,column=3)
        Button(transaction, text='Exit', width=8, command=exit_window).grid(row=5,column=4)


    def expense_button():

        transaction.grid_columnconfigure(0, weight=1)
        transaction.grid_columnconfigure(1, weight=0)
        transaction.grid_columnconfigure(2, weight=0)
        transaction.grid_columnconfigure(3, weight=0)
        transaction.grid_columnconfigure(4, weight=0)
        transaction.grid_columnconfigure(5, weight=1)


        transaction.geometry("500x219")
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

        Label(transaction, text='Date (dd/mm/yy):').grid(row=3, column=1)
        # Create a DateEntry widget
        date_input = DateEntry(transaction, width=12, background='darkblue', foreground='white', borderwidth=2)
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



        def submit(transaction_list, transaction_dict):
            global transaction_amount
            global transaction_date
            global transaction_source
            global transaction_category


            result = messagebox.askokcancel("Confirm Submission", "Are you sure you want to submit this values?")

            if result:
                try:
                    transaction_amount = int(amount_input.get())
                except:
                    messagebox.showerror("Error", "Invalid Amount Format")

                try:
                    transaction_date = date_input.get()
                    transaction_source = source_input.get()
                    transaction_category = selected_option.get()
                except:
                    messagebox.showerror("Error", "Please fill out all options with the right values")

                if transaction_source != None and transaction_source != "" and selected_option.get() != 'Select an option':
                    id_numbers =[]
                    for n in transaction_list:
                        values = n['ID']
                        id_numbers.append(values)
                    while True:
                        transaction_dict['ID'] = r.randint(1000, 9999)
                        if transaction_detail['ID'] not in id_numbers:
                            break
            
                    transaction_dict['Type'] = 'Income'
                    transaction_dict['Category'] = transaction_category
                    transaction_dict['Amount'] = transaction_amount
                    transaction_dict['Date'] = transaction_date
                    transaction_list.append(transaction_detail)
                    transaction_dict = {}
                    clear()
                else:
                    messagebox.showerror("Error", "Please fill out all options with the right values")
            else:
                pass
            print(transaction_list)

        
        def exit_window():
            result = messagebox.askokcancel("Confirm Exit", "Are you sure you want to exit this page?")
            if result:
                transaction.destroy()
            else:
                pass


        Button(transaction, text='Submit', width=8, command= lambda : submit(transaction_details, transaction_detail)).grid(row=5,column=2)
        Button(transaction, text='Clear', width=8, command=clear).grid(row=5,column=3)
        Button(transaction, text='Exit', width=8, command=exit_window).grid(row=5,column=4)



    transaction_type_label = Label(transaction, text='What Type of Transaction?', font=("Helvetica", 10, "bold underline"))
    transaction_type_label.grid(row=0, column=0, columnspan=4, pady=10)
    incomes_button = Button(transaction, text='Income', width=10, command=income_button)
    incomes_button.grid(row=1, column=1)
    expenses_button = Button(transaction, text='Expense', width=10,  command=expense_button)
    expenses_button.grid(row=1, column=2)

    transaction.mainloop()


welcome = Tk()
welcome.title("Personal Finance Tracker")
welcome.geometry("500x500")
welcome.resizable(False,False)


def add_transaction():
    # global transaction_detail
    # global transaction_details
    # global balance
    welcome.destroy()
    transaction_page()

# To make it look more presentable
formatted_dict = ', '.join([f"{key}: {value}" for key, value in transaction_details[-1].items()])

Label(welcome, text="").pack()
Label(welcome, text=f'Welcome To Your Personal Finance Tracker {user}', font=("Helvetica", 10, "bold underline")).pack()
Label(welcome, text="").pack()
Label(welcome, text = f'Current Account Balance: ${balance}').pack()
Label(welcome, text= f'Your Last Transaction: \n{formatted_dict}').pack()
Button(welcome, text= 'Add Transaction', command=add_transaction()).pack()


welcome.mainloop()

