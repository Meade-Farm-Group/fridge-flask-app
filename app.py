from flask import Flask, render_template
import sql_queries

app = Flask(__name__)

alphabet = "_ABCDEFGHIJK"


@app.route("/")
@app.route("/home")
def home_page():

    # QUERY CALL ( Get ALL location id and names for display )
    locations = sql_queries.get_locations()

    return render_template('index.html', locations=locations)


@app.route('/location/<string:location_id>/', defaults={'rack_id': None},
           methods=['POST', 'GET'])
@app.route('/location/<string:location_id>/<string:rack_id>',
           methods=['POST', 'GET'])
def location_page(location_id, rack_id):

    # QUERY CALL ( Get the dimensions for the table )
    data = sql_queries.get_table_size(location_id)

    locdet = {
        "id": location_id,
        "short_id": location_id,
        "name": data["name"],
        "tableSize": data["tableSize"],
    }

    if "FVFR" in location_id:
        html_loc = "location2d.html"
    # "DIS2" OR "ST1"
    elif "DIS" in location_id or "ST" in location_id:
        html_loc = "location3d.html"
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


@app.route('/update_data/<string:location_id>', methods=['POST'])
def update_data(location_id):
    data = sql_queries.get_pallets_by_location(location_id)
    return data


@app.route("/palletInfo/<string:pallet_location_id>")
def palletInfo_page(pallet_location_id):

    # QUERY CALL ( get all info of all pallets in a single location )
    pallets = sql_queries.get_pallet_details(pallet_location_id)

    return render_template(
        'palletInfo.html',
        pallets=pallets,
        pallet_location_id=pallet_location_id)


@app.errorhandler(404)
def error_404(e):
    return render_template('errors/404.html'), 404


if __name__ == "__main__":

    app.run(debug=True)
