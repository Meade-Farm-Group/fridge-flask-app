import os
import pyodbc
if os.path.exists("env.py"):
    import env
import sql_queries
import json
from util import check_table_type


server = os.getenv("PROPHET_SERVER")
db = os.getenv("PROPHET_DATABASE")
username = os.getenv("PROPHET_USERNAME")
password = os.getenv("PROPHET_PASSWORD")
driver = '{ODBC Driver 17 for SQL Server}'

cnx = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={db};\
                       UID={username};PWD={password}')

cursor = cnx.cursor()

# for key, value in my_list["pallets"].items():
#     for row in value:
#         print(va)

# with open('locationDetails.json') as json_file:
#     data = json.load(json_file)

# data = sql_queries.get_pallet_details_search("Sugraone", "81766",
#                                              "2158-0129", None)
data = sql_queries.get_pallet_details("D2-BAY-9")
print(data)
# Using readlines()
# file1 = open('test.txt', 'r')
# Lines = file1.readlines()
# # Strips the newline character
# for line in Lines:
#     print('"'+line.strip()+'": "#",')
