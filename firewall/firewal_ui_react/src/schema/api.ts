import z from "zod"

export const loginResponseSchema = z.object({
    access_token: z.string(),
    token_type: z.literal("bearer"),
    user_id: z.string().or(z.number()),
});

export const fetchReposResponseSchema = z.object({
    id: z.number(),
    name: z.string()
})


const AnalyticsDataSchema = z.object({

    repo_id: z.number(),
    repo_name: z.string(),
    quantity: z.number(),

})

export const AnalyticsSchema = z.object({

    total: z.number(),
    description: z.enum(["blocked", "traffic", "request", ""]),
    period: z.string(),
    data: z.array(AnalyticsDataSchema)

})

export const MonthlySuccessfulAndBlockedSchema = z.object({

    month: z.string(),
    successful_requests: z.number(),
    blocked_requests: z.number()
})