import z from "zod"

export const credentialsSchema = z.object({
    adminName: z.string().min(4, "error: minimum length of username input field is 4"),
    password: z.string().min(8, "error: minimum length of password input field is 8")
})
