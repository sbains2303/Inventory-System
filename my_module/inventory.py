from tkinter.ttk import Treeview
import customtkinter
from my_module.connection import sql_query


class InventoryWindow:
    def __init__(self, master):
        self.master = master
        master.geometry("630x400")
        master.title("Inventory")

        self.label = customtkinter.CTkLabel(
            master, text="Inventory", font=('Helvetica', 20, 'bold')).place(x=280, y=9)

        # Treeview widget to display inventory table
        self.trv = Treeview(master, selectmode='browse', height=20)
        self.trv.grid(row=1, column=1, padx=50, pady=100)
        self.trv["columns"] = ("1", "2", "3", "4")
        self.trv['show'] = 'headings'

        columns = [("1", "Product ID"), ("2", "Quantity"), ("3", "Incoming"), ("4", "Outgoing")]
        for col_id, col_name in columns:
            self.trv.column(col_id, width=110, anchor='c')
            self.trv.heading(col_id, text=col_name)

        # Fill table with inventory data
        self.fill_table()

        self.id_label = customtkinter.CTkLabel(
            master, text="Update product details ", text_color="white", font=('Helvetica', 14, 'bold')
        )
        self.id_label.place(x=360, y=60)

        customtkinter.CTkLabel(master, text="Product ID: ", text_color="white").place(x=380, y=100)
        self.id = customtkinter.CTkEntry(master)
        self.id.place(x=460, y=100)

        customtkinter.CTkLabel(master, text="Quantity: ").place(x=380, y=140)
        self.quantity = customtkinter.CTkEntry(master)
        self.quantity.place(x=460, y=140)

        customtkinter.CTkLabel(master, text="Incoming: ").place(x=380, y=180)
        self.inco = customtkinter.CTkEntry(master)
        self.inco.place(x=460, y=180)

        customtkinter.CTkLabel(master, text="Outgoing: ").place(x=380, y=220)
        self.outgo = customtkinter.CTkEntry(master).place(x=460, y=220)

        customtkinter.CTkButton(
            master, text="Change product", width=8, command=self.update_sql).place(x=480, y=290)

    # Method to update product details in inventory table
    def update_sql(self):
        change_query = 'UPDATE Inventory SET Quantity=%s, Incoming=%s, Outgoing=%s WHERE ProductID=%s'
        query_variables = [self.quantity.get(), self.inco.get(), self.outgo.get(), self.id.get()]

        sql_query(change_query, query_variables)
        self.fill_table()

    # Method to fill Treeview widget
    def fill_table(self):
        for item in self.trv.get_children():
            self.trv.delete(item)

        query_variables = []
        rData = sql_query('SELECT * FROM Inventory', query_variables)

        for row in rData:
            self.trv.insert(
                "", 'end', iid=row[0], text=row[0], values=(row[0], row[1], row[2], row[3])
            )


# Application window is created and program is run
if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    app = InventoryWindow(root)
    root.mainloop()
