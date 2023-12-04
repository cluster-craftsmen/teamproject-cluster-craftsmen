import "@mantine/core/styles.css";
import { MantineProvider, Title } from "@mantine/core";
import { theme } from "./theme";
import DataInput from "./DataInput";
import ServersList from "./ServersList";
import BarGraph from "./BarGraph";
import ResetData from "./ResetData";
import { ChartDataProvider } from './ChartDataContext';


export default function App() {
  return (
    <MantineProvider theme={theme}>
      <Title order={1}>
        Consistent Hashing using Apache Arrow Flight
      </Title>
      <ChartDataProvider>
        <DataInput />
        <ServersList />
        <BarGraph />
        <ResetData />
      </ChartDataProvider>
    </MantineProvider>
  );
}
