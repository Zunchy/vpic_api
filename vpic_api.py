import logging
from flask import Flask, url_for, jsonify
from sqlalchemy import text
from models import db, Make, Model, MakeModel

app = Flask(__name__)
logging.basicConfig(filename='log_file.log')

# connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@' + '.' + '/' + 'vPICList_Lite1' + '?trusted_connection=yes&driver=SQL+Server'
db.init_app(app)

@app.route("/api/discover", methods=['GET'])
def discover_endpoints():
    return [
        url_for("decode_vin"),
        url_for("makes"),
        url_for("models"),
        url_for("make_models")
    ]

@app.route("/api/decodeVin/<vin>", methods=['GET'])
def decode_vin(vin):
    query = text("EXEC[dbo].[spVinDecode] @v = :vin")
    result = db.session.execute(query, {"vin": vin})

    rows = result.fetchall()
    columns = result.keys()
    data = [dict(zip(columns, row)) for row in rows]

    return jsonify(data)

@app.route("/api/makes", methods=['GET'])
def makes():
    makes = Make.query.all()
    return jsonify(makes)

@app.route("/api/models", methods=['GET'])
def models():
    makes = Model.query.all()
    return jsonify(makes)

@app.route("/api/makeModels", methods=['GET'])
def make_models():
    make_models = MakeModel.query.all()
    return jsonify(make_models)

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('Invalid Route was triggered')
    return "Invalid Route"