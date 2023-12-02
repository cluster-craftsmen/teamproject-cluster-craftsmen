import hashlib

import pandas as pd
import pyarrow as pa
import pyarrow.flight as flight
from bson import ObjectId
from flask import Flask, jsonify, request

import config as app_config
from common import (get_server_metadata, get_comprehensive_server_metadata, insert_data_into_flight_server)

app = Flask(__name__)
hash_ring_len = (2 ** 32) - 1


@app.route('/api/insert_records', methods=['POST'])
def insert_records():
    val = request.get_json()
    records_count = val["records_count"]
    server_metadata, node_hashes = get_server_metadata()

    data = {}
    for i in range(records_count):
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
            helper_server_hash_list = []

            primary_server_hash = str(node_hashes[0 % len(node_hashes)])
            helper_server_hash_list.append(primary_server_hash)

            if (1 % len(node_hashes)) != 0:
                secondary_server_hash = str(node_hashes[1 % len(node_hashes)])
                helper_server_hash_list.append(secondary_server_hash)
            else:
                helper_server_hash_list = str("")

            for server_hash in helper_server_hash_list:
                if server_hash not in data:
                    data[server_hash] = {'key': [], 'key_hash_val': [], 'is_primary': [], 'is_secondary': []}
                data[server_hash]['key'].append(unique_id)
                data[server_hash]['key_hash_val'].append(key_hash)
                data[server_hash]['is_primary'].append(server_hash == primary_server_hash)
                data[server_hash]['is_secondary'].append(server_hash == secondary_server_hash)

    for server_hash, server_data in data.items():
        srv_name = server_metadata[server_hash]['server_name']
        conn_string = app_config.server_mapping[srv_name]["connection_string"]
        insert_data_into_flight_server(conn_string, server_data)

    return jsonify({"message": "Data Insertion Successful"})


@app.route('/api/get_data', methods=['GET'])
def get_data():
    op = []
    phy_server_metadata, vir_server_metadata, _ = get_comprehensive_server_metadata()

    for srv_name in phy_server_metadata:
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


@app.route('/api/add_server', methods=['POST'])
def add_server():
    val = request.get_json()
    server_name = val["server_name"]

    phy_server_metadata, vir_server_metadata, _ = get_comprehensive_server_metadata()
    master_df = pd.DataFrame()
    for srv_name in phy_server_metadata:
        conn_string = app_config.server_mapping[srv_name]["connection_string"]

        client = flight.connect(conn_string)
        reader = client.do_get(flight.Ticket(b''))
        data = reader.read_all()
        df = data.to_pandas()
        master_df = pd.concat([master_df, df], axis=0)
        client.close()

    for server_hash in vir_server_metadata:
        srv_name = vir_server_metadata[server_hash]['server_name']
        conn_string = app_config.server_mapping[srv_name]["connection_string"]

        client = flight.connect(conn_string)
        initial_df = pd.DataFrame({"dummy": []})
        data_table = pa.Table.from_pandas(initial_df)
        reset_descriptor = pa.flight.FlightDescriptor.for_path("reset")
        writer, _ = client.do_put(reset_descriptor, data_table.schema)
        writer.write_table(data_table)
        writer.close()
        client.close()

    app_config.cmpe273_db.servers.update_one({"server_name": server_name}, {"$set": {"is_alive": True}})

    phy_server_metadata_updated, vir_server_metadata_updated, node_hashes = get_comprehensive_server_metadata()

    data = {}
    for index, row in master_df.iterrows():
        unique_id = row["key"]
        key_hash = row["key_hash_val"]
        is_primary = row["is_primary"]

        if not is_primary:
            continue

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
            helper_server_hash_list = []

            primary_server_hash = str(node_hashes[0 % len(node_hashes)])
            helper_server_hash_list.append(primary_server_hash)

            if (1 % len(node_hashes)) != 0:
                secondary_server_hash = str(node_hashes[1 % len(node_hashes)])
                helper_server_hash_list.append(secondary_server_hash)
            else:
                helper_server_hash_list = str("")

            for server_hash in helper_server_hash_list:
                if server_hash not in data:
                    data[server_hash] = {'key': [], 'key_hash_val': [], 'is_primary': [], 'is_secondary': []}
                data[server_hash]['key'].append(unique_id)
                data[server_hash]['key_hash_val'].append(key_hash)
                data[server_hash]['is_primary'].append(server_hash == primary_server_hash)
                data[server_hash]['is_secondary'].append(server_hash == secondary_server_hash)

    for server_hash, server_data in data.items():
        srv_name = vir_server_metadata_updated[server_hash]['server_name']
        conn_string = app_config.server_mapping[srv_name]["connection_string"]
        insert_data_into_flight_server(conn_string, server_data)

    return jsonify({"message": "Data distribution Successful"})


@app.route('/api/disable_server', methods=['POST'])
def disable_server():
    val = request.get_json()
    server_name = val["server_name"]

    phy_server_metadata, vir_server_metadata, _ = get_comprehensive_server_metadata()
    master_df = pd.DataFrame()
    for srv_name in phy_server_metadata:
        conn_string = app_config.server_mapping[srv_name]["connection_string"]

        client = flight.connect(conn_string)
        reader = client.do_get(flight.Ticket(b''))
        data = reader.read_all()
        df = data.to_pandas()
        master_df = pd.concat([master_df, df], axis=0)
        client.close()

    for server_hash in vir_server_metadata:
        srv_name = vir_server_metadata[server_hash]['server_name']
        conn_string = app_config.server_mapping[srv_name]["connection_string"]

        client = flight.connect(conn_string)
        initial_df = pd.DataFrame({"dummy": []})
        data_table = pa.Table.from_pandas(initial_df)
        reset_descriptor = pa.flight.FlightDescriptor.for_path("reset")
        writer, _ = client.do_put(reset_descriptor, data_table.schema)
        writer.write_table(data_table)
        writer.close()
        client.close()

    app_config.cmpe273_db.servers.update_one({"server_name": server_name}, {"$set": {"is_alive": False}})

    phy_server_metadata_updated, vir_server_metadata_updated, node_hashes = get_comprehensive_server_metadata()

    data = {}
    for index, row in master_df.iterrows():
        unique_id = row["key"]
        key_hash = row["key_hash_val"]
        is_primary = row["is_primary"]

        if not is_primary:
            continue

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
            helper_server_hash_list = []

            primary_server_hash = str(node_hashes[0 % len(node_hashes)])
            helper_server_hash_list.append(primary_server_hash)

            if (1 % len(node_hashes)) != 0:
                secondary_server_hash = str(node_hashes[1 % len(node_hashes)])
                helper_server_hash_list.append(secondary_server_hash)
            else:
                helper_server_hash_list = str("")

            for server_hash in helper_server_hash_list:
                if server_hash not in data:
                    data[server_hash] = {'key': [], 'key_hash_val': [], 'is_primary': [], 'is_secondary': []}
                data[server_hash]['key'].append(unique_id)
                data[server_hash]['key_hash_val'].append(key_hash)
                data[server_hash]['is_primary'].append(server_hash == primary_server_hash)
                data[server_hash]['is_secondary'].append(server_hash == secondary_server_hash)

    for server_hash, server_data in data.items():
        srv_name = vir_server_metadata_updated[server_hash]['server_name']
        conn_string = app_config.server_mapping[srv_name]["connection_string"]
        insert_data_into_flight_server(conn_string, server_data)

    return jsonify({"message": "Data distribution Successful"})


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
    app.run(port=5000)