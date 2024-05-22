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

#schema = database.get_tables()
#foreign_keys = database.get_foreign_keys()
#views = database.get_views()

client = AzureOpenAI(
        api_key=os.getenv("_OPENAI_API_KEY"),  
        api_version="2023-12-01-preview",
        azure_endpoint = os.getenv("_OPENAI_API_BASE")
    )



system_message='''
            You are a data analyst who is an expert in querying a Microsoft System Center Configuration Manager SQL database.
            This is the only data source available to you.
            
    '''
system_message=system_message + "The version of System Center Configuration Manager is : \n" + os.getenv("_CONFIG_MANAGER_VERSION")
system_message=system_message + "\n The current datetime is " + datetime.today().strftime('%Y-%m-%d %H:%M:%S')

messages.append({"role": "system", "content": system_message})

# Example function hard coded to return the same weather
# In production, this could be your backend API or an external API
def query_sccm_database(query):
    print("-------------------------Running Query---------------------------------")
    cprint(query, color="light_blue")
    print("----------------------------------------------------------------")
    return json.dumps(database.execute_query(query))

def clean_message(message):
    return message.replace("\n", "").replace("\r", "")

def run_conversation():
    
    cprint("How can I help you? \n", color='green')
    query = input()
    #query = "get all orders over 200"
    # Step 1: send the conversation and available functions to the model
    messages.append({"role": "user", "content": query})
    tools = [{
            "type": "function",
            "function": {
                "name": "query_sccm_database",
                "description": "Get data from the System Center Configuration Manager SQL Server Database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query used to retrieve data from the System Center Configuration Manager SQL Server Database"
                        }
                    },
                    "required": ["query"],
                },
            },
        },
    ]
    response = client.chat.completions.create(
        model="gpt-35-turbo",
        temperature=0,
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message

    try:
        tool_calls = response_message.tool_calls
    except Exception as e:
        print (e.message)
    
    if not tool_calls:
        print("\n")
        cprint(response_message.content, color='light_blue')
        # print(response_message.content)
        pass

    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "query_sccm_database": query_sccm_database
        }  # only one function in this example, but you can have multiple
        #messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function responswhat e to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            args=clean_message(tool_call.function.arguments)
            function_args = json.loads(args)
            json_string = json.dumps(function_args)
            function_response = function_to_call(json_string)
                
           
            if function_name=="query_sccm_database":
                records=json.dumps(function_response)
                print("-------------------------Output---------------------------------")
                cprint(records, color='blue')
                print("----------------------------------------------------------------")
            else:  # extend conversation with function response

                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
             
                second_response = client.chat.completions.create(
                    model="gpt-35-turbo",
                    messages=messages,
                )  # get a new response from the model where it can see the function response
                print(second_response.choices[0].message.content)

    run_conversation()

run_conversation()