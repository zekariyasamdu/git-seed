"use server"

import { createSession, deleleSession } from "@/lib/session";
import { credentialsSchema } from "@/schema"
import { redirect } from "next/navigation";
const testUser = {
    id: "1",
    user: "root",
    password: "12345678"
}
export async function login(prevState: unknown, formData: FormData) {

    const values = {
        adminName: formData.get("adminName") as string,
        password: formData.get("password") as string,
    }

    const result = credentialsSchema.safeParse(values);

    if (!result.success) {
        return {
            error: result.error.flatten().fieldErrors,
        }
    }

    const { adminName, password } = result.data

    if (adminName !== testUser.user || password !== testUser.password) {
        return {
            error: {
                adminName: ["Invalied Credentials"]
            }
        }
    }
    await createSession(testUser.id)
    redirect("/dashboard")

}

export async function logout() {
    await deleleSession()
    redirect("/login")
}