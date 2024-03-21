from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, abort, reqparse
import logging
import os
from datetime import datetime
import time
import random

app = Flask(__name__)
api = Api(app, version="1.0", title="Service API", description="A simple service management API")

# global variables
service_running = False
data_store = {}

# logging settings
logging.basicConfig(filename="service.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

# model for data
data_model = api.model("Data", {
    "id": fields.String(required=True, description="Data identifier"),
    "data": fields.String(required=True, description="Data content")
})


@api.route("/api/start")
class StartService(Resource):
    def get(self):
        global service_running
        if service_running:
            abort(409, "Service already running")
        service_running = True
        logger.info("Service starting")
        time.sleep(random.randint(3, 12))
        logger.info("Service started")
        return "Service started"


@api.route("/api/stop")
class StopService(Resource):
    def get(self):
        global service_running
        if not service_running:
            abort(404)
        service_running = False
        logger.info("Service stopping")
        time.sleep(random.randint(2, 8))
        logger.info("Service stopped")
        return "Service stopped"


@api.route("/api/shutdown")
class ShutdownService(Resource):
    def get(self):
        global service_running
        if not service_running:
            abort(404)
        service_running = False
        logger.info("Service shut down")
        os._exit(0)


@api.route("/api/data", methods=["POST"])
class AddData(Resource):
    @api.expect(data_model, validate=True)
    def post(self):
        if not service_running:
            abort(404)
        data = request.json
        data_id = data.get("id")
        if data_id in data_store:
            return {"error": "Data with the given id already exists"}, 400
        data_store[data_id] = data
        logger.info(f"Data added: {data}")
        return data, 201


@api.route("/api/data/<data_id>")
class DataOperations(Resource):
    def get(self, data_id):
        if not service_running:
            abort(404)
        if data_id in data_store:
            logger.info(f"Returning data for id: {data_id}")
            return jsonify(data_store[data_id])
        else:
            logger.warning(f"Getting data with id {data_id}, data not found")
            abort(404, "Data not found")

    def put(self, data_id):
        if not service_running:
            abort(404)
        if data_id in data_store:
            data = request.json
            data_store[data_id] = data
            logger.info(f"Data updated: {data}")
            return data, 200
        else:
            logger.warning(f"Updating data with id {data_id}, data not found")
            abort(404, "Data not found")

    def delete(self, data_id):
        if not service_running:
            abort(404)
        if data_id in data_store:
            del data_store[data_id]
            logger.info(f"Data deleted with id: {data_id}")
            return "Data deleted", 200
        else:
            logger.warning(f"Deleting data with id {data_id}, data not found")
            abort(404, "Data not found")


@api.route("/api/data")
class ListData(Resource):
    def get(self):
        if not service_running:
            abort(404)
        logger.info("Returning all data")
        return jsonify(data_store)


@api.route("/api/neitiaika")
class LocalTime(Resource):
    def get(self):
        local_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Returning local time {local_time}")
        return {"local_time": local_time}


# parsers for GET parameters
add_update_parser = reqparse.RequestParser()
add_update_parser.add_argument("id", type=str, required=True, help="Data's ID")
add_update_parser.add_argument("data", type=str, required=True, help="Data's content")

get_delete_parser = reqparse.RequestParser()
get_delete_parser.add_argument("id", type=str, required=True, help="Data's ID")


@api.route("/api/addsimpledata")
@api.expect(add_update_parser)
class AddOrUpdateSimpleData(Resource):
    def get(self):
        args = add_update_parser.parse_args()
        data_id = args["id"]
        data_value = args["data"]

        if not service_running:
            abort(404, "Service is not running")

        data_store[data_id] = data_value
        logger.info(f"Data {'added' if data_id not in data_store else 'updated'}: {data_id} = {data_value}")

        return {data_id: data_value}, 200


@api.route("/api/getsimpledata")
@api.expect(get_delete_parser)
class GetSimpleData(Resource):
    def get(self):
        args = get_delete_parser.parse_args()
        data_id = args["id"]

        if not service_running:
            abort(404, "Service is not running")
        if data_id not in data_store:
            abort(404, "Data not found")

        logger.info(f"Returning data for id: {data_id}")
        return {data_id: data_store[data_id]}


@api.route("/api/deletesimpledata")
@api.expect(get_delete_parser)
class DeleteSimpleData(Resource):
    def get(self):
        args = get_delete_parser.parse_args()
        data_id = args["id"]

        if not service_running:
            abort(404, "Service is not running")
        if data_id not in data_store:
            abort(404, "Data not found")

        del data_store[data_id]
        logger.info(f"Data deleted with id: {data_id}")
        return {"message": "Data deleted"}, 200


if __name__ == "__main__":
    app.run(debug=True, port=8080)
