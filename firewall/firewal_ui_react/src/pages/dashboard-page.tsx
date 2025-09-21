import { Chart } from "@/components/graphs/chat"
import Pychart from "@/components/charts/py-chart"
import CardItem from "@/components/CardItem"
import { useFetchRequestTraffic } from "@/hooks/use-fetch-request-traffic"
import { useFetchBlockedTraffic } from "@/hooks/use-fetch-bloacked-traffic"
import { useFetchTraffic } from "@/hooks/use-fetch-traffic"

const DashboardPage = () => {

    const dataRequestTraffic = useFetchRequestTraffic();
    const dataBlockedTraffic = useFetchBlockedTraffic();
    const dataTraffic = useFetchTraffic();


    const chartData = [

        { month: "January", blocked_requests: 186, successful_requests: 80 },
        { month: "February", blocked_requests: 305, successful_requests: 200 },
        { month: "March", blocked_requests: 237, successful_requests: 120 },
        { month: "April", blocked_requests: 73, successful_requests: 190 },
        { month: "May", blocked_requests: 209, successful_requests: 130 },
        { month: "June", blocked_requests: 214, successful_requests: 140 }

    ]


    return (

        <div className="flex flex-row w-screen h-full p-3">

            <div className="w-1/5 h-full gap-10 flex flex-col justify-center items-center">

                <CardItem className="h-1/5 w-full flex relative flex-col items-center justify-center gap-10" title="Total Blocked Requests" content="10" description="Last 24 hours" warning={true} />
                <CardItem className="h-1/5 w-full flex relative flex-col items-center justify-center gap-10" title="Total Repositories" content="4" description="Last 24 hours" warning={false} />
                <CardItem className="h-1/5 w-full flex relative flex-col items-center justify-center gap-10" title="Total Network Traffic" content="4.6KB" description="Last 24 hours" warning={false} />
                <CardItem className="h-1/5 w-full flex relative flex-col items-center justify-center gap-10" title="Total Successfull Requests" content="104" description="Last 24 hours" warning={false} />

            </div>

            <div className="w-4/5">

                <div className="h-1/2 w-full flex flex-row justify-center gap-25" >

                    <Chart chartData={chartData} className="h-full w-4/5" />

                </div>

                <div className="h-1/2 w-full flex flex-row gap-25 items-center justify-center">

                    <Pychart className="w-fit h-fit flex flex-col justify-center items-center" isLoading={dataRequestTraffic.isLoading} lable="successful requests" title="Successful Requests" analytics={dataRequestTraffic.data} />
                    <Pychart className="w-fit h-fit flex flex-col justify-center items-center" isLoading={dataBlockedTraffic.isLoading} lable="blocked requests" title="Blocked Requests" analytics={dataBlockedTraffic.data} />
                    <Pychart className="w-fit h-fit flex flex-col justify-center items-center" isLoading={dataTraffic.isLoading} lable="Traffic" title="Traffic" analytics={dataTraffic.data} />

                </div>
            </div>
        </div>
    )
}

export default DashboardPage
