import "@mantine/core/styles.css";
// import React, { FormEvent, useCallback, useState } from "react";
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
      <Title>
        Consistent Hashing
      </Title>
      <ChartDataProvider>
      <DataInput/>
      <ServersList/>
      <BarGraph/>
      <ResetData/>
      </ChartDataProvider>
    </MantineProvider>

  )
}
