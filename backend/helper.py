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


''' MONGODB servers collection records
{
    "_id" : ObjectId("655e99b4fa1e3e7d5858fa71"),
    "server_name" : "S1",
    "ip" : "57.127.173.228",
    "is_alive" : true,
    "physical_server_num" : NumberInt(1),
    "virtual_servers" : [
        {
            "virtual_server_num" : NumberInt(1),
            "hash" : NumberInt(343916181)
        },
        {
            "virtual_server_num" : NumberInt(2),
            "hash" : NumberInt(672061336)
        },
        {
            "virtual_server_num" : NumberInt(3),
            "hash" : NumberLong(3970224632)
        },
        {
            "virtual_server_num" : NumberInt(4),
            "hash" : NumberLong(2934886673)
        },
        {
            "virtual_server_num" : NumberInt(5),
            "hash" : NumberLong(2310567160)
        },
        {
            "virtual_server_num" : NumberInt(6),
            "hash" : NumberLong(3639521738)
        },
        {
            "virtual_server_num" : NumberInt(7),
            "hash" : NumberLong(2522800927)
        },
        {
            "virtual_server_num" : NumberInt(8),
            "hash" : NumberInt(1581010100)
        }
    ]
}
{
    "_id" : ObjectId("655e9b20fa1e3e7d5858fa72"),
    "server_name" : "S2",
    "ip" : "37.193.200.207",
    "is_alive" : true,
    "physical_server_num" : NumberInt(2),
    "virtual_servers" : [
        {
            "virtual_server_num" : NumberInt(1),
            "hash" : NumberLong(3271804495)
        },
        {
            "virtual_server_num" : NumberInt(2),
            "hash" : NumberInt(382375538)
        },
        {
            "virtual_server_num" : NumberInt(3),
            "hash" : NumberInt(1072829011)
        },
        {
            "virtual_server_num" : NumberInt(4),
            "hash" : NumberInt(402487703)
        },
        {
            "virtual_server_num" : NumberInt(5),
            "hash" : NumberLong(3586275773)
        },
        {
            "virtual_server_num" : NumberInt(6),
            "hash" : NumberLong(3921087882)
        },
        {
            "virtual_server_num" : NumberInt(7),
            "hash" : NumberLong(3107098241)
        },
        {
            "virtual_server_num" : NumberInt(8),
            "hash" : NumberInt(1233903388)
        }
    ]
}
{
    "_id" : ObjectId("655e9b6ffa1e3e7d5858fa73"),
    "server_name" : "S3",
    "ip" : "69.65.46.27",
    "is_alive" : true,
    "physical_server_num" : NumberInt(3),
    "virtual_servers" : [
        {
            "virtual_server_num" : NumberInt(1),
            "hash" : NumberInt(2053069429)
        },
        {
            "virtual_server_num" : NumberInt(2),
            "hash" : NumberInt(805699460)
        },
        {
            "virtual_server_num" : NumberInt(3),
            "hash" : NumberLong(2961735483)
        },
        {
            "virtual_server_num" : NumberInt(4),
            "hash" : NumberInt(1135430556)
        },
        {
            "virtual_server_num" : NumberInt(5),
            "hash" : NumberLong(3356668517)
        },
        {
            "virtual_server_num" : NumberInt(6),
            "hash" : NumberLong(3233286366)
        },
        {
            "virtual_server_num" : NumberInt(7),
            "hash" : NumberInt(1344330928)
        },
        {
            "virtual_server_num" : NumberInt(8),
            "hash" : NumberLong(3260641313)
        }
    ]
}
{
    "_id" : ObjectId("655e9b90fa1e3e7d5858fa74"),
    "server_name" : "S4",
    "ip" : "183.115.118.221",
    "is_alive" : true,
    "physical_server_num" : NumberInt(4),
    "virtual_servers" : [
        {
            "virtual_server_num" : NumberInt(1),
            "hash" : NumberInt(1739662624)
        },
        {
            "virtual_server_num" : NumberInt(2),
            "hash" : NumberLong(3443381417)
        },
        {
            "virtual_server_num" : NumberInt(3),
            "hash" : NumberInt(1993646231)
        },
        {
            "virtual_server_num" : NumberInt(4),
            "hash" : NumberInt(818871430)
        },
        {
            "virtual_server_num" : NumberInt(5),
            "hash" : NumberInt(591648473)
        },
        {
            "virtual_server_num" : NumberInt(6),
            "hash" : NumberLong(3052278266)
        },
        {
            "virtual_server_num" : NumberInt(7),
            "hash" : NumberLong(3320611392)
        },
        {
            "virtual_server_num" : NumberInt(8),
            "hash" : NumberLong(4074332221)
        }
    ]
}
'''