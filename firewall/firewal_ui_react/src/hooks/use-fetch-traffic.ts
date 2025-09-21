import type { Analytics } from "@/types/api";
import { useQuery } from "@tanstack/react-query";
const fetchTraffic = async (): Promise<Analytics> => {
    await new Promise((resolve) => setTimeout(resolve, 500));

    return {
        total: 28450,
        period: "2024-01",
        description: "blocked",
        data: [
            { repo_id: 1, repo_name: "frontend-app", quantity: 12500 },
            { repo_id: 2, repo_name: "backend-api", quantity: 8900 },
            { repo_id: 3, repo_name: "mobile-app", quantity: 4550 },
            { repo_id: 4, repo_name: "data-pipeline", quantity: 1850 },
            { repo_id: 5, repo_name: "documentation", quantity: 650 },
        ],
    };
};

export const useFetchTraffic = () => {

    const query = useQuery({
        queryKey: ["repos"],
        queryFn: fetchTraffic,
        initialData: {
            total: 0,
            period: "",
            description: "",
            data: []
        } as Analytics
    });


    return {
        data: query.data,
        isLoading: query.isLoading,
        isError: query.isError,
        error: query.error,
        isSuccess: query.isSuccess,
    };
};