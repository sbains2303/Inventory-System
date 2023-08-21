import tkinter as tk
import shortuuid
import customtkinter
import inventory
import products
import insights

prod = []
sup = []
cust = []


def nextW():
    pass


class loginWindow:
    def __init__(self, master):

        self.master = master
        self.container = tk.Frame(self.master)
        self.master.geometry("300x280")
        self.master.title('Login')
        self.master.configure(bg="#DBDBDB")

        self.labelUsr = customtkinter.CTkLabel(self.master, text="Log in", font=('Helvetica',20,'bold'))
        self.labelUsr.place(x=30, y=20)

        self.labelUsr = customtkinter.CTkLabel(self.master, text="Username: ")
        self.labelUsr.place(x=50, y=60)
        username_entry = customtkinter.CTkEntry(self.master)
        username_entry.place(x=50, y=90)

        self.labelPass = customtkinter.CTkLabel(self.master, text="Password: ")
        self.labelPass.place(x=50, y=120)
        password_entry = customtkinter.CTkEntry(self.master)
        password_entry.place(x=50, y=150)

        self.login_button = customtkinter.CTkButton(self.master,text="Log in", fg_color="#006400", command = self.new_window)
        self.login_button.place(x=130, y=230)


    def new_window(self):
        self.master.withdraw()
        self.master = customtkinter.CTk()
        self.app = MainPage(self.master)
        self.master.mainloop()


class MainPage:
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x320")
        self.master.title("Main Menu")

        self.label = customtkinter.CTkLabel(self.master,text="Inventory Management System", font=('Helvetica',20,'bold') )
        self.label.place(x=60,y=20)

        self.invButton = customtkinter.CTkButton(self.master, text="Inventory", height=40, border_width=1, width=300, font=('Helvetica', 17), command=lambda: self.new_window(
            inventory.inventory_window))
        self.invButton.place(x=30, y=60)

        self.prodButton = customtkinter.CTkButton(self.master, text="Products", height=40, width=260, border_width=1, font=('Helvetica', 17), command=lambda: self.new_window(
            products.products_window))
        self.prodButton.place(x=30, y=100)

        self.suppButton = customtkinter.CTkButton(self.master,text="Suppliers", border_width=1, height=40, width=220,font=('Helvetica', 17), command=nextW)
        self.suppButton.place(x=30, y=140)

        self.purchButton = customtkinter.CTkButton(self.master,text="Purchases", border_width=1,height=40, width=180,font=('Helvetica', 17), command=nextW)
        self.purchButton.place(x=30, y=180)

        self.salButton = customtkinter.CTkButton(self.master,text="Sales", border_width=1,height=40, width=140, font=('Helvetica', 17), command=nextW)
        self.salButton.place(x=30, y=220)

        self.custButton = customtkinter.CTkButton(self.master,text="Insights", border_width=1,height=40, width=100,font=('Helvetica', 17), command=lambda: self.new_window(
            insights.insights_window))
        self.custButton.place(x=30, y=260)

    def new_window(self, _class):
        self.new = customtkinter.CTk()
        self.app = _class(self.new)
        self.new.mainloop()


def ck_name(n):
    nName = n
    while len(nName) > 20:
        nName = input("Name must be less than 20 characters. Please enter again: ")


def id_gen(t):
    newId = t + shortuuid.ShortUUID().random(length=9)
    if t == 's':
        while (newId in sup):
            newId = t + shortuuid.ShortUUID().random(length=9)
        sup.append(newId)
    if t == 'p':
        while (newId in prod):
            newId = t + shortuuid.ShortUUID().random(length=9)
        prod.append(newId)
    if t == 'c':
        while (newId in cust):
            newId = t + shortuuid.ShortUUID().random(length=9)
        cust.append(newId)
    return newId


def main():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    root = customtkinter.CTk()
    app = loginWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
