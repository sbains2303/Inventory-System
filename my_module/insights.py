import customtkinter
from ai import start_ai
from my_module.connection import sql_query

class insights_window:

    def __init__(self, master):
        self.master = master
        self.master.geometry("600x400")
        self.master.title("Insights")

        self.label = customtkinter.CTkLabel(self.master, text="Insights", font=('Helvetica',20,'bold'))
        self.label.place(x=260, y=5)
        self.chlabel = customtkinter.CTkLabel(self.master, text="Choose a product below:", font=('Helvetica',14,'bold'))
        self.chlabel.place(x=30, y=50)


        def callai():
            start_ai(self.rid)

        self.products = sql_query('SELECT Name FROM Products', [])
        self.product = customtkinter.CTkOptionMenu(self.master, values=self.products, command = callai)
        self.product.place(x=30, y=80)

        self.id = sql_query('SELECT ProductID FROM Products WHERE Name=%s',[self.product.get()])
        self.rid = [row[0] for row in self.id]



