from tkinter import *
from tkinter import messagebox
import random as r

def get_user_details():
    root = Tk()
    root.title("Login")
    root.geometry("200x100")
    root.resizable(False,False)


    Label(root, text="Username: ").grid(column=0, row=0)
    user_name = Entry(root)
    user_name.grid(row=0, column=1, columnspan=3)
    Label(root, text="Password: ").grid(row=1, column=0)
    password = Entry(root, show="*")
    password.grid(row=1, column=1, columnspan=3)

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
    error_label.grid(row=3, column=0, columnspan=2)

    Button(root, padx=10, text="Submit", command=submit).grid(row=2, column=1)
    Button(root, padx=10, text="Clear", command=clear).grid(row=2, column=2)


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
    transaction.resizable(False,False)

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

        user_dropdown_choice = selected_option.get()
        user_dropdown_choice = user_dropdown_choice.strip().lower()

        # List of options for the dropdown menu
        options = ["Category", "Amount", "Date", "Source"]

        # The dropdown menu next to the Entry box
        dropdown = OptionMenu(transaction, selected_option, *options) # The star helps with going over the list without having to do loops or comprehension
        dropdown.grid(row=1, column=1)

        user_input = Entry(transaction)
        user_input.grid(row=1, column=2, columnspan=3)

        def clear():
            user_input.delete(0, END)

        def clear_entry(*args):
            global user_dropdown_choice
            user_dropdown_choice = selected_option.get()
            print(f"{user_dropdown_choice} : {selected_option.get()}")
            user_input.delete(0, END)

        def submit():
            global transaction_amount
            global transaction_date
            global transaction_source
            global transaction_category

            if user_dropdown_choice == "amount":
                transaction_amount = user_input.get()
                user_input.delete(0, END)
            if user_dropdown_choice == "date":
                transaction_date = user_input.get()
                user_input.delete(0, END)
            if user_dropdown_choice == "source":
                transaction_source = user_input.get()
                user_input.delete(0, END)
            if user_dropdown_choice == "category":
                transaction_category = user_input.get()
                user_input.delete(0, END)
            else:
                print(user_dropdown_choice)

        
        def exit_window():
            id_numbers =[]
            for n in transaction_details:
                id_numbers.append(transaction_details[n]['ID'])
            while True:
                transaction_detail['ID'] = r.randint(1000, 9999)
                if transaction_detail['ID'] not in id_numbers:
                    break
    
            transaction_detail['Type'] = 'Income'
            transaction_detail['Category'] = transaction_category
            transaction_detail['Amount'] = transaction_amount
            transaction_detail['Date'] = transaction_date
            transaction_details.append(transaction_detail)
            transaction_detail = {}
            transaction.destroy()

        # When a new option is chosen, the entry is cleared
        selected_option.trace("w", clear_entry)

        Button(transaction, text='Submit', width=8, command=submit).grid(row=2,column=2)
        Button(transaction, text='Clear', width=8, command=clear).grid(row=2,column=3)
        Button(transaction, text='Exit', width=8, command=exit_window).grid(row=2,column=4)


    def expense_button():
        transaction.geometry("500x500")
        global transaction_type
        transaction_type = 'Expense'
        expenses_button.grid_forget()
        incomes_button.grid_forget()
        transaction_type_label.grid_forget()

        Label(transaction, text='Please Fill Out The Details', font=("Helvetica", 10, "bold underline")).grid(row=0, column=0, columnspan=4, pady=10)



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



Label(welcome, text="").pack()
Label(welcome, text=f'Welcome To Your Personal Finance Tracker {user}', font=("Helvetica", 10, "bold underline")).pack()
Label(welcome, text="").pack()
Label(welcome, text = f'Current Account Balance: ${balance}').pack()
Label(welcome, text= f'Your Last Transaction: {transaction_details[-1]}').pack()
Button(welcome, text= 'Add Transaction', command=add_transaction).pack()


welcome.mainloop()

