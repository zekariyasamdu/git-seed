import { useAuth } from "@/hooks/use-auth";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { ProtectedRoute } from "./protectedRoute";
import LoginPage from "@/pages/login-page";
import DashboardPage from "@/pages/dashboard-page";

const Routes = () => {
    const { token } = useAuth();

    const routesForPublic = [
        {}
    ];

    const routesForAuthenticatedOnly = [
        {
            path: "/",
            element: <ProtectedRoute />,
            children: [
                {
                    path: "/",
                    element: <DashboardPage />,
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
