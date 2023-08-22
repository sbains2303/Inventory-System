from tkinter.ttk import Treeview
import customtkinter

from my_module import main
from my_module.connection import sql_query

def find_Sup(s):
    find_sup_query ="""SELECT SupplierID 
                         FROM Supplier 
                         WHERE Name=%s"""
    rows = sql_query(find_sup_query, [s])
    if len(rows) == 0:
        nID = main.id_gen(s)
        return nID
    else: return rows[0]

class supplier_window:

    def __init__(self, master):
        self.master = master
        self.master.geometry("780x400")
        self.master.title("Supplier")
        self.label = customtkinter.CTkLabel(self.master, text="Suppliers", font=('Helvetica', 20, 'bold'))
        self.label.place(x=340, y=5)

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
        self.fill_table()

        self.upl = customtkinter.CTkLabel(self.master, text="Add a Supplier: ", text_color="white",
                                          font=('Helvetica', 14, 'bold'))
        self.upl.place(x=440, y=50)

        self.dl = customtkinter.CTkLabel(self.master, text="Name:")
        self.dl.place(x=460, y=80)
        self.dlbutton = customtkinter.CTkEntry(self.master)
        self.dlbutton.place(x=610, y=80)

        self.prl = customtkinter.CTkLabel(self.master, text="Product Name: ")
        self.prl.place(x=460, y=120)
        products = sql_query('SELECT NAME FROM Products', [])
        self.suppo = customtkinter.CTkOptionMenu(self.master, values=products, command=None)
        self.suppo.place(x=610, y=120)

        self.addb = customtkinter.CTkButton(self.master, text="Add supplier", width=200,
                                            command=lambda: self.addSale())
        self.addb.place(x=440, y=160)

        self.ldel = customtkinter.CTkLabel(self.master, text="Delete a supplier: ", font=('Helvetica', 14, 'bold'))
        self.ldel.place(x=440, y=210)

        self.idl = customtkinter.CTkLabel(self.master, text="Supplier ID:")
        self.idl.place(x=460, y=250)

        self.iden = customtkinter.CTkEntry(self.master)
        self.iden.place(x=610, y=250)

        self.butdel = customtkinter.CTkButton(self.master, text="Delete supplier", width=200)
        self.butdel.place(x=440, y=290)

    def addSale(self):
        product = sql_query('SELECT ProductID FROM Products WHERE Name=%s', [self.suppo.get()])
        product_list = [row[0] for row in product]
        variables = []
        variables.append(main.id_gen('s'))
        variables.append(self.dlbutton.get())
        placeholder = ', '.join(['%s'] * len(product_list))
        query = f"INSERT INTO Supplier VALUES (%s,%s,{placeholder})"
        parameters = variables + product_list
        sql_query(query, parameters)
        self.fill_table()

    def delPurchase(self):
        sql_query('DELETE FROM Supplier WHERE SupplierID=%s', [self.iden.get()])
        self.fill_table()

    def fill_table(self):
        for item in self.trv.get_children():
            self.trv.delete(item)
        query_variables = []
        rData = sql_query('SELECT * FROM Supplier', query_variables)
        for row in rData:
            self.trv.insert("", 'end', iid=row[0], text=row[0],
                            values=(row[0], row[1], row[2], row[3]))

