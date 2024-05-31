from tkinter import *

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
transaction_details = [0]
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
        transaction.geometry("500x500")
        incomes_button.grid_forget()
        expenses_button.grid_forget()
        transaction_type.grid_forget()
        Label(transaction, text='Please Fill Out The Details', font=("Helvetica", 10, "bold underline")).grid(row=0, column=0, columnspan=4, pady=10)

    def expense_button():
        transaction.geometry("500x500")
        expenses_button.grid_forget()
        incomes_button.grid_forget()
        transaction_type.grid_forget()

        Label(transaction, text='Please Fill Out The Details', font=("Helvetica", 10, "bold underline")).grid(row=0, column=0, columnspan=4, pady=10)



    transaction_type = Label(transaction, text='What Type of Transaction?', font=("Helvetica", 10, "bold underline"))
    transaction_type.grid(row=0, column=0, columnspan=4, pady=10)
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

