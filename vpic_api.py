import logging
from typing import Any
from flask import Flask, url_for, jsonify
from sqlalchemy import text
from models import db, Make, Model, MakeModel, VinResult
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
logging.basicConfig(filename='log_file.log')

# connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@' + '.' + '/' + 'vPICList_Lite1' + '?trusted_connection=yes&driver=SQL+Server'
db.init_app(app)

@app.route("/api/discover", methods=['GET'])
def discover_endpoints():
    return [
        url_for("decode_vin", vin='VIN_NUMBER'),
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
    data = [mapDecodeProcedureResults(dict(zip(columns, row))) for row in rows]

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

# Mapping Methods
def mapDecodeProcedureResults(data: dict[Any, Any]):
    app.logger.info(data)
    result = VinResult()
    result.attributeId = data["AttributeId"]
    result.code = data["Code"]
    result.createdOn = data["CreatedOn"]
    result.dataType = data["DataType"]
    result.decode = data["Decode"]
    result.elementId = data["ElementId"]
    result.groupName = data["GroupName"]
    result.keys = data["Keys"]
    result.patternId = data["PatternId"]
    result.source = data["Source"]
    result.value = data["Value"]
    result.variable = data["Variable"]
    result.vinSchemaId = data["VinSchemaId"]
    result.wmiId = data["WmiId"]

    return result
