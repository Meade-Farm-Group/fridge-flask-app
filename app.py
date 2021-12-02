from flask import Flask, render_template
import sql_queries
from util import check_table_type

app = Flask(__name__)

alphabet = "_ABCDEFGHIJK"


@app.route("/")
@app.route("/home")
def home_page():

    # Query call to get all locations
    locations = sql_queries.get_locations()

    return render_template('index.html', locations=locations)


# Route takes in a location id string and may take in a rack id string.
# If no rack id is provided, it will have a default value of None
@app.route('/location/<string:location_id>/', defaults={'rack_id': None},
           methods=['POST', 'GET'])
@app.route('/location/<string:location_id>/<string:rack_id>',
           methods=['POST', 'GET'])
def location_page(location_id, rack_id):

    # Query to get the dimensions for the table
    data = sql_queries.get_table_size(location_id)

    if("ST" in location_id):
        cells_per_bay = 2
    elif("DIS" in location_id):
        cells_per_bay = 3
    else:
        cells_per_bay = 1
    tableType = check_table_type(location_id)
    locdet = {
        "id": location_id,  # Id of the location
        "tableType": tableType,  # How table will render
        "name": data["name"],  # Full name of the location
        "tableSize": data["tableSize"],  # Table dimensions
        "cellsPerBay": cells_per_bay  # How many cells until a break
    }

    return render_template('location.html',
                           alphabet=alphabet,
                           locdet=locdet,
                           rack_id=rack_id)


@app.route('/location/<string:location_id>/<string:rack_id>',
           methods=['POST', 'GET'])
def rack_change(location_id, rack_id):
    return render_template('location3d.html')


# Routing used to refresh the data for the tables
@app.route('/update_data/<string:location_id>', methods=['POST'])
def update_data(location_id):
    data = sql_queries.get_pallets_by_location(location_id)
    return data


@app.route("/palletInfo/<string:cell_id>")
def palletInfo_page(cell_id):

    # Query to get all information of pallets in this location
    pallets = sql_queries.get_pallet_details(cell_id)

    return render_template('palletInfo.html',
                           pallets=pallets,
                           cell_id=cell_id
                           )


@app.errorhandler(404)
def error_404(e):
    return render_template('errors/404.html'), 404


if __name__ == "__main__":

    app.run(debug=True)
