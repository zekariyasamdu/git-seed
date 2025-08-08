import * as crypto from 'crypto';


// Convert password to 32-byte key using SHA-256
export function getKeyFromPassword(password: string) {
  return crypto.createHash('sha256').update(password).digest();
}
