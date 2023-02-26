import rsa

# Generate a new RSA key pair with 2048 bits
publicKey, privateKey = rsa.newkeys(2048)

# Save the public key to a file in PEM format
with open("publicKey.pem", "wb") as f:
    f.write(rsa.PublicKey.save_pkcs1(publicKey))

# Save the private key to a file in PEM format
with open("privateKey.pem", "wb") as f:
    f.write(rsa.PrivateKey.save_pkcs1(privateKey))