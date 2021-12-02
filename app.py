from flask import Flask, render_template
import sql_queries

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

    locdet = {
        "id": location_id,  # Id of the location
        "short_id": location_id,  # Shortened id that is used for the cell id
        "name": data["name"],  # Full name of the location
        "tableSize": data["tableSize"],  # Table dimensions
    }

    # If the location is "Fruit Veg", or a location that only cares about
    # height and rack
    if "FVFR" in location_id:
        html_loc = "location2d.html"

    # If the location is "Dispatch" or "Starch", or a location that cares about
    # height, rack and depth
    elif "DIS" in location_id or "ST" in location_id:
        html_loc = "location3d.html"

        # get the first and last char of the location id and change it to the
        # shortened version
        locdet["short_id"] = location_id[0] + location_id[-1]
    else:
        return render_template('errors/404.html'), 404

    return render_template(html_loc,
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


@app.route("/palletInfo/<string:pallet_location_id>")
def palletInfo_page(pallet_location_id):

    # Query to get all information of pallets in this location
    pallets = sql_queries.get_pallet_details(pallet_location_id)

    return render_template('palletInfo.html',
                           pallets=pallets,
                           pallet_location_id=pallet_location_id)


@app.errorhandler(404)
def error_404(e):
    return render_template('errors/404.html'), 404


if __name__ == "__main__":

    app.run(debug=True)
