import { Chart } from "@/components/graphs/chat"
import Pychart from "@/components/charts/py-chart"
import CardItem from "@/components/CardItem"
import { useFetchRequestTraffic } from "@/hooks/use-fetch-request-traffic"
import { useFetchBloackedTraffic } from "@/hooks/use-fetch-bloacked-traffic"
import { useFetchTraffic } from "@/hooks/use-fetch-traffic"

const DashboardPage = () => {

    const dataRequestTraffic = useFetchRequestTraffic();
    const dataBlockedTraffic = useFetchBloackedTraffic();
    const dataTraffic = useFetchTraffic();

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

                    <Chart className="h-full w-4/5" />

                </div>

                <div className="h-1/2 w-full flex flex-row gap-25 items-center justify-center">

                    <Pychart className="w-fit h-fit flex flex-col justify-center items-center" title="Successful Requests" Data={dataRequestTraffic} />
                    <Pychart className="w-fit h-fit flex flex-col justify-center items-center" title="Blocked Requests" Data={dataBlockedTraffic} />
                    <Pychart className="w-fit h-fit flex flex-col justify-center items-center" title="Traffic" Data={dataTraffic} />

                </div>
            </div>
        </div>
    )
}

export default DashboardPage
