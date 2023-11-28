from bson import ObjectId
from flask import Flask, request, jsonify
import hashlib
from pprint import pprint as pp
import pyarrow as pa
import pyarrow.flight as flight
import pandas as pd

import config as app_config

app = Flask(__name__)


@app.route('/api/insert_keys', methods=['POST'])
def insert_keys():
    val = request.get_json()
    key_count = val["key_count"]

    server_metadata = {}
    node_hashes = []
    cursor = app_config.cmpe273_db.servers.find({"is_alive": True})
    for rec in cursor:
        for vir_srv_rec in rec["virtual_servers"]:
            server_metadata[str(vir_srv_rec["hash"])] = {"server_name": rec["server_name"]}
            node_hashes.append(vir_srv_rec["hash"])
    node_hashes.sort()

    data = {}
    for i in range(key_count):
        unique_id = str(ObjectId())
        key_hash = int(hashlib.sha256(f"{unique_id}".encode()).hexdigest(), 16) % hash_ring_len

        inserted = False
        for k in range(0, len(node_hashes)):
            if (node_hashes[k % len(node_hashes)]) <= key_hash <= (node_hashes[(k + 1) % len(node_hashes)]):
                if str(node_hashes[(k + 1) % len(node_hashes)]) in data:
                    data[str(node_hashes[(k + 1) % len(node_hashes)])]['key'].append(unique_id)
                    data[str(node_hashes[(k + 1) % len(node_hashes)])]['key_hash_val'].append(key_hash)
                    data[str(node_hashes[(k + 1) % len(node_hashes)])]['is_primary'].append(1)
                    data[str(node_hashes[(k + 1) % len(node_hashes)])]['is_secondary'].append(0)
                else:
                    data[str(node_hashes[(k + 1) % len(node_hashes)])] = {
                        'key': [unique_id], 'key_hash_val': [key_hash], 'is_primary': [1], 'is_secondary': [0]
                    }

                if str(node_hashes[(k + 2) % len(node_hashes)]) in data:
                    data[str(node_hashes[(k + 2) % len(node_hashes)])]['key'].append(unique_id)
                    data[str(node_hashes[(k + 2) % len(node_hashes)])]['key_hash_val'].append(key_hash)
                    data[str(node_hashes[(k + 2) % len(node_hashes)])]['is_primary'].append(0)
                    data[str(node_hashes[(k + 2) % len(node_hashes)])]['is_secondary'].append(1)
                else:
                    data[str(node_hashes[(k + 2) % len(node_hashes)])] = {
                        'key': [unique_id], 'key_hash_val': [key_hash], 'is_primary': [0], 'is_secondary': [1]
                    }

                inserted = True
                break
        if not inserted:
            if str(node_hashes[0 % len(node_hashes)]) in data:
                data[str(node_hashes[0 % len(node_hashes)])]['key'].append(unique_id)
                data[str(node_hashes[0 % len(node_hashes)])]['key_hash_val'].append(key_hash)
                data[str(node_hashes[0 % len(node_hashes)])]['is_primary'].append(1)
                data[str(node_hashes[0 % len(node_hashes)])]['is_secondary'].append(0)
            else:
                data[str(node_hashes[0 % len(node_hashes)])] = {
                    'key': [unique_id], 'key_hash_val': [key_hash], 'is_primary': [1], 'is_secondary': [0]
                }

            if 1 % len(node_hashes) != 0:
                if str(node_hashes[1]) in data:
                    data[str(node_hashes[1])]['key'].append(unique_id)
                    data[str(node_hashes[1])]['key_hash_val'].append(key_hash)
                    data[str(node_hashes[1])]['is_primary'].append(0)
                    data[str(node_hashes[1])]['is_secondary'].append(1)
                else:
                    data[str(node_hashes[1])] = {
                        'key': [unique_id], 'key_hash_val': [key_hash], 'is_primary': [0], 'is_secondary': [1]
                    }

    for server_hash, server_data in data.items():
        # if server_metadata[server_hash]['server_name'] == "S1":
        srv_name = server_metadata[server_hash]['server_name']
        conn_string = app_config.server_mapping[srv_name]["connection_string"]
        client = flight.connect(conn_string)
        initial_df = pd.DataFrame(server_data)
        data_table = pa.Table.from_pandas(initial_df)
        insert_descriptor = pa.flight.FlightDescriptor.for_path("insert")
        writer, _ = client.do_put(insert_descriptor, data_table.schema)
        writer.write_table(data_table)
        writer.close()
        client.close()

    return 'Perfect'


@app.route('/api/get_data', methods=['GET'])
def get_data():
    op = []
    cursor = app_config.cmpe273_db.servers.find({"is_alive": True})
    for rec in cursor:
        srv_name = rec["server_name"]
        conn_string = app_config.server_mapping[srv_name]["connection_string"]

        client = flight.connect(conn_string)
        reader = client.do_get(flight.Ticket(b''))
        data = reader.read_all()

        df = data.to_pandas()
        result = {
            "server_name": rec["server_name"],
            "primary_data_count": 0,
            "secondary_data_count": 0,
        }
        for index, row in df.iterrows():
            result["primary_data_count"] += row["is_primary"]
            result["secondary_data_count"] += row["is_secondary"]

        op.append(result)
        client.close()

    return jsonify(op)


@app.route('/api/reset_data', methods=['GET'])
def reset_data():
    op = []
    cursor = app_config.cmpe273_db.servers.find({"is_alive": True})
    for rec in cursor:
        srv_name = rec["server_name"]
        conn_string = app_config.server_mapping[srv_name]["connection_string"]

        client = flight.connect(conn_string)

        initial_df = pd.DataFrame({"dummy": []})
        data_table = pa.Table.from_pandas(initial_df)
        reset_descriptor = pa.flight.FlightDescriptor.for_path("reset")
        writer, _ = client.do_put(reset_descriptor, data_table.schema)
        writer.write_table(data_table)
        writer.close()
        client.close()

    return jsonify({"message": "Data Reset Successful"})


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    hash_ring_len = (2 ** 32) - 1

    app.run()
