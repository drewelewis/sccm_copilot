import pyodbc
import json
import time

class Database:
    def __init__(self, server, database, user, password):
        self.server = server
        self.database = database
        self.user = user
        self.password = password    


    def __str__(self):
        return f"I'm {self.database} database on {self.server} server"

    def connectionstring(self):
        return f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.user};PWD={self.password};Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;'

    def execute_query(self, query):
        obj=json.loads(query)
        query=obj['query']
        conn = pyodbc.connect(self.connectionstring())
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            if records := cursor.fetchall():
                conn.close()
                return records
            else:
                conn.close()
                return None
            
        except Exception as e:
            print(e)
            return None
       
    
    def get_tables(self):
        
        conn = pyodbc.connect(self.connectionstring())
        cursor = conn.cursor()
        
        query = """SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='dbo' and TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG=""" + "'" + self.database + "'"
        
        print (query)
        cursor.execute(query)
        if tables := cursor.fetchall():
            for table in tables:
                table = table[0]
                query = f"SELECT TOP 1 * FROM {table}"
                #print (query)
                cursor.execute(query)
                rows = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                # Loop through the list
                write_table_schema (table)
                for tup in cursor.description:
                    # Print the first and second values
                    write_table_schema(f"{tup[0]}: {tup[1].__name__}")
                write_table_schema ("")


            conn.close()

        else:
            conn.close()
            return None
    
    def get_views(self):
        
        conn = pyodbc.connect(self.connectionstring())
        cursor = conn.cursor()
        
        query = """SELECT v.TABLE_NAME AS ViewName, c.COLUMN_NAME AS ColumnName FROM INFORMATION_SCHEMA.VIEWS v INNER JOIN INFORMATION_SCHEMA.COLUMNS c ON v.TABLE_NAME = c.TABLE_NAME WHERE c.TABLE_SCHEMA='dbo' AND c.TABLE_CATALOG=""" + "'" + self.database + "'" 
                    

        print (query)
        cursor.execute(query)
        view_name=""
        if views := cursor.fetchall():
            for view in views:
                if view_name!=view[0]:
                    write_view ("")
                    view_name=view[0]
                    write_view(f"{view_name}")
                
                write_view(f"{view[1]}")


            conn.close()

        else:
            conn.close()
            return None


    def get_foreign_keys(self):

        conn = pyodbc.connect(self.connectionstring())
        cursor = conn.cursor()
        
        query = """SELECT 
                    OBJECT_NAME (f.referenced_object_id) AS "ReferenceTable", 
                    COL_NAME(fc.referenced_object_id, fc.referenced_column_id) AS "ReferenceColumn",
                    OBJECT_NAME(f.parent_object_id) AS "ParentTable", 
                    COL_NAME(fc.parent_object_id, fc.parent_column_id) AS "ParentColumn"
                FROM 
                    sys.foreign_keys AS f 
                INNER JOIN 
                    sys.foreign_key_columns AS fc ON f.OBJECT_ID = fc.constraint_object_id
                """
        
        print (query)
        cursor.execute(query)
        if keys := cursor.fetchall():
            for key in keys:
                write_foreign_key(f"fk___{key[0]}___{key[1]}___{key[2]}___{key[3]}")
            conn.close()

        else:
            conn.close()
            return None

def write_view(txt):
    append_text_to_file("schema_details/views.txt", txt)

def write_foreign_key(txt):
    append_text_to_file("schema_details/foreign_keys.txt", txt)

def write_table_schema(txt):
    append_text_to_file("schema_details/schema.txt", txt)

def append_text_to_file(filename, txt):
    with open(filename, 'a') as file:
        file.write(txt + '\n')
