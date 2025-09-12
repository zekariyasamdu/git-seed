import { useAuth } from "@/hooks/use-auth";
import { Navigate, Outlet } from "react-router-dom";

export const ProtectedRoute = () => {
    const { token } = useAuth();

    if (!token) {
        return <Navigate to="/login" />;
    }

    return <Outlet />;
};
