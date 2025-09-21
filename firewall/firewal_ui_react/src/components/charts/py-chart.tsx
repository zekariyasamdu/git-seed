import Chart from "chart.js/auto";
import { CategoryScale } from "chart.js";
import { memo, useMemo } from "react";
import { Pie } from "react-chartjs-2";
import { Card } from "../ui/card";
import type { Analytics } from "@/types/api";
import { Skeleton } from "../ui/skeleton";

Chart.register(CategoryScale);

type IPychartProps = {
    analytics: Analytics,
    isLoading: boolean,
    title: string,
    lable: string

} & React.HTMLAttributes<HTMLDivElement>

function Pychart({ analytics, isLoading, lable, title, ...props }: IPychartProps) {


    const chartData = useMemo(
        () => ({
            labels: analytics.data.map((d) => d.repo_name.toString()),
            datasets: [
                {
                    label: lable,
                    data: analytics.data.map((d) => d.quantity),
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
        [analytics, lable]
    );

    if (isLoading) return <Card className="p-0 "><Skeleton className="w-[300px] h-[322px] flex flex-col justify-center items-center"></Skeleton></Card>

    return (
        <Card {...props} className="w-fit h-fit flex flex-col justify-center items-center">
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
