import customtkinter
import pandas as pd
from ai import SmartInventoryManagementSystem
from my_module.connection import sql_query, py_conn
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class InsightsWindow:

    def __init__(self, master):
        self.master = master
        self.master.geometry("800x600")
        self.master.title("Insights")

        # Create and place labels and entry widget
        self.label = customtkinter.CTkLabel(self.master, text="Insights", font=('Helvetica', 20, 'bold'))
        self.label.place(x=350, y=5)

        self.create_label("Type product name below:", 30, 50,'white')
        self.product = customtkinter.CTkEntry(self.master)
        self.product.place(x=30, y=80)
        self.create_button("Show", self.getProduct, 30, 120)

    # Creating label in customertkinter
    def create_label(self, text, x, y,colour):
        customtkinter.CTkLabel(self.master, text=text, font=('Helvetica', 14, 'bold'),text_color=colour).place(x=x, y=y)

    # Creating button in customtkinter
    def create_button(self, text, command, x, y):
        customtkinter.CTkButton(self.master, command=command, text=text).place(x=x, y=y)

    # Get product id and call ai for sales calculations
    def getProduct(self):
        product_name = self.product.get()
        product_id = self.get_product_id(product_name)
        if product_id:
            self.call_ai(product_id)

    # Retrieves product id from MySQL database
    def get_product_id(self, product_name):
        result = sql_query('SELECT ProductID FROM Products WHERE Name=%s', [product_name])
        return result[0][0] if result else None

    # Creates new inventory_management_system instance and gets predictions values
    def call_ai(self, product_id):
        sales_data = py_conn(0, product_id)  # Replace with actual sales data file name
        stock_data = py_conn(1, product_id)  # Replace with actual stock data file name

        inventory_management_system = SmartInventoryManagementSystem(sales_data, stock_data)
        inventory_management_system.optimize_inventory()
        self.test = inventory_management_system.getTest()
        self.predictions = inventory_management_system.getPredictions()
        self.test['predicted_week_avg'] = self.predictions

        # Create a Matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 5))

        # Ensure the date format in 'self.test' index matches the date format used in 'start_date' and 'end_date'
        self.test.index = pd.to_datetime(self.test.index)

        plt.xlim(self.test.index.min(), self.test.index.max())
        plt.ylim(0, 80)

        plt.xlabel('Week in Year')
        plt.ylabel('Sales')
        plt.title('Actual vs Predicted Sales')
        plt.tick_params(axis='x', rotation=45)
        plt.plot(self.test.index, self.test['week_avg'], label='Actual Sales')
        plt.plot(self.test.index, self.test['predicted_week_avg'], label='Predicted Sales', linestyle='dashed')

        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.config(width=800, height=800)
        canvas_widget.place(x=350, y=80)

        self.create_label("Solid line = Actual sales", 30, 220,'light blue')
        self.create_label("Dashed line = Predicted sales", 30, 240, 'orange')
        self.create_label("derived from previous sales", 30, 260, 'orange')
