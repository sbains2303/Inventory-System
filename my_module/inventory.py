from tkinter.ttk import Treeview
import customtkinter
from my_module.connection import sql_query


class inventory_window:
    def __init__(self, master):
        self.master = master
        self.master.geometry("630x400")
        self.master.title("Inventory")
        self.label = customtkinter.CTkLabel(self.master, text="Inventory", font=('Helvetica',20,'bold'))
        self.label.place(x=280, y=9)

        self.trv = Treeview(self.master, selectmode='browse')
        self.trv.grid(row=1, column=1, padx=50, pady=100)
        self.trv.configure(height=20)
        self.trv["columns"] = ("1", "2", "3", "4")
        self.trv['show'] = 'headings'

        self.trv.column("1", width=110, anchor='c')
        self.trv.column("2", width=110, anchor='c')
        self.trv.column("3", width=110, anchor='c')
        self.trv.column("4", width=110, anchor='c')

        self.trv.heading("1", text="Product ID")
        self.trv.heading("2", text="Quantity")
        self.trv.heading("3", text="Incoming")
        self.trv.heading("4", text="Outgoing")
        self.fill_table()

        self.idl = customtkinter.CTkLabel(self.master, text="Update product details ", text_color="white", font=('Helvetica',14,'bold'))
        self.idl.place(x=360, y=60)

        self.idl = customtkinter.CTkLabel(self.master, text="Product ID: ", text_color="white")
        self.idl.place(x=380, y=100)
        self.id = customtkinter.CTkEntry(self.master)
        self.id.place(x=460, y=100)

        self.qul = customtkinter.CTkLabel(self.master, text="Quantity: ")
        self.qul.place(x=380, y=140)
        self.quantity = customtkinter.CTkEntry(self.master)
        self.quantity.place(x=460, y=140)

        self.inl = customtkinter.CTkLabel(self.master, text="Incoming: ")
        self.inl.place(x=380, y=180)
        self.inco = customtkinter.CTkEntry(self.master)
        self.inco.place(x=460, y=180)

        self.oul = customtkinter.CTkLabel(self.master, text="Outgoing: ")
        self.oul.place(x=380, y=220)
        self.outgo = customtkinter.CTkEntry(self.master)
        self.outgo.place(x=460, y=220)

        self.change_button = customtkinter.CTkButton(self.master, text="Change product", width=8, command= self.update_sql)
        self.change_button.place(x=480, y=290)

    def update_sql(self):
        change_query = ('UPDATE Inventory SET Quantity=%s, Incoming=%s, Outgoing=%s WHERE ProductID=%s')
        query_variables = []
        query_variables.append(self.quantity.get())
        query_variables.append(self.inco.get())
        query_variables.append(self.outgo.get())
        query_variables.append(self.id.get())

        sql_query(change_query, query_variables)
        self.fill_table()

    def fill_table(self):
        for item in self.trv.get_children():
            self.trv.delete(item)
        query_variables = []
        rData = sql_query('SELECT * FROM Inventory', query_variables)
        for row in rData:
            self.trv.insert("", 'end', iid=row[0], text=row[0],
                       values=(row[0], row[1], row[2], row[3]))
