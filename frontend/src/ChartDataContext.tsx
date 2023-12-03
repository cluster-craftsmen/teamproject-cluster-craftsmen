import React, { createContext, useContext, ReactNode, useState } from 'react';

interface ChartDataContextProps {
  children: ReactNode;
}

interface ChartDataContextValue {
  chartData: number[];
  setChartData: React.Dispatch<React.SetStateAction<number[]>>;
}

const ChartDataContext = createContext<ChartDataContextValue | undefined>(undefined);

export const ChartDataProvider: React.FC<ChartDataContextProps> = ({ children }) => {
  const [chartData, setChartData] = useState<number[]>([]);

  const value: ChartDataContextValue = {
    chartData,
    setChartData,
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
