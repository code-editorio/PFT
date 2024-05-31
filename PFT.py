from tkinter import *

def get_user_details():
    root = Tk()
    root.title("Login")


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

welcome = Tk()
welcome.title("Personal Finance Tracker")
welcome.geometry("500x500")

def add_transaction():
    # global transaction_detail
    # global transaction_details
    # global balance
    welcome.destroy()

    transaction = Tk()
    transaction.title("Add Transaction")
    transaction.geometry("500x500")



    transaction.mainloop()



Label(welcome, text="").pack()
Label(welcome, text=f'Welcome To Your Personal Finance Tracker {username}', font=("Helvetica", 10, "bold underline")).pack()
Label(welcome, text="").pack()
Label(welcome, text = f'Current Account Balance: ${balance}').pack()
Label(welcome, text= f'Your Last Transaction: {transaction_details[-1]}').pack()
Button(welcome, text= 'Add Transaction', command=add_transaction).pack()


welcome.mainloop()