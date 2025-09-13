import Chart from "chart.js/auto";
import { CategoryScale } from "chart.js";
import { useState } from "react";
import { Pie } from "react-chartjs-2";

// Define the data type
interface DataPoint {
    id: number;
    year: number;
    userGain: number;
    userLost: number;
}

const Data: DataPoint[] = [
    {
        id: 1,
        year: 2016,
        userGain: 80000,
        userLost: 823
    },
    {
        id: 2,
        year: 2017,
        userGain: 45677,
        userLost: 345
    },
    {
        id: 3,
        year: 2018,
        userGain: 78888,
        userLost: 555
    },
    {
        id: 4,
        year: 2019,
        userGain: 90000,
        userLost: 4555
    },
    {
        id: 5,
        year: 2020,
        userGain: 4300,
        userLost: 234
    }
];

Chart.register(CategoryScale);

export default function Pychart() {
    const [chartData] = useState({
        labels: Data.map((data) => data.year.toString()),
        datasets: [
            {
                label: "Users Gained",
                data: Data.map((data) => data.userGain),
                backgroundColor: [
                    "rgba(75,192,192,1)",
                    "#ecf0f1",
                    "#50AF95",
                    "#f3ba2f",
                    "#2a71d0"
                ],
                borderColor: "black",
                borderWidth: 2
            }
        ]
    });

    return (
        <div className="w-1/3 h-full">
            <div className="chart-container w-full h-full">
                <h2 style={{ textAlign: "center" }}>Pie Chart</h2>
                <Pie className="w-full h-full"
                    data={chartData}
                    options={{
                        plugins: {
                            title: {
                                display: false,
                                text: "Users Gained between 2016-2020"
                            }
                        }
                    }}
                />
            </div>
        </div>
    );
}