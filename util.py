def check_table_type(loc_id):
    if (loc_id.count("-") == 2):
        tableType = "2d"
    else:
        tableType = "3d"

    return tableType
