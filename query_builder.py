import os
from pprint import pprint
from openai import AzureOpenAI
import json
from datetime import datetime
from termcolor import colored, cprint
import database

import models

messages=[]

database = database.Database(
        server=os.getenv("_SERVER"),  
        database=os.getenv("_DATABASE"),
        user = os.getenv("_USERNAME"),
        password = os.getenv("_PASSWORD")
    )

#tables = database.tables
#foreign_keys = database.foreign_keys
views = database.views

client = AzureOpenAI(
        api_key=os.getenv("_OPENAI_API_KEY"),  
        api_version=os.getenv("_OPENAI_API_VERSION"),
        azure_endpoint = os.getenv("_OPENAI_API_BASE")
)
system_message='''

You are an Microsoft System Center database analyst.  
Microsoft Endpoint Configuration Manager, formerly known as System Center Configuration Manager (SCCM), 
is a Windows-centric endpoint management tool used to manage devices within an Active Directory domain. 
SCCM is backed by a SQL Server Database that you can query to learn more about devices in great detail.
The SCCM database contains tables and views, but you will be using only views for this task.

You will be given the contents of a views.json file that contains details of all database views with fields and a datatype for each field.

views.json contains a collection of views that lists the view's name and the list of fields in each view with their corresponding name.
In the views file, each field also has a type that specifies the datatype of the field.
Here is a small snippet from that file that shows the structure.
{
	"views": [
		{
			"name": "v_PeerSourceRejectionData",
			"fields": [
				{
					"name": "StatusTime",
					"type": "datetime"
				},
				{
					"name": "TotalMemberCount",
					"type": "int"
				},
				{
					"name": "OverallStatusProtectedCount",
					"type": "int"
				}
			]
		}
	]
}

Your task is to suggest a SQL query that can be used by the user to get the requested data. 
You will only return JSON output.

The JSON output will contain 2 keys: sql and comments.

If you have trouble generating a query, please share your thoughts in the comments section only and do not include a SQL query.

Here is an example of the expected JSON output:
{
    "sql": "SELECT * FROM table_name",
    "comments": "Any additional comments or suggestions"
}

Here is an example of the expected JSON output if you are not sure or need more information to generate a query:
{
    "sql": "",
    "comments": "I am not sure about that, can you ask that in a different way?"
}

Your task will be completed by following these steps in order.
Step1. Analyze the views.json file to get a good understanding of the views and fields available.
Step2. Take the time to undertand all the fields for each view and their data types.
Step3. Take the time needed to understand the user's request.
Step4. Make an initial decision on a potential query you could recommend to the user and store this in memory.
Step5. Take your initial query and ensure you have not missed any detail or made any errors by evaluating it against the views.json file. 
Step6. Based on your additonal analysis, you will fix any errors.
Step7. You will present your final query to the user in JSON format.
'''
system_message=system_message + "Here is views.json  \n" + views
messages.append({"role": "system", "content": system_message})

def execute(query:str):
    
    cprint(">_ "+query, color='blue')
    # Step 1: send the conversation and available functions to the model
    messages.append({"role": "user", "content": query})
   
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=messages,
        response_format={"type": "json_object"}
    )
    response_message = response.choices[0].message
    if response_message is not None:
        cprint(response_message.content, color='cyan')
    #print(response_message)



