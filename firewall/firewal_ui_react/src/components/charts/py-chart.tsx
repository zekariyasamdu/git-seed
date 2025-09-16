import Chart from "chart.js/auto";
import { CategoryScale } from "chart.js";
import { memo, useMemo } from "react";
import { Pie } from "react-chartjs-2";
import { Card } from "../ui/card";

Chart.register(CategoryScale);

interface DataPoint {
    id: number;
    year: number;
    userGain: number;
    userLost: number;
}

type IPychartProps = {
    Data: DataPoint[];
    title: string
} & React.HTMLAttributes<HTMLDivElement>

function Pychart({ Data, title, ...props }: IPychartProps) {

    const chartData = useMemo(
        () => ({
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
                        "#2a71d0",
                    ],
                    borderColor: "black",
                    borderWidth: 1,
                },
            ],
        }),
        [Data]
    );

    return (
        <Card {...props}>
            <h2 style={{ textAlign: "center" }}>{title}</h2>
            <div className="relative w-fit h-56 flex items-center justify-center">
                <Pie
                    data={chartData}
                    options={{
                        cutout: "70%",
                        plugins: {
                            title: {
                                display: false,
                                text: "Users Gained between 2016-2020",
                            },
                            legend: {
                                display: true,
                                position: "bottom",
                            },
                        },
                        responsive: true,
                        maintainAspectRatio: false,
                    }}
                />
            </div>
        </Card>
    );
}


export default memo(Pychart);
