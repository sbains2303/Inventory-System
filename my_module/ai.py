import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split


class SmartInventoryManagementSystem:
    def __init__(self, sales_data, stock_data):
        self.sales_data = sales_data
        self.stock_data = stock_data

    def integrate_data(self):
        # Combine sales and stock data, if needed
        return self.sales_data, self.stock_data

    def demand_forecasting(self, sales_df):
        # Time series analysis and machine learning for demand forecasting

        # Preprocessing sales data
        df = sales_df
        df['Date'] = pd.to_datetime(df['Date']) - pd.to_timedelta(7, unit='d')
        df = df[['Date', 'Sale']]  # Select relevant columns

        # Create a shifted column for previous week's sales
        df['shift_sale'] = df['Sale'].shift(1)

        # Group data by weekly intervals (Mondays) and aggregate sales
        df = df.groupby([pd.Grouper(key='Date', freq='W-MON')]).agg({'Sale': 'sum', 'shift_sale': 'sum'})

        # Remove the first row (due to the shift operation) and calculate a four-week average
        df = df.iloc[1:]
        df['week_avg'] = self.four_week_avg(df['Sale'].tolist())

        # Create a test dataset with the last 26 weeks and a training dataset
        self.test = df.iloc[-26:]
        df = df.iloc[:-26]

        # Split data into features 'X' (excluding 'Sale') and target 'y' ('Sale')
        X = df.drop('Sale', axis=1)
        y = df['Sale']

        # Split the training data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create and train the Support Vector Regression (SVR) model
        clf = svm.SVR(C=1, kernel='linear', degree=8, gamma='scale', coef0=10)
        clf.fit(X_train, y_train)

        # Make predictions for the test dataset
        self.test = self.test.drop('Sale', axis=1)  # Prepare the test data
        self.predictions = clf.predict(self.test)

    def four_week_avg(self, sales):
        # Calculate a four-week average

        sum = 0
        week_avg = []

        # Calculate the average for the last 4 weeks
        for i in range(3, -1, -1):
            for j in range(i):
                sum += sales[j]
            if (i != 0):
                week_avg.append(sum / i)
            sum = 0

        week_avg.append(sales[0])
        week_avg.reverse()

        # Calculate the average for the remaining weeks
        for row in range(len(sales) - 4):
            for row in range(row, row + 4):
                sum += sales[row]
            week_avg.append(sum / 4)
            sum = 0

        return week_avg

    def optimize_inventory(self):
        sales_df, stock_df = self.integrate_data()
        self.demand_forecasting(sales_df)

    def getTest(self):
        # Get the test dataset (last 26 weeks)
        return self.test

    def getPredictions(self):
        # Get the predictions made by the model
        return self.predictions

