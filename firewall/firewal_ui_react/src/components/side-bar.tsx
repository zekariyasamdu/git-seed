import { Home, CircleUserRound, LayoutList, ChartColumnIncreasing, Inbox, Gitlab, Settings } from "lucide-react"

import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar"
import { SuspenseImage } from "./suspense-image"

// main containt 
const contentItems = [
    {
        title: "Home",
        url: "/",
        icon: Home,
    },
    {
        title: "Logs",
        url: "#",
        icon: ChartColumnIncreasing,
    },
    {
        title: "White List",
        url: "#",
        icon: LayoutList,
    },
    {
        title: "Repositories",
        url: "#",
        icon: Gitlab,
    },
]

// footer containt
const footerItems = [
    {
        title: "Inbox",
        url: "#",
        icon: Inbox,
    },
    {
        title: "Settings",
        url: "#",
        icon: Settings,
    },
    {
        title: "Profile",
        url: "#",
        icon: CircleUserRound,
    },
]

export function AppSidebar() {
    return (
        <Sidebar collapsible="icon">
            <SidebarContent>
                <SidebarGroup>
                    <SidebarGroupLabel className="text-2xl text-black p-1 h-[55px]" >
                        <SuspenseImage
                            src="/src/assets/logo.jpg"
                            width={50}
                            height={50}
                            alt="Company Logo"
                            className="h-[50px] w-[50px]"
                        />
                        INSA Guard
                    </SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            {contentItems.map((item) => (
                                <SidebarMenuItem key={item.title}>
                                    <SidebarMenuButton asChild>
                                        <a href={item.url}>
                                            <item.icon />
                                            <span>{item.title}</span>
                                        </a>
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            ))}
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>

            <SidebarFooter>
                <SidebarMenu>
                    <SidebarMenuItem>
                        {footerItems.map((item) => (
                            <SidebarMenuItem key={item.title}>
                                <SidebarMenuButton asChild>
                                    <a href={item.url}>
                                        <item.icon />
                                        <span>{item.title}</span>
                                    </a>
                                </SidebarMenuButton>
                            </SidebarMenuItem>
                        ))}
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarFooter>
        </Sidebar>
    )
}