import { decryptFile } from "./decryption.ts";
import { encryptFile } from "./encryption.ts";


// --- CLI driver ---
const args = process.argv.slice(2);
const [command, file, key] = args;
if (command === 'encrypt') {
  encryptFile(file, key);
} else if (command === 'decrypt') {
  decryptFile(file, key);
}