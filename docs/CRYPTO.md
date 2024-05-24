# Cryptography

An overview of the decisions made in the design of this file sharing system w.r.t. cryptography.

## Authentication

- Users register with a password (hashed with Argon2id) and a RSA public key us stored in the db. Their keys are saved in the `.cartel` directory.

## Authorisation

## Data at Rest

## Data in Transit
