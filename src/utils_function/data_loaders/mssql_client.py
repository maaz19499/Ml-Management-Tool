# Importing the necessary libraries
import numpy as np
import pyodbc
import pandas as pd

    # Creating SQL engine
def mssql_engine(server, database, user_name, password):

        port = 1433
        try:
            cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+user_name+';PWD='+password)
        except:
            raise ConnectionError("It seems there is some issue with sql connection, just check your credentials")
        return (cnxn)
    
