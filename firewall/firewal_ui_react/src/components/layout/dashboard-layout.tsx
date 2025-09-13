import { AppSidebar } from "@/components/side-bar";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { Outlet } from "react-router-dom";
import { Menu } from "../menu";

export default function DashboardLayout() {
    return (

        <div className="flex">
            <AppSidebar />
            <main className="w-full relative">
                <SidebarTrigger className="absolute" />
                <div className="flex flex-row justify-center ">
                    <Menu />
                </div>
                <Outlet />
            </main>
        </div>
    )
}
