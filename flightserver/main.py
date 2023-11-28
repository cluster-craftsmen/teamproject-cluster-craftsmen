import pyarrow.flight as flight
import pyarrow as pa
import logging

class FlightServer(flight.FlightServerBase):
    _schema = pa.schema([
        ('key', pa.string()), 
        ('key_hash_val', pa.int64()), 
        ('is_primary', pa.bool_()), 
        ('is_secondary', pa.bool_())
    ])

    def __init__(self, location, **kwargs):
        super().__init__(location, **kwargs)
        self._location = location
        self._data = pa.Table.from_batches([pa.RecordBatch.from_arrays(
            [pa.array([], type=field.type) for field in self._schema],
            schema=self._schema
        )])

    def do_put(self, context, descriptor, reader, writer):
        description = descriptor.path[0].decode('utf-8')

        try:
            if description == "insert":
                data_table = reader.read_all()
                self._data = pa.concat_tables([self._data, data_table])

            elif description == "reset":
                self._data = pa.Table.from_batches([pa.RecordBatch.from_arrays(
                    [pa.array([], type=field.type) for field in self._schema],
                    schema=self._schema
                )])

            elif description == "modify":
                request_data_table = reader.read_all()
                request_data_df = request_data_table.to_pandas()

                modified_df = self._data.to_pandas()
                for index, row in request_data_df.iterrows():
                    key = row['key']
                    is_primary = row['is_primary']
                    is_secondary = row['is_secondary']
                    modified_df.loc[modified_df['key'] == key, 'is_primary'] = is_primary
                    modified_df.loc[modified_df['key'] == key, 'is_secondary'] = is_secondary

                self._data = pa.Table.from_pandas(modified_df, preserve_index=False)

            elif description == "delete":
                request_data_table = reader.read_all()
                request_data_df = request_data_table.to_pandas()

                keys_to_delete = request_data_df['key'].tolist()
                modified_df = self._data.to_pandas()
                modified_df = modified_df[~modified_df['key'].isin(keys_to_delete)]

                self._data = pa.Table.from_pandas(modified_df, preserve_index=False)

        except Exception as e:
            logging.error(f"Error in do_put: {e}")

    def do_get(self, context, ticket):
        try:
            return flight.RecordBatchStream(self._data)
        except Exception as e:
            logging.error(f"Error in do_get: {e}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    server = FlightServer(location="grpc://0.0.0.0:8815")
    logging.info("Starting the server on localhost:8815")
    server.serve()
