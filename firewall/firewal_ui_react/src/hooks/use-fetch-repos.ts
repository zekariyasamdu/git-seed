import { fetchReposResponseSchema } from "@/schema/api";
import type { fetchReposResponse } from "@/types/api";
import axios from "axios";
import { useEffect, useState } from "react";


export default function useFetchRepos() {
    const [isLoading, setIsLoading] = useState(false)
    const [data, setData] = useState<fetchReposResponse | null>(null);
    const [error, setError] = useState("");

    useEffect(() => {
        async function fetchReps() {
            try {

                setIsLoading(true)
                const res = await axios.get('http://127.0.0.1:5000/repos');
                if (res.status == 200) {
                    const checkRep = fetchReposResponseSchema.safeParse(res.data)
                    if (!checkRep.success) {
                        const errorMessages = Object.values(checkRep.error.flatten().fieldErrors)
                        console.log(errorMessages)
                        setError("Invalid response")

                    } else {
                        setData(checkRep.data)
                    }
                    setIsLoading(false)
                    return
                }
                setError("Something went wrong");
                setIsLoading(false)

            } catch (e) {
                setError("Network Error")
                setIsLoading(false)
                throw new Error("Network error", { cause: e })
            }
        }

        fetchReps()
    }, [])


    return {
        isLoading,
        data,
        error
    };
}