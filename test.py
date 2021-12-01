import os
import pyodbc
if os.path.exists("env.py"):
    import env
import sql_queries
import json


server = os.getenv("PROPHET_SERVER")
db = os.getenv("PROPHET_DATABASE")
username = os.getenv("PROPHET_USERNAME")
password = os.getenv("PROPHET_PASSWORD")
driver = '{ODBC Driver 17 for SQL Server}'

cnx = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={db};\
                       UID={username};PWD={password}')

cursor = cnx.cursor()

# data = queries.get_pallets_by_location("FVST")

# print(data["pallets"])

# for loc in data["pallets"]:
#     if("FVFR1-09-A" in loc):
#         print("Exists")
#     else:
#         print("Not Exists")

# for row in test.fetchall():
#     print(row)
# print(cursor)
# print(cursor.description)

# my_list = {}
# for row in cursor.fetchall():
#     my_list[str(row[0])] = {
#         "supcode": row[1]
#     }
# print(row)
# print(my_list)

# print(my_list[]['supcode'])

# for key, value in my_list["pallets"].items():
#     for row in value:
#         print(va)

# print(my_list.keys())
# print(my_list)

# with open('locationDetails.json') as json_file:
#     data = json.load(json_file)

# locdet = data["FVFR1"]

# print(locdet["tableSize"][0])

# cursor.execute('''
#         SELECT
#         locfil_nl.loccode,
#         prdall_nl.descr,
#         palfil_nl.palfilid,
#         palstk_nl.recqty,
#         res.soldqty,
#         res.balance
#         FROM palstk_nl
#         LEFT JOIN palfil_nl ON palstk_nl.palfilid = palfil_nl.palfilid
#         LEFT JOIN locdet_nl ON palfil_nl.locdetid = locdet_nl.locdetid
#         LEFT JOIN locfil_nl ON locdet_nl.locfilid = locfil_nl.locfilid
#         LEFT JOIN lotdet_nl ON palstk_nl.lotdetid = lotdet_nl.lotdetid
#         LEFT JOIN spdfil_nl ON lotdet_nl.prodnum = spdfil_nl.prodnum
#         LEFT JOIN prdall_nl ON spdfil_nl.mascode = prdall_nl.mascode
#         LEFT JOIN (
#             SELECT
#             p1.palstkid,
#             ISNULL(SUM(po2.qty),0) AS soldqty,
#             ISNULL((p1.recqty-SUM(po2.qty)),p1.recqty) AS balance
#             FROM palstk_nl p1
#             LEFT OUTER JOIN palord_nl po2 ON po2.palstkid = p1.palstkid
#             GROUP BY p1.palstkid, p1.recqty
#         ) res ON palstk_nl.palstkid = res.palstkid
#         WHERE
#         locfil_nl.loccode LIKE '{}%'
#         AND
#         res.balance != 0
#     '''.format(str(location_id)))

# def test_call():
#     cursor.execute("""
#         SELECT
#         palstk_nl.recqty,
#         palfil_nl.palfilid,
#         locdet_nl.locfilid,
#         locfil_nl.loccode,
#         prdall_nl.descr
#         FROM palstk_nl
#         LEFT JOIN palfil_nl ON palstk_nl.palfilid = palfil_nl.palfilid
#         LEFT JOIN locdet_nl ON palfil_nl.locdetid = locdet_nl.locdetid
#         LEFT JOIN locfil_nl ON locdet_nl.locfilid = locfil_nl.locfilid
#         LEFT JOIN lotdet_nl ON palstk_nl.lotdetid = lotdet_nl.lotdetid
#         LEFT JOIN spdfil_nl ON lotdet_nl.prodnum = spdfil_nl.prodnum
#         LEFT JOIN prdall_nl ON spdfil_nl.mascode = prdall_nl.mascode
#         WHERE
#         locfil_nl.loccode LIKE 'FVFR1%';
#     """)

# def test_call2(location_id):
#     location_id = "DIS2"
#     cursor.execute('''
#         SELECT
#         locfil_nl.loccode
#         FROM locfil_nl
#         WHERE
#         locfil_nl.zonecode LIKE '{}';
#     '''.format(str(location_id)))

#     for row in cursor.fetchall():
#         print(row)

# def get_table_size_test(location_id):

#     cursor.execute('''
#         SELECT TOP 1
#         locfil_nl.loccode
#         FROM locfil_nl
#         WHERE
#         locfil_nl.loccode LIKE '{}%'
#         ORDER BY locfil_nl.loccode DESC;
#     '''.format(str(location_id)))

#     for row in cursor.fetchall():
#         print(row[0])

data = sql_queries.get_pallets_by_location("D2-01")

print(data)


# if (rack%2 == 0){
#                 // If rack is even, run this
#             }else{
#                 // If rack is odd, run this
#             }
#             var table = document.getElementById("myTable");
#             for (var i = 0, row; row = table.rows[i]; i++) {
#                 for (var j = 1, col; col = row.cells[j]; j++) {
#                     console.log(col)
#                     //replaceCellId(col, data, rack, i, j);
#                     //cellUpdate(col, data);
#                 }
#             }
