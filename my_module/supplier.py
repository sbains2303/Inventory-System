from my_module import main
from my_module.connection import sql_query


def find_Sup(s):
    find_sup_query ="""SELECT SupplierID 
                         FROM Supplier 
                         WHERE Name=%s"""
    rows = sql_query(find_sup_query, [s])
    if len(rows) == 0:
        nID = main.id_gen(s)
        return nID
    else: return rows[0]