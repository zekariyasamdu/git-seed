import React from "react";
import { useAuth } from "@/hooks/use-auth";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { ProtectedRoute } from "./protectedRoute";
import LoginPage from "@/pages/login-page";
import DashboardLayout from "@/components/layout/dashboard-layout";
import { WhiteListPage } from "@/pages/white-list-page";
import { NotFoundPage } from "@/pages/not-found-page";
const LazyDashboardPage = React.lazy(() => import('@/pages/dashboard-page'))


const Routes = () => {
    const { token } = useAuth();

    const routesForPublic = [
        {
            path: "*",
            element: <NotFoundPage />,
        },
    ];

    const routesForAuthenticatedOnly = [
        {
            path: "/",
            element: <ProtectedRoute />,
            children: [
                {
                    path: "/",
                    element: <DashboardLayout />,
                    children: [
                        {
                            path: '/',
                            element: <React.Suspense fallback={<>loading</>}> <LazyDashboardPage /> </React.Suspense>
                        },
                        {
                            path: '/white-list',
                            element: <WhiteListPage />
                        }
                    ]
                },
            ],
        },
    ];

    const routesForNotAuthenticatedOnly = [
        {
            path: "/login",
            element: <LoginPage />,
        },
    ];

    const router = createBrowserRouter([
        ...routesForPublic,
        ...(!token ? routesForNotAuthenticatedOnly : []),
        ...routesForAuthenticatedOnly,
    ]);

    return <RouterProvider router={router} />;
};

export default Routes;
