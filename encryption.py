import rsa
import os

# Load the public key from a file
with open("publicKey.pem", "rb") as key_file:
    publicKey = rsa.PublicKey.load_pkcs1(key_file.read())

# Function to encrypt a file
def encrypt_file(file_path):
    # Open the file in binary mode
    with open(file_path, "rb") as file:
        # Read the contents of the file
        file_contents = file.read()
        # Determine the maximum block size for this key
        max_block_size = rsa.common.byte_size(publicKey.n) - 11
        # Encrypt the contents of the file in chunks
        encrypted_contents = b""
        for i in range(0, len(file_contents), max_block_size):
            chunk = file_contents[i:i+max_block_size]
            encrypted_chunk = rsa.encrypt(chunk, publicKey)
            encrypted_contents += encrypted_chunk
    # Write the encrypted contents to a new file
    with open(file_path + ".encrypted", "wb") as encrypted_file:
        encrypted_file.write(encrypted_contents)
    # Remove the original file
    os.remove(file_path)

def encrypt_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if not file_name.endswith(".encrypted"):
                encrypt_file(os.path.join(root, file_name))

# Prompt the user for a file or folder path
encryption_choice = input("Enter 'f' to encrypt a file or 'd' to encrypt a folder: ")

if encryption_choice == 'f':
    file_path = input("Enter the file path to encrypt: ")
    if os.path.isfile(file_path):
        encrypt_file(file_path)
    else:
        print("Invalid file path.")
elif encryption_choice == 'd':
    folder_path = input("Enter the folder path to encrypt: ")
    if os.path.isdir(folder_path):
        encrypt_folder(folder_path)
    else:
        print("Invalid folder path.")
else:
    print("Invalid choice.")
