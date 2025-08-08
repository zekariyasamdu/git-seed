import * as fs from 'fs';
import * as crypto from 'crypto'
import { getKeyFromPassword } from './utils.ts';

const algorithm = 'aes-256-cbc';
const ivLength = 16;

// Decrypt a file using AES-256-CBC
export function decryptFile(filename: string | undefined, password: string | undefined) {
  if (!filename || !password) {
    throw new Error("Filename and password must be provided");
  }
  const key = getKeyFromPassword(password);
  const input = fs.createReadStream(filename);

  let iv;
  let decipher: crypto.Decipheriv;
  let started = false;

  const outputFilename = filename.replace(/\.enc$/, '');
  const output = fs.createWriteStream(outputFilename);

  input.on('readable', () => {
    if (!started) {
      const chunk = input.read(ivLength);
      if (chunk) {
        iv = chunk;
        decipher = crypto.createDecipheriv(algorithm, key, iv);
        started = true;
      } else {
        return;
      }
    }

    const chunk = input.read();
    if (chunk) {
      const decrypted = decipher.update(chunk);
      output.write(decrypted);
    }
  });

  input.on('end', () => {
    if (decipher) {
      const final = decipher.final();
      output.write(final);
      output.close();
      console.log(`[+] Decrypted: ${filename} -> ${outputFilename}`);
    } else {
      console.error('[-] Failed to decrypt.');
    }
  });
}
