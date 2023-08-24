import tkinter as tk

import customtkinter
import shortuuid

import insights
import inventory
import products
import purchases
import sales
from my_module import supplier


# Initialize lists to store IDs for different entities
prod, sup, cust, ords = [], [], [], []


# WelcomeWindow class for the initial window
class WelcomeWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x300")
        self.master.title('Welcome')
        self.master.configure(bg="#DBDBDB")

        tk.Frame(self.master)

        customtkinter.CTkLabel(self.master, text="Inventory Management System",
                               font=('Helvetica', 30, 'bold')).place(x=25, y=40)
        customtkinter.CTkLabel(self.master, text="Click below to continue to the main menu", text_color="#006400",
                               font=('Helvetica', 18, 'bold')).place(x=80, y=150)
        customtkinter.CTkButton(self.master, text="Continue",
                                fg_color="#006400", command=self.new_window).place(x=175, y=200)

    def new_window(self):
        self.master.withdraw()
        self.master = customtkinter.CTk()
        self.app = MainPage(self.master)
        self.master.mainloop()


# MainPage class for the main menu
class MainPage:
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x320")
        self.master.title("Main Menu")

        customtkinter.CTkLabel(self.master, text="Inventory Management System",
                               font=('Helvetica', 20, 'bold')).place(x=60, y=20)

        button_params = [
            ("Inventory", 300, 60, inventory.InventoryWindow),
            ("Products", 260, 100, products.products_window),
            ("Suppliers", 220, 140, supplier.SupplierWindow),
            ("Purchases", 180, 180, purchases.purchases_window),
            ("Sales", 140, 220, sales.SalesWindow),
            ("Insights", 100, 260, insights.InsightsWindow)
        ]

        customtkinter.CTkLabel(
            self.master,
            text="Inventory Management System",
            font=('Helvetica', 20, 'bold')
        ).place(x=60, y=20)

        for text, width, y, command in button_params:
            customtkinter.CTkButton(
                self.master,
                text=text,
                border_width=1,
                height=40,
                width=width,
                font=('Helvetica', 17),
                command=lambda cmd=command: self.new_window(cmd)
            ).place(x=30, y=y)

    def new_window(self, _class):
        self.new = customtkinter.CTk()
        self.app = _class(self.new)
        self.new.mainloop()


# Function to check and limit the length of a name
def check_name(n):
    n_name = n
    while len(n_name) > 20:
        n_name = input("Name must be less than 20 characters. Please enter again: ")


# Function to generate a unique ID based on a type
def id_gen(t):
    new_id = t + shortuuid.ShortUUID().random(length=9)
    if t == 's':
        while new_id in sup:
            new_id = t + shortuuid.ShortUUID().random(length=9)
        sup.append(new_id)
    if t == 'p':
        while new_id in prod:
            new_id = t + shortuuid.ShortUUID().random(length=9)
        prod.append(new_id)
    if t == 'c':
        while new_id in cust:
            new_id = t + shortuuid.ShortUUID().random(length=9)
        cust.append(new_id)
    if t == 'o':
        while new_id in ords:
            new_id = t + shortuuid.ShortUUID().random(length=9)
        ords.append(new_id)
    return new_id


# Entry point of the application
def main():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    root = customtkinter.CTk()
    app = WelcomeWindow(root)
    root.mainloop()

# Check script is run as main program
if __name__ == '__main__':
    main()
