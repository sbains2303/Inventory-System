from tkinter.ttk import Treeview
import customtkinter

from my_module import main
from my_module.connection import sql_query
import my_module
import supplier

def create_prod():
    id = my_module.main.id_gen('p')
    name = str(input("Enter product name: "))
    my_module.main.check_name(name)
    price = float(input("Enter the unit price: "))
    sName = str("Enter supplier name: ")
    supID = supplier.find_Sup(sName)

    create_prod_query = """INSERT INTO Products(ProductID, Name, UnitPrice, SupplierID) VALUES (%s,%s,%d,%s)"""
    sql_query(create_prod_query, [id,name,price,supID])


class products_window:

    def __init__(self, master):
        self.master = master
        self.master.geometry("630x400")
        self.master.title("Products")
        self.label = customtkinter.CTkLabel(self.master, text="Products", font=('Helvetica',20,'bold'))
        self.label.place(x=280, y=5)

        self.trv = Treeview(self.master, selectmode='browse')
        self.trv.grid(row=1, column=1, padx=50, pady=80)
        self.trv.configure(height=20)
        self.trv["columns"] = ("1", "2", "3", "4")
        self.trv['show'] = 'headings'

        self.trv.column("1", width=130, anchor='c')
        self.trv.column("2", width=110, anchor='c')
        self.trv.column("3", width=110, anchor='c')
        self.trv.column("4", width=110, anchor='c')

        self.trv.heading("1", text="Product ID")
        self.trv.heading("2", text="Name")
        self.trv.heading("3", text="Unit price")
        self.trv.heading("4", text="Supplier ID")
        self.fill_table()

        self.idl = customtkinter.CTkLabel(self.master, text="Update unit price: ", text_color="white",
                                          font=('Helvetica', 14, 'bold'))
        self.idl.place(x=360, y=50)

        self.idl = customtkinter.CTkLabel(self.master, text="Product ID ", text_color="white")
        self.idl.place(x=380, y=80)
        self.ido = customtkinter.CTkEntry(self.master)
        self.ido.place(x=460, y=80)

        self.prl = customtkinter.CTkLabel(self.master, text="Unit price")
        self.prl.place(x=380, y=120)
        self.entp = customtkinter.CTkEntry(self.master)
        self.entp.place(x=460, y=120)

        self.change_button = customtkinter.CTkButton(self.master, text="Change product",command=lambda: self.update_sql(1))
        self.change_button.place(x=360, y=160)

        self.ldel = customtkinter.CTkLabel(self.master, text="Delete product from inventory:", font=('Helvetica', 14, 'bold'))
        self.ldel.place(x=360, y=200)

        self.idl = customtkinter.CTkLabel(self.master, text="Product ID ", text_color="white")
        self.idl.place(x=380, y=230)
        self.idt = customtkinter.CTkEntry(self.master)
        self.idt.place(x=460, y=230)

        self.change_button = customtkinter.CTkButton(self.master, text="Delete product", command= lambda: self.update_sql(2))
        self.change_button.place(x=360, y=270)

        self.change_button = customtkinter.CTkButton(self.master, text="Add product",width=200, command= lambda: self.newProductWindow())
        self.change_button.place(x=360, y=350)

    def update_sql(self, option):
        query_variables = []
        if (option == 1):
            change_query = ('UPDATE Products SET UnitPrice=%s WHERE ProductID=%s')
            query_variables.append(self.entp.get())
            query_variables.append(self.ido.get())
        else:
            change_query = ('DELETE FROM Products WHERE ProductID=%s')
            query_variables.append(self.idt.get())

        sql_query(change_query, query_variables)
        self.fill_table()

    def fill_table(self):
        for item in self.trv.get_children():
            self.trv.delete(item)
        query_variables = []
        rData = sql_query('SELECT * FROM Products', query_variables)
        for row in rData:
            self.trv.insert("", 'end', iid=row[0], text=row[0],
                       values=(row[0], row[1], row[2], row[3]))

    def newProductWindow(self):
        self.new = customtkinter.CTk()
        self.new.geometry("400x350")
        self.new.title("Product addition")

        self.labeln = customtkinter.CTkLabel(self.new, text="Fill product details:", font=('Helvetica', 14, 'bold'))
        self.labeln.place(x=40, y=20)

        self.namel = customtkinter.CTkLabel(self.new, text="Name")
        self.namel.place(x=60 , y=60)

        self.name = customtkinter.CTkEntry(self.new)
        self.name.place(x= 150, y=60)

        self.pricel = customtkinter.CTkLabel(self.new, text="Unit price")
        self.pricel.place(x=60, y=100)

        self.price = customtkinter.CTkEntry(self.new)
        self.price.place(x=150, y=100)

        self.newid = my_module.main.id_gen('p')
        self.suppliers = sql_query('SELECT Name FROM Supplier',[])

        self.optionl = customtkinter.CTkLabel(self.new, text="Supplier")
        self.optionl.place(x=60, y=140)


        self.option = customtkinter.CTkOptionMenu(self.new, values=self.suppliers)
        self.option.place(x=150, y =140)

        self.addb = customtkinter.CTkButton(self.new, text="Add product", command=lambda: addProduct())
        self.addb.place(x=60, y=180)

        self.sup = customtkinter.CTkLabel(self.new, text="Add with new supplier:", font=('Helvetica', 14, 'bold'))
        self.sup.place(x=40, y=230)

        self.optiont = customtkinter.CTkLabel(self.new, text="New supplier")
        self.optiont.place(x=60, y=270)

        self.opt = customtkinter.CTkEntry(self.new)
        self.opt.place(x=150, y =270)

        self.nsup = customtkinter.CTkButton(self.new, text="Add supplier and product")
        self.nsup.place(x=60, y=310)


        def addProduct():
            result = sql_query('SELECT SupplierID FROM Supplier WHERE Name=%s',[self.option.get()])
            result_list = [row[0] for row in result]
            variables = []
            variables.append(self.newid)
            variables.append(self.name.get())
            variables.append(int(self.price.get()))
            placeholders = ', '.join(['%s'] * len(result_list))
            query =f"INSERT INTO Products VALUES (%s,%s,%s,{placeholders})"
            parameters = variables + result_list
            sql_query(query,parameters)
            self.fill_table()

        def addSup():
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

        self.new.mainloop()