"use client"
import useFetchAuth from "@/hooks/use-fetch-auth";
import { createContext } from "react";

export interface AppUser {
    uid: string;
    email: string | null;
    token: string
}

export interface AuthContextType {
    user: AppUser | null | false;
    loading: boolean;
    login: (email: string,password: string, redirect?: string) => Promise<void>;
    register: (email: string,password: string, redirect?: string) => Promise<void>;
    signout: () => void;
}


export const authContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const authInfo: AuthContextType | undefined = useFetchAuth();
    return <authContext.Provider value={authInfo}>{children}</authContext.Provider>;
}