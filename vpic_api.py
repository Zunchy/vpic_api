import logging
from typing import Any
from flask import Flask, make_response, request, url_for, jsonify
from sqlalchemy import text
from models import Suggestions, db, Make, Model, MakeModel, VinResult
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
logging.basicConfig(filename='log_file.log')

# connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@' + '.' + '/' + 'vPICList_Lite1' + '?trusted_connection=yes&trustservercertificate=yes&driver=ODBC+Driver+18+for+SQL+Server'
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

@app.route("/api/suggestion", methods=['POST'])
def add_suggestion():
    data = request.json
    suggestion_to_add = mapSuggestionToModel(dict(data))

    try:
        db.session.add(suggestion_to_add)
        db.session.commit()
        db.session.refresh(suggestion_to_add)
        return jsonify(suggestion_to_add)
    except Exception as e:
        app.logger.info(e)
        return make_response("Error occured during record add", 400)

@app.route("/api/suggestion", methods=['PUT'])
def update_suggestion():
    data = request.json

    matching_model = Suggestions.query.get(data["id"])
    if matching_model is None:
        return make_response("Record not found", 400)

    matching_model = mapSuggestionForUpdate(matching_model, dict(data))

    try:
        db.session.commit()
        db.session.refresh(matching_model)
        return jsonify(matching_model)
    except Exception as e:
        app.logger.info(e)
        return make_response("Error occured during record update", 400)

@app.route("/api/suggestion", methods=['DELETE'])
def delete_suggestion():
    data = request.json

    matching_model = Suggestions.query.get(data["id"])
    if matching_model is None:
        return make_response("Record not found", 400)

    try:
        db.session.delete(matching_model)
        db.session.commit()
        return make_response("Success", 200)
    except Exception as e:
        app.logger.info(e)
        return make_response("Error occured during record delete", 400)
    
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

def mapSuggestionToModel(data: dict[Any, Any]) -> Suggestions:
    model = Suggestions()

    model.name = data["name"]
    model.phoneNumber = data["phoneNumber"]
    model.email = data["email"]
    model.suggestion = data["suggestion"]

    return model

def mapSuggestionForUpdate(suggestion: Suggestions, data: dict[Any, Any]):
    suggestion.name = data["name"]
    suggestion.phoneNumber = data["phoneNumber"]
    suggestion.email = data["email"]
    suggestion.suggestion = data["suggestion"]

    return suggestion