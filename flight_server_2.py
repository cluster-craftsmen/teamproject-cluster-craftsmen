import pyarrow.flight as flight
import pyarrow as pa
import pandas as pd


class FlightServer(flight.FlightServerBase):

    def __init__(self, location, **kwargs):
        super(FlightServer, self).__init__(location, **kwargs)
        self._location = location
        self._schema = {
            'key': [], 'key_hash_val': [], 'is_primary': [], 'is_secondary': []}
        self._initial_df = pd.DataFrame(self._schema)
        self._data = pa.Table.from_pandas(self._initial_df)

    def do_put(self, context, descriptor, reader, writer):
        description = descriptor.path[0].decode('utf-8')

        if description == "insert":
            data_table = reader.read_all()
            data_to_insert = data_table.to_pandas()

            self._data = pa.Table.from_pandas(self._data.to_pandas()._append(data_to_insert, ignore_index=True))

        if description == "reset":
            self._data = pa.Table.from_pandas(self._initial_df)

        if description == "modify":
            request_data_table = reader.read_all()
            request_data_df = request_data_table.to_pandas()

            keys = request_data_df['keys'].tolist()

            modified_df = self._data.to_pandas()
            modified_df.loc[modified_df['key'].isin(keys), 'is_primary'] = 0
            modified_df.loc[modified_df['key'].isin(keys), 'is_secondary'] = 1

            self._data = pa.Table.from_pandas(modified_df)

        if description == "delete":
            request_data_table = reader.read_all()
            request_data_df = request_data_table.to_pandas()

            keys = request_data_df['keys'].tolist()

            modified_df = self._data.to_pandas()
            modified_df = modified_df[~modified_df['key'].isin(keys)]

            self._data = pa.Table.from_pandas(modified_df)

    def do_get(self, context, ticket):
        return flight.RecordBatchStream(self._data)


if __name__ == '__main__':
    server = FlightServer(location="grpc://0.0.0.0:7771")
    print("Starting the server on localhost:8815")
    server.serve()
