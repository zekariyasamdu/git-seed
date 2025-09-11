import z from 'zod';
import { credentialsSchema } from './schema';

export interface Ilayout {
    children: React.ReactNode
}

export type Icredentials = z.infer<typeof credentialsSchema>