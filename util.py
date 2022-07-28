def check_table_type(cell_id):
    # print(cell_id)
    # print(cell_id.count('-'))
    # print("-----------")
    if("D2" in cell_id):
        tableType = "3d"
    elif(cell_id.count('-') == 2 or
         "FVFR" in cell_id):
        tableType = "2d"
    else:
        tableType = "3d"
    return tableType
