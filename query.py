import os
import json
import pyodbc
import database

database = database.Database(
        server=os.getenv("_SERVER"),  
        database=os.getenv("_DATABASE"),
        user = os.getenv("_USERNAME"),
        password = os.getenv("_PASSWORD")
    )

def get_data(query: str):
    
    query = """SELECT ResourceID,Hardware_ID0,Virtual_Machine_Host_Name0
                    FROM v_R_System
                    WHERE Operating_System_Name_and0 LIKE '%Windows%'"""
    
    records=database.execute_query(query)

    for r in records:
        print(f"{r.ResourceID}\t{r.Hardware_ID0}\t{r.Virtual_Machine_Host_Name0}")

    # print(content)
    #return content

get_data("")
