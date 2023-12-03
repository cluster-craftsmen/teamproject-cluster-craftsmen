// BarGraph.tsx
import 'primeicons/primeicons.css';
import 'primereact/resources/themes/lara-light-indigo/theme.css';
import 'primereact/resources/primereact.css';
import 'primeflex/primeflex.css';
import React, { useEffect, useState } from 'react';
import { Chart } from 'primereact/chart';
import { useChartData } from './ChartDataContext';

interface ServerData {
  primary_data_count: number;
}

export default function BarGraph() {
  const { chartData, setChartData } = useChartData();
  const [serverData, setServerData] = useState<ServerData[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/get_data');
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        const result: ServerData[] = await response.json();
        setServerData(result);
        setChartData(result.map((server) => server.primary_data_count));
      } catch (error) {
        console.error('Error fetching data');
      }
    };
    fetchData();
  }, [setChartData]);

  const getLightTheme = () => {
    let basicOptions = {
      maintainAspectRatio: false,
      aspectRatio: 0.8,
      plugins: {
        legend: {
          labels: {
            color: '#495057',
          },
        },
      },
      scales: {
        x: {
          ticks: {
            color: '#495057',
          },
          grid: {
            color: '#ebedef',
          },
        },
        y: {
          ticks: {
            color: '#495057',
          },
          grid: {
            color: '#ebedef',
          },
        },
      },
    };

    return {
      basicOptions,
    };
  };

  const { basicOptions } = getLightTheme();

  return (
    <>
      <div>
        <div className="card">
          {serverData.length > 0 && (
            <div>
              <div> {serverData[0].primary_data_count} </div>
              <Chart
                type="bar"
                data={{
                  labels: ['Server 1', 'Server 2', 'Server 3', 'Server 4'],
                  datasets: [
                    {
                      label: 'Data across Servers',
                      backgroundColor: '#42A5F5',
                      data: chartData,
                    },
                  ],
                }}
                options={basicOptions}
              />
            </div>
          )}
        </div>
      </div>
    </>
  );
}
