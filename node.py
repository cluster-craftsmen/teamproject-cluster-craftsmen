import hashlib


class Node:
    def __init__(self, ring_len):
        self.M = ring_len

    def generate_sha1_hash(self, node_name, server_num):
        hash_val = int(hashlib.sha1(f"{node_name}-{server_num}".encode()).hexdigest(), 16) % self.M
        return hash_val

    def generate_sha224_hash(self, node_name, server_num):
        hash_val = int(hashlib.sha224(f"{node_name}-{server_num}".encode()).hexdigest(), 16) % self.M
        return hash_val

    def generate_sha256_hash(self, node_name, server_num):
        hash_val = int(hashlib.sha256(f"{node_name}-{server_num}".encode()).hexdigest(), 16) % self.M
        return hash_val

    def generate_sha384_hash(self, node_name, server_num):
        hash_val = int(hashlib.sha384(f"{node_name}-{server_num}".encode()).hexdigest(), 16) % self.M
        return hash_val

    def generate_sha512_hash(self, node_name, server_num):
        hash_val = int(hashlib.sha512(f"{node_name}-{server_num}".encode()).hexdigest(), 16) % self.M
        return hash_val

    def generate_sha3_224_hash(self, node_name, server_num):
        hash_val = int(hashlib.sha3_224(f"{node_name}-{server_num}".encode()).hexdigest(), 16) % self.M
        return hash_val

    def generate_sha3_256_hash(self, node_name, server_num):
        hash_val = int(hashlib.sha3_256(f"{node_name}-{server_num}".encode()).hexdigest(), 16) % self.M
        return hash_val

    def generate_sha3_384_hash(self, node_name, server_num):
        hash_val = int(hashlib.sha3_384(f"{node_name}-{server_num}".encode()).hexdigest(), 16) % self.M
        return hash_val

    @staticmethod
    def generate_meta(node_name, physical_server_num, virtual_server_num):
        meta = {
            "node": f"{node_name}-{physical_server_num}_{virtual_server_num}",
            "server_no": physical_server_num,
            "server_vir_no": virtual_server_num,
            "count": 0
        }
        return meta

    def generate_server_metadata(self, node_name, physical_server_num):
        server_metadata = {}
        node_hashes = []

        for virtual_server_num in range(0, 8, 1):
            hash_val = self.generate_sha256_hash(node_name, f"{physical_server_num}_{virtual_server_num}")
            server_metadata[str(hash_val)] = self.generate_meta(node_name, physical_server_num, virtual_server_num)
            node_hashes.append(hash_val)

        '''
        hash_val = self.generate_sha1_hash(node_name, f"{physical_server_num}_0")
        server_metadata[str(hash_val)] = self.generate_meta(node_name, physical_server_num, 0)
        node_hashes.append(hash_val)

        hash_val = self.generate_sha224_hash(node_name, f"{physical_server_num}_1")
        server_metadata[str(hash_val)] = self.generate_meta(node_name, physical_server_num, 1)
        node_hashes.append(hash_val)

        hash_val = self.generate_sha256_hash(node_name, f"{physical_server_num}_2")
        server_metadata[str(hash_val)] = self.generate_meta(node_name, physical_server_num, 2)
        node_hashes.append(hash_val)

        hash_val = self.generate_sha384_hash(node_name, f"{physical_server_num}_3")
        server_metadata[str(hash_val)] = self.generate_meta(node_name, physical_server_num, 3)
        node_hashes.append(hash_val)

        hash_val = self.generate_sha512_hash(node_name, f"{physical_server_num}_4")
        server_metadata[str(hash_val)] = self.generate_meta(node_name, physical_server_num, 4)
        node_hashes.append(hash_val)

        hash_val = self.generate_sha3_224_hash(node_name, f"{physical_server_num}_5")
        server_metadata[str(hash_val)] = self.generate_meta(node_name, physical_server_num, 5)
        node_hashes.append(hash_val)

        hash_val = self.generate_sha3_256_hash(node_name, f"{physical_server_num}_6")
        server_metadata[str(hash_val)] = self.generate_meta(node_name, physical_server_num, 6)
        node_hashes.append(hash_val)

        hash_val = self.generate_sha3_384_hash(node_name, f"{physical_server_num}_7")
        server_metadata[str(hash_val)] = self.generate_meta(node_name, physical_server_num, 7)
        node_hashes.append(hash_val)
        '''
        return server_metadata, node_hashes
