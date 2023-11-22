# FlightServer.py
import pyarrow.flight as flight
import pyarrow as pa
from pyarrow import json
import pandas as pd


class NumberFlightServer(flight.FlightServerBase):
    def do_get(self, context, ticket):
        # pa.Table.from_pylist()
        # data = pa.Table.from_pydict({"A": "b", "B": {"C": "D"}})
        # data = pa.Table.from_pylist([
        #     {"eqwe": 1, "wqe": "a"},
        #     {"3213": {"dsad": 1}, "4535": "a"}
        # ])
        table = json.read_json(fn)
        return flight.RecordBatchStream(data)

    def do_put(self, context, descriptor, reader, writer):
        dataset = descriptor.path[0].decode('utf-8')


if __name__ == '__main__':
    location = flight.Location.for_grpc_tcp(host="localhost", port=50051)
    server = NumberFlightServer(location)
    print("Starting the server on localhost:50051")
    server.serve()
