import config as app_config
from node import Node

# client = MongoClient("mongodb://localhost:27017/")
# cmpe273_db = client["cmpe273"]


def update_hash_values():
    hash_ring_len = (2 ** 32) - 1
    node_client = Node(hash_ring_len)

    cursor = app_config.cmpe273_db.servers.find({})
    for rec in cursor:
        virtual_servers = list(rec["virtual_servers"])
        virtual_servers[0]["hash"] = node_client.generate_sha256_hash(
            rec["server_name"], f"{rec['physical_server_num']}_{virtual_servers[0]['virtual_server_num']}")
        virtual_servers[1]["hash"] = node_client.generate_sha256_hash(
            rec["server_name"], f"{rec['physical_server_num']}_{virtual_servers[1]['virtual_server_num']}")
        virtual_servers[2]["hash"] = node_client.generate_sha256_hash(
            rec["server_name"], f"{rec['physical_server_num']}_{virtual_servers[2]['virtual_server_num']}")
        virtual_servers[3]["hash"] = node_client.generate_sha256_hash(
            rec["server_name"], f"{rec['physical_server_num']}_{virtual_servers[3]['virtual_server_num']}")
        virtual_servers[4]["hash"] = node_client.generate_sha256_hash(
            rec["server_name"], f"{rec['physical_server_num']}_{virtual_servers[4]['virtual_server_num']}")
        virtual_servers[5]["hash"] = node_client.generate_sha256_hash(
            rec["server_name"], f"{rec['physical_server_num']}_{virtual_servers[5]['virtual_server_num']}")
        virtual_servers[6]["hash"] = node_client.generate_sha256_hash(
            rec["server_name"], f"{rec['physical_server_num']}_{virtual_servers[6]['virtual_server_num']}")
        virtual_servers[7]["hash"] = node_client.generate_sha256_hash(
            rec["server_name"], f"{rec['physical_server_num']}_{virtual_servers[7]['virtual_server_num']}")

        app_config.cmpe273_db.servers.update_one({"_id": rec["_id"]}, {"$set": {"virtual_servers": virtual_servers}})


update_hash_values()

