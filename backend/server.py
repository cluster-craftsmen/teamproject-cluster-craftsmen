from bson import ObjectId
from flask import Flask, request, jsonify
import hashlib
import pyarrow as pa
import pyarrow.flight as flight
import pandas as pd

import config as app_config

app = Flask(__name__)
hash_ring_len = (2 ** 32) - 1

def get_server_metadata():
    server_metadata = {}
    node_hashes = []
    cursor = app_config.cmpe273_db.servers.find({"is_alive": True})
    for rec in cursor:
        for vir_srv_rec in rec["virtual_servers"]:
            server_metadata[str(vir_srv_rec["hash"])] = {"server_name": rec["server_name"]}
            node_hashes.append(vir_srv_rec["hash"])
    node_hashes.sort()
    return server_metadata, node_hashes

def insert_data_into_flight_server(conn_string, data):
    client = flight.connect(conn_string)
    initial_df = pd.DataFrame(data)
    data_table = pa.Table.from_pandas(initial_df)
    insert_descriptor = pa.flight.FlightDescriptor.for_path("insert")
    writer, _ = client.do_put(insert_descriptor, data_table.schema)
    writer.write_table(data_table)
    writer.close()
    client.close()

@app.route('/api/insert_keys', methods=['POST'])
def insert_keys():
    val = request.get_json()
    key_count = val["key_count"]
    server_metadata, node_hashes = get_server_metadata()
    
    data = {}
    for i in range(key_count):
        unique_id = str(ObjectId())
        key_hash = int(hashlib.sha256(f"{unique_id}".encode()).hexdigest(), 16) % hash_ring_len
        inserted = False
        for k in range(len(node_hashes)):
            if node_hashes[k] <= key_hash <= node_hashes[(k + 1) % len(node_hashes)]:
                primary_server_hash = str(node_hashes[(k + 1) % len(node_hashes)])
                secondary_server_hash = str(node_hashes[(k + 2) % len(node_hashes)])

                for server_hash in [primary_server_hash, secondary_server_hash]:
                    if server_hash not in data:
                        data[server_hash] = {'key': [], 'key_hash_val': [], 'is_primary': [], 'is_secondary': []}
                    data[server_hash]['key'].append(unique_id)
                    data[server_hash]['key_hash_val'].append(key_hash)
                    data[server_hash]['is_primary'].append(server_hash == primary_server_hash)
                    data[server_hash]['is_secondary'].append(server_hash == secondary_server_hash)

                inserted = True
                break

        if not inserted:
            # Fallback logic if not inserted
            pass

    for server_hash, server_data in data.items():
        srv_name = server_metadata[server_hash]['server_name']
        conn_string = app_config.server_mapping[srv_name]["connection_string"]
        insert_data_into_flight_server(conn_string, server_data)

    return jsonify({"message": "Data Insertion Successful"})

@app.route('/api/get_data', methods=['GET'])
def get_data():
    op = []
    server_metadata, _ = get_server_metadata()
    for server_hash in server_metadata:
        srv_name = server_metadata[server_hash]['server_name']
        conn_string = app_config.server_mapping[srv_name]["connection_string"]

        client = flight.connect(conn_string)
        reader = client.do_get(flight.Ticket(b''))
        data = reader.read_all()
        df = data.to_pandas()
        result = {
            "server_name": srv_name,
            "primary_data_count": sum(df["is_primary"]),
            "secondary_data_count": sum(df["is_secondary"]),
        }
        op.append(result)
        client.close()

    return jsonify(op)

@app.route('/api/reset_data', methods=['GET'])
def reset_data():
    server_metadata, _ = get_server_metadata()
    for server_hash in server_metadata:
        srv_name = server_metadata[server_hash]['server_name']
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

if __name__ == '__main__':
    app.run(port=5012)
