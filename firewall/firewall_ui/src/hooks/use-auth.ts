import { Icredentials } from "@/types";
import { useState } from "react";

export default function useAuth() {
    const [user, setUser] = useState();
    const [loading, setLoading] = useState(false)
    const [islogedin, setIslogedin] = useState(false);

    function login(credentials: Icredentials) {

    }

    function signUp(credentials: Icredentials) {

    }

    return {
        login,
        user,
        loading
    }
} 