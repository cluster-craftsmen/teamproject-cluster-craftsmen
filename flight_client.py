# FlightClient.py
import pyarrow.flight as flight


if __name__ == '__main__':
    location = flight.Location.for_grpc_tcp(host="localhost", port=50051)
    client = flight.FlightClient(location)

    reader = client.do_get(flight.Ticket(b''))
    data = reader.read_all()

    table_dict = data.to_pydict()
    print(table_dict)
