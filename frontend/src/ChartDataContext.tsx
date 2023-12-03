import React, { createContext, useContext, ReactNode, useState } from 'react';

interface ServerData {
  primary_data_count: number;
  secondary_data_count: number;
  server_name: string;
}

interface ChartDataContextProps {
  children: ReactNode;
}

interface ChartDataContextValue {
  serverData: ServerData[];
  setServerData: React.Dispatch<React.SetStateAction<ServerData[]>>;
  fetchAndUpdateServerData: () => Promise<void>;
}

const ChartDataContext = createContext<ChartDataContextValue | undefined>(undefined);

export const ChartDataProvider: React.FC<ChartDataContextProps> = ({ children }) => {
  const [serverData, setServerData] = useState<ServerData[]>([]);

  const fetchAndUpdateServerData = async () => {
    try {
      const response = await fetch('/api/get_data');
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }
      const result: ServerData[] = await response.json();
      setServerData(result);
    } catch (error) {
      console.error('Error fetching and updating data:', error);
    }
  };

  const value: ChartDataContextValue = {
    serverData,
    setServerData,
    fetchAndUpdateServerData,
  };

  return <ChartDataContext.Provider value={value}>{children}</ChartDataContext.Provider>;
};

export const useChartData = (): ChartDataContextValue => {
  const context = useContext(ChartDataContext);
  if (!context) {
    throw new Error('useChartData must be used within a ChartDataProvider');
  }
  return context;
};
