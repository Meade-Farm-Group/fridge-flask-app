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

# function replaceCellId(col, data, rack, i, j) {
#     var cell = document.getElementById(col.id) //Cell Html object
#     var cell_id = cell.getAttribute("cell-id"); // Getting the Id of the cell
#     var col_link = col.getElementsByClassName("cell-link")[0];
#     var newId = data["loc_id"] +"-"+ cell_id;
#     col_link.innerHTML = "<div> Cell " + rack +"-"+ cell_id+"</div>";
#     col_link.href="/palletInfo/"+newId;
#     cell.setAttribute("id", newId);
# }

# data = sql_queries.get_pallets_by_location("FVFR1")
data = sql_queries.get_pallets_by_location("D2-01")

print(data)
