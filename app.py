from flask import Flask, render_template, flash, redirect, url_for, request
import sql_queries
from util import check_table_type
import json
import os
if os.path.exists("env.py"):
    import env
from waitress import serve
from forms import SearchForm

app = Flask(__name__)

alphabet = "_ABCDEFGHIJK"

app.config['SECRET_KEY'] = 'ojou9823o2f82uye9foj2e8f9hu'


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
    tableType = ""
    # Query to get the dimensions for the table
    data = sql_queries.get_table_size(location_id)

    # File that contains the spacing required between cells
    # No data in db to determine this, so it must be hard coded
    with open('cellsPerBay.json') as json_file:
        data2 = json.load(json_file)

    # Check to see if location exists in file
    if(location_id in data2):
        cells_per_bay = data2[location_id]
    else:
        # If no location found, use default value
        cells_per_bay = 1

    # Check if the url is valid
    # If there is no cell locations or bays in this location, then it
    # does not exist, or not implemented yet
    if data['cell'] is None and len(data['bays']) == 0:
        return render_template('errors/locationNotExist.html'), 404
    # if a cell is present, then it will not be None
    if data['cell'] is not None:
        # Structure of the cell id will determine the storage type
    tableType = check_table_type(data["cell"])
        # If the cell id has 3 values for cell location
    if(tableType == "3d"):
            # If the id given exceeds the number of racks in location,
            # it is invalid
            if int(rack_id) > data["tableSize"][0]:
                return render_template('errors/locationNotExist.html'), 404
        # If the cell id does not have 3 values
    else:
            # 2d storages should not have a rack Id, so if one is provided,
            # invalid data
            if rack_id is not None:
                return render_template('errors/locationNotExist.html'), 404

    # Storing values in json object for easier data management
    locdet = {
        "id": location_id,  # Id of the location
        "tableType": tableType,  # How table will render
        "name": data["name"],  # Full name of the location
        "tableSize": data["tableSize"],  # Table dimensions
        "cellsPerBay": cells_per_bay,  # How many cells until break
        "bays": data["bays"]
    }

    return render_template('location.html',
                           alphabet=alphabet,
                           locdet=locdet,
                           rack_id=rack_id)


# Routing used to refresh the data for the tables
@app.route('/update_data/<string:location_id>', methods=['POST'])
def update_data(location_id):
    data = sql_queries.get_pallets_by_location(location_id)
    return data


@app.route("/palletInfo/<string:cell_id>")
def palletInfo_page(cell_id):

    # Query to get all information of pallets in this location
    data = sql_queries.get_pallet_details(cell_id)

    if data["zonecode"] is None:
        return render_template('errors/palletNotExist.html'), 404

    return render_template('palletInfo.html',
                           data=data,
                           cell_id=cell_id)


@app.route('/palletInfo/<string:cell_id>/loading')
def loading_model(cell_id):
    return render_template("loading.html", cell_id=cell_id)


@app.route('/search', methods=['POST', 'GET'])
def search_page():
    form = SearchForm()
    if form.validate_on_submit():
        r = form.reference.data
        if r == '':
            r = None

        return redirect(url_for('search_result_page',
                                pc=form.product_name.data,
                                po=form.purchase_order.data,
                                r=r, bbd=form.best_before_date.data))
    else:
        print("INVALID")
    return render_template('search.html', form=form)


@app.route('/search/results')
def search_result_page():
    pc = request.args.get("pc")
    po = request.args.get("po")
    r = request.args.get("r")
    bbd = request.args.get("bbd")
    data = sql_queries.get_pallet_details_search(pc, po, r, bbd)
    # if data["pallets"].count == 0:
    #     return redirect(url_for('search_page'))
    return render_template("searchResults.html", data=data)


@app.route('/search/loading')
def search_loading_page():
    return render_template("searchLoading.html")


@app.route('/map')
def map_page():
    return render_template("map.html")


@app.route('/detailedMap/<string:location_id>')
def location_detailed_page(location_id):
    return render_template("detailedMap.html")


@app.errorhandler(404)
def error_404(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(503)
def error_503(e):
    return render_template('errors/503.html'), 503


if "PRODUCTION" in os.environ:
    serve(app, listen="*:7014")
else:
    if __name__ == "__main__":
        app.run(debug=True)
