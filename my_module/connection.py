import mysql
from mysql.connector import connect
import pymysql
import pandas as pd


def py_conn(choice, id):
    connection = pymysql.connect(
        host="localhost",
        user='root',
        password='root',
        database="inventory",
    )
    # pycursor = connection.cursor()
    if (choice == 0):
        df = pd.read_sql_query(sql="SELECT Date,Sale FROM Sales WHERE ProductID=%s",params=[id],con=connection)
    else:
        df = pd.read_sql_query(sql='SELECT Date,Purchase FROM Purchases WHERE ProductID=%s', params=[id], con=connection)
    return df

def sql_query(query, variables):
    conn = mysql.connector.connect(
            host="localhost",
            user='root',
            password='root',
            database="inventory",
        )
    cursor = conn.cursor()

    if len(variables) == 1:
        cursor.execute(query, (variables[0],))
        if query.strip().upper().startswith('SELECT'):
            data = cursor.fetchall()
            return data
    if len(variables) == 2: cursor.execute(query, (variables[0], variables[1],))
    if len(variables) == 3: cursor.execute(query, (variables[0], variables[1], variables[2]), )
    if len(variables) == 4: cursor.execute(query, (variables[0], variables[1], variables[2], variables[3]), )
    if len(variables) == 5: cursor.execute(query, (variables[0], variables[1], variables[2], variables[3], variables[4]), )
    if len(variables) == 6: cursor.execute(query, (variables[0], variables[1], variables[2], variables[3], variables[4], variables[5]), )

    conn.commit()

    if query.strip().upper().startswith('SELECT') & (len(variables) == 0):
        cursor.execute(query)
        data = cursor.fetchall()
        return data


    conn.close()
    cursor.close()