import fs from 'fs';
import crypto from 'crypto'


const algorithm = 'aes-256-cbc';
const ivLength = 16;

// Convert password to 32-byte key using SHA-256
function getKeyFromPassword(password) {
  return crypto.createHash('sha256').update(password).digest();
}

// Encrypt a file
function encryptFile(filename, password) {
  const key = getKeyFromPassword(password);
  const iv = crypto.randomBytes(ivLength);
  const cipher = crypto.createCipheriv(algorithm, key, iv);

  const input = fs.createReadStream(filename);
  const output = fs.createWriteStream(filename + '.enc');

  output.write(iv); // write IV to the beginning of the file

  input.pipe(cipher).pipe(output);

  output.on('finish', () => {
    console.log(`[+] Encrypted: ${filename} -> ${filename}.enc`);
  });
}

// Decrypt a file
function decryptFile(filename, password) {
  const key = getKeyFromPassword(password);
  const input = fs.createReadStream(filename);

  let iv;
  let decipher;
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

// --- CLI driver ---
const args = process.argv.slice(2);
const [command, file, key] = args;
if (command === 'encrypt') {
  encryptFile(file, key);
} else if (command === 'decrypt') {
  decryptFile(file, key);
}