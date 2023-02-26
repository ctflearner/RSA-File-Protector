import rsa
import os

# Load the private key from a file
with open("privateKey.pem", "rb") as key_file:
    privateKey = rsa.PrivateKey.load_pkcs1(key_file.read())

# Function to decrypt a file
def decrypt_file(file_path):
    # Open the encrypted file in binary mode
    with open(file_path, "rb") as file:
        # Read the contents of the encrypted file
        encrypted_contents = file.read()
        # Determine the maximum block size for this key
        max_block_size = rsa.common.byte_size(privateKey.n)
        # Decrypt the contents of the file in chunks
        decrypted_contents = b""
        for i in range(0, len(encrypted_contents), max_block_size):
            chunk = encrypted_contents[i:i+max_block_size]
            decrypted_chunk = rsa.decrypt(chunk, privateKey)
            decrypted_contents += decrypted_chunk
    # Write the decrypted contents to a new file
    new_file_path = file_path.rstrip(".encrypted")
    with open(new_file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_contents)
    # Remove the original encrypted file
    os.remove(file_path)

# Function to decrypt all files in a folder
def decrypt_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".encrypted"):
                decrypt_file(os.path.join(root, file_name))

# Prompt the user for a file or folder path
decryption_choice = input("Enter 'f' to decrypt a file or 'd' to decrypt a folder: ")

if decryption_choice == 'f':
    file_path = input("Enter the file path to decrypt: ")
    if os.path.isfile(file_path) and file_path.endswith(".encrypted"):
        decrypt_file(file_path)
    else:
        print("Invalid file path or file is not encrypted.")
elif decryption_choice == 'd':
    folder_path = input("Enter the folder path to decrypt: ")
    if os.path.isdir(folder_path):
        decrypt_folder(folder_path)
    else:
        print("Invalid folder path.")
else:
    print("Invalid choice.")
