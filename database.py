import pyodbc
import json
import time
from typing import List
from dataclasses import dataclass
import ast
import jsonlines


@dataclass
class Field:
    name: str
    type: str
    def tojson(self):
        return {
            "name": self.name,
            "type": self.type
        }

@dataclass
class Table:
    name: str
    fields: List[Field]
    def tojson(self):
        return {
            "name": self.name,
            "fields": [field.tojson() for field in self.fields]
        }
@dataclass
class Tables:
    tables: List[Table]
    def tojson(self):
        return {
            "tables": [table.tojson() for table in self.tables]
        }
   

@dataclass
class View:
    name: str
    fields: List[Field]
    def tojson(self):
        return {
            "name": self.name,
            "fields": [field.tojson() for field in self.fields]
        }
@dataclass
class Views:
    views: List[View]
    def tojson(self):
        return {
            "views": [view.tojson() for view in self.views]
        }


class Database:
    def __init__(self, server, database, user, password):
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.table_file="schema_details/tables.json"
        self.views_file="schema_details/views.json"
        self.foreign_keys_file="schema_details/foreign_keys.txt"
        self.tables=self.get_tables()
        self.views=self.get_views() 
        self.foreign_keys=self.get_foreign_keys()


    def __str__(self):
        return f"I'm {self.database} database on {self.server} server"
    

    def connectionstring(self):
        return f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.user};PWD={self.password};Encrypt=no;TrustServerCertificate=no;Connection Timeout=30;'

    def get_tables(self) -> str:

        cached_data=read_text_from_file(self.table_file)
        if cached_data:
            return cached_data
        else:

            conn = pyodbc.connect(self.connectionstring())
            cursor = conn.cursor()
            
            query = """SELECT t.TABLE_NAME AS TableName, c.COLUMN_NAME AS ColumnName, c.DATA_TYPE as DataType FROM INFORMATION_SCHEMA.TABLES t INNER JOIN INFORMATION_SCHEMA.COLUMNS c ON t.TABLE_NAME = c.TABLE_NAME WHERE c.TABLE_SCHEMA='dbo' and t.TABLE_TYPE = 'BASE TABLE' AND t.TABLE_CATALOG=""" + "'" + self.database + "' GROUP BY t.TABLE_NAME, c.COLUMN_NAME, c.DATA_TYPE"
            
            print (query)
            cursor.execute(query)
            tables_list= []

            table_name=""
            if tables := cursor.fetchall():
                for row in tables:
                    
                    if table_name!=row[0]:
                        table_name=row[0]
                        try:
                            if len(fields)>0:
                                tables_list.append(Table(table_name,fields))
                        except:
                            pass
                        fields=[]
                    else:
                        column0=row[0]
                        column1=row[1]
                        column2=row[2]
                        f=Field(column1,column2)
                        fields.append(f)
                        
                
                ts=Tables(tables_list)
                    
                table_str=str(ts.tojson())
                json_str=str(table_str).replace("'", '"')

                conn.close()

                write_table_schema(self,json_str)
                return json_str

            else:
                conn.close()
                return None
            
    def get_views(self) -> str:
        
        cached_data=read_text_from_file(self.views_file)
        if cached_data:
            return cached_data
        else:
            

            conn = pyodbc.connect(self.connectionstring())
            cursor = conn.cursor()
            
            query = """SELECT v.TABLE_NAME AS ViewName, c.COLUMN_NAME AS ColumnName, c.DATA_TYPE as DataType FROM INFORMATION_SCHEMA.VIEWS v INNER JOIN INFORMATION_SCHEMA.COLUMNS c ON v.TABLE_NAME = c.TABLE_NAME WHERE v.TABLE_NAME LIKE 'v_GS_%' and c.TABLE_SCHEMA='dbo' AND c.TABLE_CATALOG=""" + "'" + self.database + "'" 
                        
            print (query)
            cursor.execute(query)
            views_list= []

            view_name=""
            if views := cursor.fetchall():
                for row in views:
                    
                    if view_name!=row[0]:
                        view_name=row[0]
                        try:
                            if len(fields)>0:
                                views_list.append(View(view_name,fields))
                        except:
                            pass
                        fields=[]
                    else:
                        column0=row[0]
                        column1=row[1]
                        column2=row[2]
                        f=Field(column1,column2)
                        fields.append(f)
                        
                
                vs=Views(views_list)
                    
                view_str=str(vs.tojson())
                json_str=str(view_str).replace("'", '"')

                conn.close()

                write_view(self,json_str)
                return json_str
            else:
                conn.close()
                return None
            
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
       
    

    



    def get_foreign_keys(self) -> str:

        cached_data=read_text_from_file(self.foreign_keys_file)
        if cached_data:
            return cached_data
        else:
        
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
                    write_foreign_key(self,f"fk___{key[0]}___{key[1]}___{key[2]}___{key[3]}")
                
                conn.close()
                read_text_from_file(self.foreign_keys_file)

            else:
                conn.close()
                return None

def write_view(database,txt):
    append_text_to_file(database.views_file, txt)

def write_foreign_key(database,txt):
    append_text_to_file(database.foreign_keys_file, txt)

def write_table_schema(database,txt):
    append_text_to_file(database.table_file, txt)

def append_text_to_file(filename, txt):
    with open(filename, 'a') as file:
        file.write(txt + '\n')

def write_jsonl_file(filename,json_data):
    with open(filename +'l', 'w') as jsonl_output:
        for entry in json_data:
            json.dump(entry, jsonl_output)
            jsonl_output.write('\n')

def read_text_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except:
        return None
    
   