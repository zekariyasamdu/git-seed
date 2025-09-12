import type { loginResponseSchema } from "@/schema";
import type z from "zod";

export type LoginResponse = z.infer<typeof loginResponseSchema>;