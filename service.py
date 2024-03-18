from flask import Flask, request, jsonify, abort
import logging
from datetime import datetime

app = Flask(__name__)

# Oletetaan, että palvelu on aluksi sammutettu.
service_running = False
data_store = {}

# Asetetaan lokitus. Tallennetaan lokitiedot tiedostoon `service.log`.
logging.basicConfig(filename="service.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

@app.route("/api/start", methods=["GET"])
def start_service():
    global service_running
    if service_running:
        abort(409, "Service already running")
    service_running = True
    logger.info("Service started")
    return "Service started"

@app.route("/api/stop", methods=["GET"])
def stop_service():
    global service_running
    service_running = False
    logger.info("Service stopped")
    return "Service stopped"

@app.route("/api/restart", methods=["GET"])
def restart_service():
    global service_running
    if not service_running:
        abort(404)
    service_running = False
    service_running = True
    logger.info("Service restarted")
    return "Service restarted"

@app.route("/api/data", methods=["POST"])
def add_data():
    if not service_running:
        abort(404)
    data = request.json
    data_id = data.get("id")  # Oletetaan, että jokaisella datalla on uniikki "id"
    if data_id in data_store:
        return jsonify({"error": "Data with the given id already exists"}), 400
    data_store[data_id] = data
    logger.info(f"Data added: {data}")
    return jsonify(data), 201


@app.route("/api/data/<data_id>", methods=["GET"])
def get_data(data_id):
    if not service_running:
        abort(404)
    if data_id in data_store:
        logger.info(f"Returning data for id: {data_id}")
        return jsonify(data_store[data_id])
    else:
        logger.warning(f"Getting data with id {data_id}, data not found")
        return "Data not found", 404


@app.route("/api/data/<data_id>", methods=["PUT"])
def update_data(data_id):
    if not service_running:
        abort(404)
    if data_id in data_store:
        data = request.json
        data_store[data_id] = data  # Päivitetään data annetulla data_id:llä
        logger.info(f"Data updated: {data}")
        return jsonify(data), 200
    else:
        logger.warning(f"Updating data with id {data_id}, data not found")
        return "Data not found", 404


@app.route("/api/data/<data_id>", methods=["DELETE"])
def delete_data(data_id):
    if not service_running:
        abort(404)
    if data_id in data_store:
        del data_store[data_id]  # Poistetaan data annetulla data_id:llä
        logger.info(f"Data deleted with id: {data_id}")
        return "Data deleted", 200
    else:
        logger.warning(f"Deleting data with id {data_id}, data not found")
        return "Data not found", 404


@app.route("/api/data", methods=["GET"])
def list_data():
    if not service_running:
        abort(404)
    logger.info("Returning all data")
    return jsonify(data_store)


@app.route('/api/neitiaika', methods=['GET'])
def get_local_time():
    local_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"Returning local time {local_time}")
    return jsonify({"local_time": local_time})


@app.route('/api/addsimpledata', methods=['GET'])
def add_or_update_simple_data():
    if not service_running:
        abort(404)

    data_id = request.args.get('id')
    data_value = request.args.get('data')
    if data_id is None or data_value is None:
        return jsonify({"error": "Both 'id' and 'data' parameters are required"}), 400

    data_store[data_id] = data_value
    logger.info(f"Data {'added' if data_id not in data_store else 'updated'}: {data_id} = {data_value}")

    return jsonify({data_id: data_value}), 200


@app.route('/api/getsimpledata', methods=['GET'])
def get_simple_data():
    data_id = request.args.get('id')
    if data_id is None:
        return jsonify({"error": "'id' parameter is required"}), 400

    return get_data(data_id)


@app.route('/api/deletesimpledata', methods=['GET'])
def delete_simple_data():
    data_id = request.args.get('id')
    if data_id is None:
        return jsonify({"error": "'id' parameter is required"}), 400

    return delete_data(data_id)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
