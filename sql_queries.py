import os
import pyodbc
from util import check_table_type
if os.path.exists("env.py"):
    import env


server = os.getenv("PROPHET_SERVER")
db = os.getenv("PROPHET_DATABASE")
username = os.getenv("PROPHET_USERNAME")
password = os.getenv("PROPHET_PASSWORD")
driver = '{ODBC Driver 17 for SQL Server}'

cnx = pyodbc.connect(f'DRIVER={driver};SERVER={server};\
                       DATABASE={db};UID={username};PWD={password}')

cursor = cnx.cursor()


def get_locations():

    # Query gets the location code and location name of all locations that are
    # of zone type "FRIDGE"
    cursor.execute('''
        SELECT
        loczon_nl.zonecode,
        loczon_nl.name
        FROM loczon_nl
        WHERE
        loczon_nl.zonetypecode = 'FRIDGE'
    ''')

    locations = {}
    # Loop uses the location id as the key, and the value is the name
    for row in cursor.fetchall():
        locations[row[0]] = {"name": row[1]}
        tableType = check_table_type(row[0])
        locations[row[0]] = {"name": row[1], "tableType": tableType}
    # Returns:
    # {
    #   "FVFR1":{
    #       "name": "Fruit Veg",
    #       "tableType": "2d"
    #   },
    #   { ... }
    # }

    return locations


def get_table_size(location_id):

    # Query gets all the cell location id's and get the name of the location
    cursor.execute('''
        SELECT
        locfil_nl.loccode,
        loczon_nl.name
        FROM locfil_nl
        LEFT JOIN loczon_nl ON locfil_nl.zonecode = loczon_nl.zonecode
        WHERE
        locfil_nl.zonecode LIKE '{}';
    '''.format(str(location_id)))

    alphabet = "_ABCDEFGHIJK"

    # Value of each dimension is defined before comparison
    loc_racks = 0
    loc_height = 0
    loc_depth = 0
    data = {}

    # Each cell will be broken up and the value of each section will be
    # compared
    for row in cursor.fetchall():
        # Creates a string list seperated by the "-"
        loc = row[0].split('-')

        # Compare rack values
        if(loc_racks < int(loc[1])):
            loc_racks = int(loc[1])

        # Compare height values
        if(loc_height < alphabet.index(loc[2])):
            loc_height = alphabet.index(loc[2])

        # Compare depth values
        if (len(loc) == 4):
            if(loc_depth < int(loc[3])):
                loc_depth = int(loc[3])

        data["name"] = row[1]
        data["cell"] = row[0]
    data["tableSize"] = [loc_racks, loc_height, loc_depth]
    # Returns:
    # {
    #     "id": "FVFR4",
    #     "name": "Fruit and Veg Fridge 4",
    #     "cell": "FVFR4-01-A",
    #     "tableSize": [3, 20, 0]
    # }

    return data


# Query to get pallets currently in store
def get_pallets_by_location(location_id):

    cursor.execute('''
        SELECT
        locfil_nl.loccode,
        loczon_nl.name,
        palstk_nl.recqty,
        res.soldqty
        FROM palstk_nl
        LEFT JOIN palfil_nl ON palstk_nl.palfilid = palfil_nl.palfilid
        LEFT JOIN locdet_nl ON palfil_nl.locdetid = locdet_nl.locdetid
        LEFT JOIN locfil_nl ON locdet_nl.locfilid = locfil_nl.locfilid
        LEFT JOIN loczon_nl ON locfil_nl.zonecode = loczon_nl.zonecode
        LEFT JOIN (
            SELECT
            p1.palstkid,
            ISNULL(SUM(po2.qty),0) AS soldqty,
            ISNULL((p1.recqty-SUM(po2.qty)),p1.recqty) AS balance
            FROM palstk_nl p1
            LEFT OUTER JOIN palord_nl po2 ON po2.palstkid = p1.palstkid
            GROUP BY p1.palstkid, p1.recqty
        ) res ON palstk_nl.palstkid = res.palstkid
        WHERE
        locfil_nl.loccode LIKE '{}%'
        AND
        res.balance != 0
    '''.format(str(location_id)))

    data = {}
    data["loc_id"] = location_id
    data["loc_name"] = ""
    data["pallets"] = []
    for row in cursor.fetchall():
        data["pallets"].append(row[0])

    return data


# Query to get information of each pallet in a location
# There can be mulitple pallets in a single location
def get_pallet_details(location_id):
    cursor.execute('''
        SELECT
        palfil_nl.palfilid,
        prdall_nl.descr,
        spdfil_nl.mark,
        palstk_nl.recqty,
        palstk_nl.BestBeforeDate,
        coufil_nl.name,
        variety_nl.variety,
        lotdet_nl.jobnum,
        sendac_nl.name,
        res.balance,
        locfil_nl.descr,
        lothed_nl.ponum,
        lotdet_nl.lotnum,
        poffil_nl.narrative,
        spdfil_nl.countsize
        FROM palstk_nl
        LEFT JOIN palfil_nl ON palstk_nl.palfilid = palfil_nl.palfilid
        LEFT JOIN locdet_nl ON palfil_nl.locdetid = locdet_nl.locdetid
        LEFT JOIN locfil_nl ON locdet_nl.locfilid = locfil_nl.locfilid
        LEFT JOIN lotdet_nl ON palstk_nl.lotdetid = lotdet_nl.lotdetid
        LEFT JOIN spdfil_nl ON lotdet_nl.prodnum = spdfil_nl.prodnum
        LEFT JOIN prdall_nl ON spdfil_nl.mascode = prdall_nl.mascode
        LEFT JOIN lothed_nl ON lotdet_nl.lotnum = lothed_nl.lotnum
        LEFT JOIN sendac_nl ON lothed_nl.supcode = sendac_nl.supcode
        LEFT JOIN variety_nl ON lotdet_nl.variety = variety_nl.varietycode
        LEFT JOIN coufil_nl ON lotdet_nl.country = coufil_nl.country
        LEFT JOIN poffil_nl ON lothed_nl.ponum = poffil_nl.ponum
        LEFT JOIN (
            SELECT
            p1.palstkid,
            ISNULL(SUM(po2.qty),0) AS soldqty,
            ISNULL((p1.recqty-SUM(po2.qty)),p1.recqty) AS balance
            FROM palstk_nl p1
            LEFT OUTER JOIN palord_nl po2 ON po2.palstkid = p1.palstkid
            GROUP BY p1.palstkid, p1.recqty
        ) res ON palstk_nl.palstkid = res.palstkid
        WHERE
        locfil_nl.loccode LIKE '{}%'
        AND
        res.balance != 0
        ORDER BY palfil_nl.palfilid DESC
    '''.format(str(location_id)))

    pallets = []
    for row in cursor.fetchall():
        pallet = {"palletId": row[0],
                  "productDescr": row[1],
                  "spdfilMark": row[2],
                  "recqty": row[3],
                  "bestBefore": row[4],
                  "country": row[5],
                  "variety": row[6],
                  "jobNum": row[7],
                  "supplierName": row[8],
                  "balence": row[9],
                  "locDescr": row[10],
                  "ponum": row[11],
                  "lotnum": row[12],
                  "narrative": row[13],
                  "countsize": row[14]}
        pallets.append(pallet)

    return pallets

# def query_to_dict(cursor):
