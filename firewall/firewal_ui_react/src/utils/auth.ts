import { credentialsSchema, loginResponseSchema } from "@/schema";
import axios from "axios";


export async function login(prevState: unknown, formData: FormData) {

    const values = {
        adminName: formData.get("adminname") as string,
        password: formData.get("password") as string,
    }

    const result = credentialsSchema.safeParse(values);

    if (!result.success) {
        const errorMessages = Object.values(result.error.flatten().fieldErrors)
        console.log(errorMessages[0])
        return {
            error: errorMessages[0]
        }
    }


    const { adminName, password } = result.data
    try {
        const res = await axios.post("http://127.0.0.1:5000/login", {
            admin_name: adminName,
            password: password,
        });

        const parsed = loginResponseSchema.parse(res.data);
        localStorage.setItem('token', parsed.access_token)
        return {
            success: {
                access_token: parsed.access_token
            }
        };
    }
    catch (e) {
        console.error("error", e)
        return { error: "Network error" };
    }



}


export function logout() {
    localStorage.removeItem('token')
}