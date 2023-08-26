import customtkinter
from ai import SmartInventoryManagementSystem
from my_module.connection import sql_query, py_conn
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class InsightsWindow:

    def __init__(self, master):
        self.master = master
        self.master.geometry("600x400")
        self.master.title("Insights")

        self.label = customtkinter.CTkLabel(self.master, text="Insights", font=('Helvetica',20,'bold'))
        self.label.place(x=260, y=5)
        self.chlabel = customtkinter.CTkLabel(self.master, text="Type product name below:", font=('Helvetica',14,'bold'))
        self.chlabel.place(x=30, y=50)

        self.product = customtkinter.CTkEntry(self.master)
        self.product.place(x=30, y=80)

        self.button = customtkinter.CTkButton(self.master, command=lambda: self.getProduct(), text="Show")
        self.button.place(x=30, y=120)

    def getProduct(self):
        variable = []
        variable.append(self.product.get())
        self.id = sql_query('SELECT ProductID FROM Products WHERE Name=%s', variable)
        rid = [row[0] for row in self.id]
        if rid:
            product_id=rid[0]
            self.callai(product_id)

    def callai(self, productID):
        sales_data = py_conn(0, productID)  # Replace with actual sales data file name
        print(sales_data)
        stock_data = py_conn(1, productID)  # Replace with actual stock data file name
        inventory_management_system = SmartInventoryManagementSystem(sales_data, stock_data)
        inventory_management_system.optimize_inventory()
        self.test = inventory_management_system.getTest()
        self.predictions = inventory_management_system.getPredictions()

        # Create a Matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6))

        plt.figure(figsize=(10, 6))
        # 'test.index' represents the time axis
        plt.plot(self.test.index, self.test['sales'], label='Actual Sales')
        plt.plot(self.test.index, self.predictions, label='Predicted Sales', linestyle='dashed')
        plt.xlabel('Time')
        plt.ylabel('Sales')
        plt.title('Actual vs Predicted Sales')
        plt.legend()
        plt.tick_params(axis='x', rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=50, y=20)
