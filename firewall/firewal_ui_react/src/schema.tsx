import z from "zod"

export const credentialsSchema = z.object({
    adminName: z.string().min(4, " minimum length of username input field is 4"),
    password: z.string().min(8, " minimum length of password input field is 8")
})


export const loginResponseSchema = z.object({
    access_token: z.string(),
    token_type: z.literal("bearer"),
    user_id: z.string().or(z.number()),
});

export const fetchReposResponseSchema = z.object({
    id: z.int(),
    name: z.string()
})