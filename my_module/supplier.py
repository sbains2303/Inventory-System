from tkinter.ttk import Treeview
import customtkinter
from my_module import main
from my_module.connection import sql_query


class SupplierWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry("780x400")
        self.master.title("Supplier")

        customtkinter.CTkLabel(self.master, text="Suppliers", font=('Helvetica', 20, 'bold')).place(x=340, y=5)

        # Treeview widget to display supplier information
        self.create_treeview()
        self.fill_table()

        self.setup_supplier_form()
        self.setup_delete_supplier()

    # Method to create Treeview widget
    def create_treeview(self):
        self.trv = Treeview(self.master, selectmode='browse')
        self.trv.grid(row=1, column=1, padx=50, pady=80)
        self.trv.configure(height=20)

        self.trv["columns"] = ("1", "2", "3")
        self.trv['show'] = 'headings'

        self.trv.column("1", width=180, anchor='c')
        self.trv.column("2", width=200, anchor='c')
        self.trv.column("3", width=180, anchor='c')

        self.trv.heading("1", text="Supplier ID")
        self.trv.heading("2", text="Name")
        self.trv.heading("3", text="Product ID")

    # Method for adding a supplier
    def setup_supplier_form(self):
        customtkinter.CTkLabel(self.master, text="Add a Supplier: ", text_color="white",
                               font=('Helvetica', 14, 'bold')).place(x=440, y=50)
        customtkinter.CTkLabel(self.master, text="Name:").place(x=460, y=80)

        self.dlbutton = customtkinter.CTkEntry(self.master)
        self.dlbutton.place(x=610, y=80)

        customtkinter.CTkLabel(self.master, text="Product Name: ").place(x=460, y=120)
        products = sql_query('SELECT NAME FROM Products', [])
        self.suppo = customtkinter.CTkOptionMenu(self.master, values=products, command=None)
        self.suppo.place(x=610, y=120)

        customtkinter.CTkButton(self.master, text="Add supplier", width=200, command=self.add_supplier).place(x=440,
                                                                                                              y=160)

    # Method for deleting a supplier
    def setup_delete_supplier(self):
        customtkinter.CTkLabel(self.master, text="Delete a supplier: ", font=('Helvetica', 14, 'bold')).place(x=440,
                                                                                                              y=210)
        customtkinter.CTkLabel(self.master, text="Supplier ID:").place(x=460, y=250)

        self.iden = customtkinter.CTkEntry(self.master)
        self.iden.place(x=610, y=250)

        customtkinter.CTkButton(self.master, text="Delete supplier", width=200, command=self.delete_supplier).place(
            x=440, y=290)

    # Method to add supplier to MySQL database
    def add_supplier(self):
        product = sql_query('SELECT ProductID FROM Products WHERE Name=%s', [self.suppo.get()])
        product_list = [row[0] for row in product]
        variables = [main.id_gen('s'), self.dlbutton.get()]
        placeholder = ', '.join(['%s'] * len(product_list))
        query = f"INSERT INTO Supplier VALUES (%s,%s,{placeholder})"
        parameters = variables + product_list
        sql_query(query, parameters)
        self.fill_table()

    # Method to delete supplier from database
    def delete_supplier(self):
        sql_query('DELETE FROM Supplier WHERE SupplierID=%s', [self.iden.get()])
        self.fill_table()

    # Method to fill Treeview widget with supplier data
    def fill_table(self):
        for item in self.trv.get_children():
            self.trv.delete(item)
        rData = sql_query('SELECT * FROM Supplier', [])
        for row in rData:
            self.trv.insert("", 'end', iid=row[0], text=row[0], values=(row[0], row[1], row[2], row[3]))

