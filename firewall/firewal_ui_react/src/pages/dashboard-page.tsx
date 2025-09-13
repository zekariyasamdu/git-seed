import { Chart } from "@/components/chat"
import Pychart from "@/components/py-chart"
import { Card, CardTitle, CardDescription, CardContent } from "@/components/ui/card"

const data = {
    totalBloacked: "4.64 MB"
}

const DashboardPage = () => {

    return (
        <div className="flex flex-col w-screen h-full  justify-between gap-10 p-5">

            <div className="h-1/3 w-full flex flex-row justify-between">
                <Pychart />
                <Pychart />
                <Pychart />
                <Pychart />
            </div>

            <div className="h-1/3 w-full flex flex-row justify-between">
                <Card className="w-1/5 h-full flex relative flex-col items-center justify-center gap-10 ">
                    <CardTitle className=" absolute left-3 top-3 text-gray-500"> Total Network Traffic</CardTitle>
                    <CardContent className="text-6xl">{data.totalBloacked}</CardContent>
                    <CardDescription className="text-gray-500">last 24 hours</CardDescription>
                </Card>
                <Chart />
                <Chart />
            </div>

            <div className="h-1/3 w-full flex flex-row justify-between">
                <Card className="w-1/5 h-full flex relative flex-col items-center justify-center gap-10 ">
                    <CardTitle className=" absolute left-3 top-3 text-gray-500"> Total Network Traffic</CardTitle>
                    <CardContent className="text-6xl">{data.totalBloacked}</CardContent>
                    <CardDescription className="text-gray-500">last 24 hours</CardDescription>
                </Card>

                <Card className="w-1/5 h-full flex relative flex-col items-center justify-center gap-10 ">
                    <CardTitle className=" absolute left-3 top-3 text-gray-500"> Total Successfull Requests</CardTitle>
                    <CardContent className="text-6xl">{104}</CardContent>
                    <CardDescription className="text-gray-500">last 24 hours</CardDescription>
                </Card>

                <Card className="w-1/5 h-full flex relative flex-col items-center justify-center gap-10 ">
                    <CardTitle className=" absolute left-3 top-3 text-gray-500"> Total Blocked Requests</CardTitle>
                    <CardContent className="text-6xl text-red-600">{12}</CardContent>
                    <CardDescription className="text-gray-500">last 24 hours</CardDescription>
                </Card>

                <Card className="w-1/5 h-full flex relative flex-col items-center justify-center gap-10 ">
                    <CardTitle className=" absolute left-3 top-3 text-gray-500"> Total Repositories</CardTitle>
                    <CardContent className="text-6xl">{10}</CardContent>
                    <CardDescription className="text-gray-500"></CardDescription>
                </Card>
            </div>

        </div>
    )
}

export default DashboardPage