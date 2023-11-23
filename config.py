from pymongo import MongoClient

# mongodb_username = "cmpe202"
# mongodb_password = "m5mg84zEtM0le7J9"
# mongo_uri = "mongodb+srv://{0}:{1}@cmpe202.2pmv4sg.mongodb.net/".format(
#     mongodb_username, mongodb_password)

client = MongoClient("mongodb://localhost:27017/")
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
