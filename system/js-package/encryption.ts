import fs from 'fs';
import crypto from 'crypto'
import { getKeyFromPassword } from "./utils.js";

const algorithm = 'aes-256-cbc';
const ivLength = 16;

// Encrypt a file
export function encryptFile(filename: string | undefined, password: string | undefined) {
  if (!filename || !password) {
    throw new Error("Filename and password must be provided");
  }
  const key = getKeyFromPassword(password);
  const iv = crypto.randomBytes(ivLength);
  const cipher = crypto.createCipheriv(algorithm, key, iv);

  const input = fs.createReadStream(filename);
  const output = fs.createWriteStream(filename + '.enc');

  output.write(iv);

  input.pipe(cipher).pipe(output);

  output.on('finish', () => {
    console.log(`[+] Encrypted: ${filename} -> ${filename}.enc`);
  });
}