from tkinter.ttk import Treeview
import customtkinter

from my_module.connection import sql_query
import main


class purchases_window:

    def __init__(self, master):
        self.master = master
        self.master.geometry("780x400")
        self.master.title("Purchases")
        self.label = customtkinter.CTkLabel(self.master, text="Purchases", font=('Helvetica', 20, 'bold'))
        self.label.place(x=340, y=5)

        self.trv = Treeview(self.master, selectmode='browse')
        self.trv.grid(row=1, column=1, padx=50, pady=80)
        self.trv.configure(height=20)

        self.trv["columns"] = ("1", "2", "3", "4", "5")
        self.trv['show'] = 'headings'

        self.trv.column("1", width=130, anchor='c')
        self.trv.column("2", width=110, anchor='c')
        self.trv.column("3", width=110, anchor='c')
        self.trv.column("4", width=110, anchor='c')
        self.trv.column("5", width=110, anchor='c')

        self.trv.heading("1", text="Order ID")
        self.trv.heading("2", text="Date")
        self.trv.heading("3", text="Supplier ID")
        self.trv.heading("4", text="Product ID")
        self.trv.heading("5", text="Purchase")
        self.fill_table()

        self.upl = customtkinter.CTkLabel(self.master, text="Add a purchase: ", text_color="white",
                                          font=('Helvetica',14,'bold'))
        self.upl.place(x=440, y=50)

        self.dl = customtkinter.CTkLabel(self.master, text="Date (e.g. 1992-02-10):")
        self.dl.place(x=460, y=80)
        self.dlbutton = customtkinter.CTkEntry(self.master)
        self.dlbutton.place(x=610, y=80)

        self.suppl = customtkinter.CTkLabel(self.master, text="Supplier Name: ")
        self.suppl.place(x=460, y=120)
        suppliers = sql_query('Select Name FROM Supplier',[])
        self.suppo = customtkinter.CTkOptionMenu(self.master, values=suppliers, command=None)
        self.suppo.place(x=610, y=120)

        self.prl = customtkinter.CTkLabel(self.master, text="Product Name: ")
        self.prl.place(x=460, y=160)
        products = sql_query('SELECT NAME FROM Products', [])
        self.suppo = customtkinter.CTkOptionMenu(self.master, values=products, command=None)
        self.suppo.place(x=610, y=160)

        self.lpurch = customtkinter.CTkLabel(self.master, text="Purchase: ")
        self.lpurch.place(x=460, y=200)
        self.epurch = customtkinter.CTkEntry(self.master)
        self.epurch.place(x=610, y=200)

        self.addb = customtkinter.CTkButton(self.master, text="Add purchase", width=200, command=lambda : self.addPurchase())
        self.addb.place(x=440, y=240)

        self.ldel = customtkinter.CTkLabel(self.master, text="Delete a purchase: ", font=('Helvetica', 14, 'bold'))
        self.ldel.place(x=440, y=280)

        self.idl = customtkinter.CTkLabel(self.master, text="Order ID:")
        self.idl.place(x=460, y=320)

        self.iden = customtkinter.CTkEntry(self.master)
        self.iden.place(x=610, y=320)

        self.butdel = customtkinter.CTkButton(self.master, text="Delete purchase", width =200)
        self.butdel.place(x=440, y=360)

    def fill_table(self):
        for item in self.trv.get_children():
            self.trv.delete(item)
        query_variables = []
        rData = sql_query('SELECT OrderID,Date,SupplierID,ProductID,Purchase FROM Purchases', query_variables)
        for row in rData:
            self.trv.insert("", 'end', iid=row[0], text=row[0],
                            values=(row[0], row[1], row[2], row[3], row[4]))

    def addPurchase(self):
        supplier = sql_query('SELECT SupplierID FROM Supplier WHERE Name=%s',[self.suppo.get()])
        supplier_list = [row[0] for row in supplier]
        product = sql_query('SELECT ProductID FROM Products WHERE Name=%s',[self.suppo.get()])
        product_list = [row[0] for row in product]
        variables = []
        variables.append(main.id_gen('o'))
        variables.append(self.dlbutton.get())
        last = [(self.epurch.get())]
        placeholdersone = ', '.join(['%s'] * len(supplier_list))
        placeholderstwo = ', '.join(['%s'] * len(product_list))
        query =f"INSERT INTO Purchases VALUES (%s,%s,{placeholdersone},{placeholderstwo})"
        parameters = variables + supplier_list + product_list + last
        sql_query(query, parameters)
        self.fill_table()

    def delPurchase(self):
        sql_query('DELETE FROM Purchases WHERE OrderID=%s',[self.iden.get()])
        self.fill_table()


