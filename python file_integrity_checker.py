import hashlib
import os

# Function to calculate the hash of a file using SHA-256.
def calculate_hash(file_path):
    # Create a SHA-256 hash object.
    hasher = hashlib.sha256()
    try:
        # Open the specified file in binary mode to read its content.
        with open(file_path, 'rb') as file:  # 'rb' ensures reading in binary format.
            # Read the file in chunks to efficiently compute the hash for large files.
            while chunk := file.read(8192):  # Read up to 8192 bytes at a time.
                hasher.update(chunk)  # Update the hash object with the chunk.
        return hasher.hexdigest()  # Return the hexadecimal representation of the hash.
    except FileNotFoundError:
        # Handle the case where the file does not exist.
        print(f"[Error] File not found: {file_path}")
        return None
    except PermissionError:
        # Handle insufficient permissions to access the file.
        print(f"[Error] Permission denied: {file_path}")
        return None

# Function to save the hash value of a file into a text file.
def save_hash(file_path, hash_value, hash_file='hashes.txt'):
    # Check if the hash file already exists.
    if not os.path.exists(hash_file):
        # If the file doesn't exist, create it and write the hash value.
        with open(hash_file, 'w') as hf:  # Open in write mode ('w').
            hf.write(f"{file_path} {hash_value}\n")  # Format: file_path hash_value
    else:
        # If the hash file exists, read its contents to avoid duplicate entries.
        with open(hash_file, 'r') as hf:  # Open in read mode ('r').
            lines = hf.readlines()
        # Check if the current file is already listed in the hash file.
        if any(file_path in line for line in lines):  # Avoid duplicate entries.
            return
        # Append the new file's hash value to the hash file.
        with open(hash_file, 'a') as hf:  # Open in append mode ('a').
            hf.write(f"{file_path} {hash_value}\n")

# Function to load previously saved hashes from a hash file.
def load_hashes(hash_file='hashes.txt'):
    # Return an empty dictionary if the hash file doesn't exist.
    if not os.path.exists(hash_file):
        return {}
    try:
        # Read the hash file and convert it into a dictionary.
        with open(hash_file, 'r') as hf:  # Open in read mode ('r').
            return dict(line.strip().split(' ', 1) for line in hf.readlines())
    except ValueError:
        # Handle cases where the hash file has invalid formatting.
        print("[Error] Malformed hashes.txt file.")
        return {}

# Function to verify the integrity of a file by comparing its current hash with a saved hash.
def check_integrity(file_path, saved_hash):
    # Calculate the current hash of the file.
    current_hash = calculate_hash(file_path)
    # Compare the current hash with the saved hash to determine integrity.
    return current_hash == saved_hash

# Main function to monitor files for changes and verify their integrity.
def main():
    print("    File Integrity Checker    ")
    print("Monitoring files for changes...\n")

    # List of files to monitor for changes. Update this list as needed.
    file_to_monitor = ['example.txt', 'kali-linux-2025.1a-vmware-amd64.7z']

    # Name of the hash file used to store previously calculated hash values.
    hash_file = 'hashes.txt'
    # Load previously saved hashes from the hash file.
    saved_hashes = load_hashes(hash_file)

    # Iterate through the list of files to monitor.
    for file in file_to_monitor:
        # Calculate the current hash of the file.
        current_hash = calculate_hash(file)
        if current_hash:  # Ensure the hash calculation was successful.
            print(f"[Hash Value] {file}: {current_hash}")  # Display the hash value.

            if file in saved_hashes:
                # Compare the current hash with the saved hash to verify integrity.
                if check_integrity(file, saved_hashes[file]):
                    print(f"[OK] {file} - File integrity verified ✅")
                else:
                    print(f"[Warning] {file} - File integrity compromised ⚠️")
            else:
                # Save the hash of new files not previously monitored.
                print(f"[New] {file} - Adding to monitoring list...")
                save_hash(file, current_hash, hash_file)

    print("\nHashes saved to 'hashes.txt'.")

# Entry point of the script.
if __name__ == "__main__":
    main()
