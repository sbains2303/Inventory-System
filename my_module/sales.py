from tkinter.ttk import Treeview
import customtkinter

from my_module import main
from my_module.connection import sql_query


class sales_window:

    def __init__(self, master):
        self.master = master
        self.master.geometry("780x400")
        self.master.title("Sales")
        self.label = customtkinter.CTkLabel(self.master, text="Sales", font=('Helvetica', 20, 'bold'))
        self.label.place(x=340, y=5)

        self.trv = Treeview(self.master, selectmode='browse')
        self.trv.grid(row=1, column=1, padx=50, pady=80)
        self.trv.configure(height=20)

        self.trv["columns"] = ("1", "2", "3", "4")
        self.trv['show'] = 'headings'

        self.trv.column("1", width=130, anchor='c')
        self.trv.column("2", width=110, anchor='c')
        self.trv.column("3", width=110, anchor='c')
        self.trv.column("4", width=110, anchor='c')

        self.trv.heading("1", text="Order ID")
        self.trv.heading("2", text="Date")
        self.trv.heading("3", text="Product ID")
        self.trv.heading("4", text="Sale")
        self.fill_table()

        self.upl = customtkinter.CTkLabel(self.master, text="Add a Sale: ", text_color="white",
                                          font=('Helvetica', 14, 'bold'))
        self.upl.place(x=440, y=50)

        self.dl = customtkinter.CTkLabel(self.master, text="Date (e.g. 1992-02-10):")
        self.dl.place(x=460, y=80)
        self.dlbutton = customtkinter.CTkEntry(self.master)
        self.dlbutton.place(x=610, y=80)

        self.prl = customtkinter.CTkLabel(self.master, text="Product Name: ")
        self.prl.place(x=460, y=120)
        products = sql_query('SELECT NAME FROM Products', [])
        self.suppo = customtkinter.CTkOptionMenu(self.master, values=products, command=None)
        self.suppo.place(x=610, y=120)

        self.lpurch = customtkinter.CTkLabel(self.master, text="Sale: ")
        self.lpurch.place(x=460, y=160)
        self.epurch = customtkinter.CTkEntry(self.master)
        self.epurch.place(x=610, y=160)

        self.addb = customtkinter.CTkButton(self.master, text="Add sale", width=200,
                                            command=lambda: self.addSale())
        self.addb.place(x=440, y=200)

        self.ldel = customtkinter.CTkLabel(self.master, text="Delete a sale: ", font=('Helvetica', 14, 'bold'))
        self.ldel.place(x=440, y=240)

        self.idl = customtkinter.CTkLabel(self.master, text="Order ID:")
        self.idl.place(x=460, y=280)

        self.iden = customtkinter.CTkEntry(self.master)
        self.iden.place(x=610, y=280)

        self.butdel = customtkinter.CTkButton(self.master, text="Delete sale", width=200)
        self.butdel.place(x=440, y=320)

    def addSale(self):
        product = sql_query('SELECT ProductID FROM Products WHERE Name=%s', [self.suppo.get()])
        product_list = [row[0] for row in product]
        variables = []
        variables.append(main.id_gen('o'))
        variables.append(self.dlbutton.get())
        last = [(self.epurch.get())]
        placeholder = ', '.join(['%s'] * len(product_list))
        query = f"INSERT INTO Sales VALUES (%s,%s,{placeholder},%s)"
        parameters = variables + product_list + last
        sql_query(query, parameters)
        self.fill_table()

    def delPurchase(self):
        sql_query('DELETE FROM Sales WHERE OrderID=%s', [self.iden.get()])
        self.fill_table()

    def fill_table(self):
        for item in self.trv.get_children():
            self.trv.delete(item)
        query_variables = []
        rData = sql_query('SELECT * FROM Sales', query_variables)
        for row in rData:
            self.trv.insert("", 'end', iid=row[0], text=row[0],
                            values=(row[0], row[1], row[2], row[3]))