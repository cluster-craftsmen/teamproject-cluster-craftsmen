from bson import ObjectId
import hashlib
from pprint import pprint as pp

from node import Node
import pandas as pd


def main():
    server_metadata = {}
    node_hashes = []

    hash_ring_len = (2 ** 32) - 1
    node_client = Node(hash_ring_len)

    for physical_server_num in range(0, 4, 1):
        node_name = '{}.{}.{}.{}'.format(*__import__('random').sample(range(0, 255), 4))
        print(node_name)
        metadata, hashes = node_client.generate_server_metadata(node_name, physical_server_num)
        server_metadata = dict(server_metadata, **metadata)
        node_hashes.extend(hashes)

    node_hashes.sort()
    pp(node_hashes)

    for i in range(100000):
        unique_id = str(ObjectId())
        hash_val = int(hashlib.sha256(f"{unique_id}".encode()).hexdigest(), 16) % hash_ring_len

        inserted = False
        for k in range(0, len(node_hashes)):
            if (node_hashes[k % len(node_hashes)]) <= hash_val <= (node_hashes[(k + 1) % len(node_hashes)]):
                server_metadata[str(node_hashes[(k + 1) % len(node_hashes)])]["count"] += 1
                inserted = True
                break
        if not inserted:
            server_metadata[str(node_hashes[0])]["count"] += 1

    pp(server_metadata)
    # server_metadata_normalized = pd.json_normalize(server_metadata)
    # for hash_val, row in server_metadata_normalized.iterrows():
    #     print(row)
    hm_dup = {}
    total_count = 0
    for key, val in server_metadata.items():
        if str(val["server_no"]) in hm_dup:
            hm_dup[str(val["server_no"])] += val["count"]
            total_count += val["count"]
        else:
            hm_dup[str(val["server_no"])] = val["count"]
            total_count += val["count"]
    pp(hm_dup)
    print(total_count)


if __name__ == "__main__":
    main()