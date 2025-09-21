import type { AnalyticsSchema, fetchReposResponseSchema, loginResponseSchema, MonthlySuccessfulAndBlockedSchema } from "@/schema/api";
import type z from "zod";

export type LoginResponse = z.infer<typeof loginResponseSchema>;
export type fetchReposResponse = z.infer<typeof fetchReposResponseSchema>;
export type Analytics = z.infer<typeof AnalyticsSchema>;
export type MonthlySuccessfulAndBlocked = z.infer<typeof MonthlySuccessfulAndBlockedSchema>