def check_table_type(cell_id):
    if (cell_id.count('-') == 2 or
            "FVFR" in cell_id or
            "STF" in cell_id or
            "DIS1" in cell_id):
        tableType = "2d"
    else:
        tableType = "3d"
    return tableType
