import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split


class SmartInventoryManagementSystem:
    def __init__(self, sales_data, stock_data):
        self.sales_data = sales_data
        self.stock_data = stock_data

    def integrate_data(self):
        sales_df = self.sales_data
        stock_df = self.stock_data

        return sales_df, stock_df

    def demand_forecasting(self, sales_df):
        # Perform time series analysis and machine learning algorithms for demand forecasting
        df = sales_df
        # Converts 'date' column to datetime format and subtracts 7 from each date to shift back by week
        df['date'] = pd.to_datetime(df['date']) - pd.to_timedelta(7, unit='d')
        # Filters df to include 'date' and 'sales' and groups data by weekly Mondays (intervals)
        df = df.filter(['date', 'sales']).groupby([pd.Grouper(key='date', freq='W-MON')])

        # Adds new 'shift_sale' column to df, containing 'sales' values shifted by one position (previous week's sales)
        df['shift_sale'] = df['sales'].shift(1)
        # Drops first row of df due to shift operation
        df = df.iloc[1:]
        # Calculates four-week average for 'sales' column and assigns to new column
        df['week_avg'] = self.four_week_avg(df['sales'].tolist())

        # Creates new df 'test' by selecting last 52 rows for testing
        self.test = df.iloc[-52:]
        # Modifies original df by excluding last 52 rows to create a training set
        df = df.iloc[:-52]

        # df is split into feature data 'X' (all columns except 'sales') and target data 'y' ('sales' column)
        X = df.drop('sales', axis=1)
        y = df['sales']
        # Training data 'X' and 'y' are split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
        # SVR model is created to fit the model using the training data, and training it to predict the target 'sales' based on features
        clf = svm.SVR(C = 1, kernel = 'linear', degree = 8, gamma = 'scale', coef0= 10)
        clf.fit(X_train, y_train)
        # Uses trained SVR model to predict 'sales' values for test set 'X_test'
        predictions = clf.predict(X_test)
        # Uses trained model to predict 'sales' values for 'test' df (last 52 weeks)
        self.predictions = clf.predict(self.test.drop('week_sale', axis = 1))

    def four_week_avg(self,sales):
        sum = 0
        week_avg = []
        for i in range(3, -1, -1):
            for j in range(i):
                sum += sales[j]
            if (i != 0):
                week_avg.append(sum/i)
            sum = 0
        week_avg.append(sales[0])
        week_avg.reverse()
        for row in range(len(sales) - 4):
            for row in range(row, row + 4):
                sum += sales[row]
            week_avg.append(sum/4)
            sum = 0
        return week_avg

    def optimize_inventory(self):
        sales_df, stock_df = self.integrate_data()
        self.demand_forecasting(sales_df)

    def getTest(self):
        return self.test.index

    def getPredictions(self):
        return self.predictions

