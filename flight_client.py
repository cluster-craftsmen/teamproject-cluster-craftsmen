import pyarrow as pa
import pyarrow.flight as flight
import pandas as pd


if __name__ == '__main__':
    client = flight.connect("grpc://0.0.0.0:8815")

    # Construct a POST request
    initial_df = pd.DataFrame({
        'key': ["C"], 'key_hash_val': ["A"], 'is_primary': ["D"], 'is_secondary': ["B"]})
    data_table = pa.Table.from_pandas(initial_df)
    insert_descriptor = pa.flight.FlightDescriptor.for_path("insert")
    writer, _ = client.do_put(insert_descriptor, data_table.schema)
    writer.write_table(data_table)
    writer.close()

    # Construct a GET request
    reader = client.do_get(flight.Ticket(b''))
    data = reader.read_all()

    df = data.to_pandas()
    for index, row in df.iterrows():
        print(row["key"], row["key_hash_val"], row["is_primary"], row["is_secondary"])
