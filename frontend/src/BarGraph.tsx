import 'primeicons/primeicons.css';
import 'primereact/resources/themes/lara-light-indigo/theme.css';
import 'primereact/resources/primereact.css';
import 'primeflex/primeflex.css';
import ReactDOM from 'react-dom';

import React, { useEffect, useState } from 'react';
import { Chart } from 'primereact/chart';

interface ServerData {
    primary_data_count: number,
    secondary_data_count: number,
    server_name: string
}

export default function BarGraph() {

    let [serverData, setServerData] = useState<ServerData[]>([]);
    let [basicData, setBasicData] = useState({
        labels: ['Server 1', 'Server 2', 'Server 3', 'Server 4'],
        datasets: [
            {
                label: 'Data across Servers',
                backgroundColor: '#42A5F5',
                data: [ 77, 59, 80, 100]
            }
        ]
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('/api/get_data');
                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }
                const result: ServerData[] = await response.json();
                setServerData(result);
            } catch (error) {
                console.error('Error fetching data');
            }
        };
        fetchData();
        // let data = basicData;
        // data.datasets[0].data[0] = serverData[0].primary_data_count;
        // setBasicData(data);
    }, []);

    
    // const data = {
    //     labels: ['Server 1', 'Server 2', 'Server 3', 'Server 4'],
    //     datasets: [
    //     {
    //         label: 'Data across Servers',
    //         backgroundColor: '#42A5F5',
    //         data: [ serverData[0].primary_data_count, 59, 80, 100]
    //     }
    // ]
    // }
    // setBasicData(data);

    const getLightTheme = () => {
        let basicOptions = {
            maintainAspectRatio: false,
            aspectRatio: 0.8,
            plugins: {
                legend: {
                    labels: {
                        color: '#495057'
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: '#495057'
                    },
                    grid: {
                        color: '#ebedef'
                    }
                },
                y: {
                    ticks: {
                        color: '#495057'
                    },
                    grid: {
                        color: '#ebedef'
                    }
                }
            }
        };

        return {
            basicOptions
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
                             <Chart type="bar" data={basicData} options={basicOptions} />
                        </div>



                    )}

                </div>
            </div>
        </>
    );
}
