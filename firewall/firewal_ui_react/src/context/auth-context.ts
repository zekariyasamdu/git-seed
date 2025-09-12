import { createContext } from "react";

export const AuthContext = createContext<{
    token: string | null,
    setToken: (token: string) => void
}>({
    token: null,
    setToken: () => { }
});