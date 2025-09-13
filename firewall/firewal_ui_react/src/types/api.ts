import type { fetchReposResponseSchema, loginResponseSchema } from "@/schema";
import type z from "zod";

export type LoginResponse = z.infer<typeof loginResponseSchema>;
export type fetchReposResponse = z.infer<typeof fetchReposResponseSchema>;