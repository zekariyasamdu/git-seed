import { AuthContext } from "@/context/auth-context";
import type { NodeChildren } from "@/types/props";
import axios from "axios";
import { useEffect, useMemo, useState } from "react";


export const AuthProvider = ({ children }: Readonly<NodeChildren>) => {
    const [token, setToken_] = useState(localStorage.getItem("token"));


    const setToken = (newToken: string) => {
        setToken_(newToken);
    };

    useEffect(() => {

        const fn = () => {

            if (token) {
                axios.defaults.headers.common["Authorization"] = "Bearer " + token;
                localStorage.setItem('token', token);

            } else {
                delete axios.defaults.headers.common["Authorization"];
                localStorage.removeItem('token')
            }
        }

        fn()

    }, [token]);

    const contextValue = useMemo(
        () => ({
            token,
            setToken,
        }),
        [token]
    );

    return (
        <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
    );
};

