import { AppSidebar } from "@/components/side-bar";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { Outlet } from "react-router-dom";

export default function DashboardLayout() {
    return (

        <div className="flex">
            <AppSidebar />
            <main className="w-full">
                <SidebarTrigger />
                <Outlet />
            </main>
        </div>
    )
}
