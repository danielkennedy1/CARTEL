# Cryptography

An overview of the decisions made in the design of this file sharing system w.r.t. cryptography.

## Authentication

- Users register with a password and a RSA public key us stored in the db. Their keys are saved in the `.cartel` directory.
    - Password hashing is done with Argon2id, using the `argon2_cffi` library. Uses low memory "SECOND RECOMMENDED" configuration from [RFC 9106 (CFRG)](https://www.rfc-editor.org/rfc/rfc9106.html#section-4-6.2) as the high memory one is 2 GiB.

- Sending a file requires password verification.

- Signature is used to verify the integrity of the file and the sender's posession of the private key.
    - This happens both before it can be persisted to the server and after it is downloaded by the recipient.
    - GCM does its own integrity verification, but we also sign the file to ensure the recipient knows who sent it.

- Password is required to download a file.

## Data at Rest

- Data is encrypted with AES-256-GCM, using the `PyCryptoDome` library.
- You can't decrypt the data without the key, which is sent using the intended recipient's public key so only they can decrypt it.
- Tamper detection is done by verifying the signature of the file and the sender's public key.
- Offline checks: if you connect and your public key is different, you will get an alert and can tell your friends to stop trusting the server.

## Data in Transit

- SSL/TLS is used to secure the connection between the client and server. (requests to port 80 are redirected to 443)

