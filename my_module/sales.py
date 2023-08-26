from tkinter.ttk import Treeview
import customtkinter

from my_module import main
from my_module.connection import sql_query

class SalesWindow:
    def __init__(self, master):
        self.master = master
        master.geometry("780x400")
        master.title("Sales")

        self.create_title_label()
        self.create_treeview()
        self.create_add_sale_section()
        self.create_delete_sale_section()
        self.fill_table()

    # Create title label for Sales window
    def create_title_label(self):
        label = customtkinter.CTkLabel(self.master, text="Sales", font=('Helvetica', 20, 'bold'))
        label.place(x=340, y=5)

    # Create Treeview widget to display sales table
    def create_treeview(self):
        self.trv = Treeview(self.master, selectmode='browse')
        self.trv.grid(row=1, column=1, padx=50, pady=80)
        self.trv.configure(height=20)
        self.trv["columns"] = ("1", "2", "3", "4")
        self.trv['show'] = 'headings'

        columns = [("1", "Order ID"), ("2", "Date"), ("3", "Product ID"), ("4", "Sale")]
        for col_id, col_name in columns:
            self.trv.column(col_id, width=130 if col_id == "1" else 110, anchor='c')
            self.trv.heading(col_id, text=col_name)

    # Inputs for adding new sale
    def create_add_sale_section(self):
        add_sale_label = customtkinter.CTkLabel(
            self.master,
            text="Add a Sale:",
            text_color="white",
            font=('Helvetica', 14, 'bold')
        )
        add_sale_label.place(x=440, y=50)

        customtkinter.CTkLabel(self.master, text="Date (e.g. 1992-02-10):").place(x=460, y=80)
        self.date_entry = customtkinter.CTkEntry(self.master)
        self.date_entry.place(x=610, y=80)

        customtkinter.CTkLabel(self.master, text="Product Name:").place(x=460, y=120)
        products = sql_query('SELECT NAME FROM Products', [])
        prod = [row[0] for row in products]
        self.product_option_menu = customtkinter.CTkOptionMenu(self.master, values=prod)
        self.product_option_menu.place(x=610, y=120)

        customtkinter.CTkLabel(self.master, text="Sale:").place(x=460, y=160)
        self.sale_entry = customtkinter.CTkEntry(self.master)
        self.sale_entry.place(x=610, y=160)

        add_button = customtkinter.CTkButton(
            self.master,
            text="Add sale",
            width=200,
            command=self.add_sale
        )
        add_button.place(x=440, y=200)

    # Inputs for deleting a sale
    def create_delete_sale_section(self):
        delete_sale_label = customtkinter.CTkLabel(
            self.master,
            text="Delete a sale:",
            font=('Helvetica', 14, 'bold')
        )
        delete_sale_label.place(x=440, y=240)

        customtkinter.CTkLabel(self.master, text="Order ID:").place(x=460, y=280)
        self.order_id_entry = customtkinter.CTkEntry(self.master)
        self.order_id_entry.place(x=610, y=280)

        delete_button = customtkinter.CTkButton(
            self.master,
            text="Delete sale",
            width=200,
            command=self.del_sale
        )
        delete_button.place(x=440, y=320)

    # Sale is added to table in MySQL
    def add_sale(self):
        product = sql_query('SELECT ProductID FROM Products WHERE Name=%s', [self.product_option_menu.get()])
        product_list = [row[0] for row in product]
        variables = [
            main.id_gen('o'),
            self.date_entry.get(),
        ]
        last = [self.sale_entry.get()]
        placeholder = ', '.join(['%s'] * len(product_list))
        query = f"INSERT INTO Sales VALUES (%s,%s,{placeholder},%s)"
        parameters = variables + product_list + last
        sql_query(query, parameters)
        self.fill_table()

    # Sale is deleted from table in MySQL
    def del_sale(self):
        sql_query('DELETE FROM Sales WHERE OrderID=%s', [self.order_id_entry.get()])
        self.fill_table()

    # Table is updated with any new records from sales table
    def fill_table(self):
        for item in self.trv.get_children():
            self.trv.delete(item)
        query_variables = []
        rData = sql_query('SELECT * FROM Sales', query_variables)
        for row in rData:
            self.trv.insert("", 'end', iid=row[0], text=row[0], values=(row[0], row[1], row[2], row[3]))

if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    app = SalesWindow(root)
    root.mainloop()

