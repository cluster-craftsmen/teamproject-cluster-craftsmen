from pymongo import MongoClient

mongodb_username = "cmpe273"
mongodb_password = "BmnVjvshPsET48ej"
mongo_uri = f"mongodb+srv://{mongodb_username}:{mongodb_password}@cmpe273finalproject.lxfgnam.mongodb.net/"

# client = MongoClient("mongodb://localhost:27017/")
# cmpe273_db = client["cmpe273"]

client = MongoClient(mongo_uri)
cmpe273_db = client["cmpe273"]

server_mapping = {
    "S1": {
        "connection_string": "grpc://0.0.0.0:7770"
    },
    "S2": {
        "connection_string": "grpc://0.0.0.0:7771"
    },
    "S3": {
        "connection_string": "grpc://0.0.0.0:7772"
    },
    "S4": {
        "connection_string": "grpc://0.0.0.0:7773"
    }
}
