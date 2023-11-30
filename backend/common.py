import config as app_config
import pyarrow as pa
import pyarrow.flight as flight
import pandas as pd


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


def get_comprehensive_server_metadata():
    phy_server_metadata = {}
    vir_server_metadata = {}
    node_hashes = []

    cursor = app_config.cmpe273_db.servers.find({"is_alive": True})
    for rec in cursor:
        phy_server_metadata[rec["server_name"]] = []
        for vir_srv_rec in rec["virtual_servers"]:
            vir_server_metadata[str(vir_srv_rec["hash"])] = {"server_name": rec["server_name"]}
            phy_server_metadata[rec["server_name"]].append(vir_srv_rec["hash"])
            node_hashes.append(vir_srv_rec["hash"])
    node_hashes.sort()
    return phy_server_metadata, vir_server_metadata, node_hashes


def insert_data_into_flight_server(conn_string, data):
    client = flight.connect(conn_string)
    initial_df = pd.DataFrame(data)
    data_table = pa.Table.from_pandas(initial_df)
    insert_descriptor = pa.flight.FlightDescriptor.for_path("insert")
    writer, _ = client.do_put(insert_descriptor, data_table.schema)
    writer.write_table(data_table)
    writer.close()
    client.close()
