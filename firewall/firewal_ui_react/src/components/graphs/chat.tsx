import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"

import {
    ChartContainer,
    ChartLegend,
    ChartLegendContent,
    ChartTooltip,
    ChartTooltipContent,
    type ChartConfig,
} from "@/components/ui/chart"
import type { MonthlySuccessfulAndBlocked } from "@/types/api"

const chartConfig = {

    blocked_requests: {
        label: "Sccessful",
        color: "#2563eb",
    },
    successful_requests: {
        label: "Blocked",
        color: "#60a5fa",
    }

} satisfies ChartConfig

type ChartsProps = {

    chartData: MonthlySuccessfulAndBlocked[]
} & React.HTMLAttributes<HTMLDivElement>


export function Chart({ chartData, ...props }: ChartsProps) {
    return (

        <ChartContainer config={chartConfig} {...props} >

            <BarChart accessibilityLayer data={chartData} >

                <CartesianGrid vertical={false} />
                <XAxis
                    dataKey="month"
                    tickLine={true}
                    tickMargin={10}
                    axisLine={true}
                    tickFormatter={(value) => value.slice(0, 3)}
                />
                <ChartTooltip content={<ChartTooltipContent />} />
                <ChartLegend content={<ChartLegendContent />} />
                <Bar dataKey="successful_requests"
                    fill="var(--color-desktop)"
                    radius={4} />
                <Bar dataKey="blocked_requests"
                    fill="var(--color-mobile)"
                    radius={4} />

            </BarChart>

        </ChartContainer>
    )
}
