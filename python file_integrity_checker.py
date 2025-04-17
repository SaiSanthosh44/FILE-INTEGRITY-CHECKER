import hashlib
import os


def calculate_hash(file_path):
    
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as file:  # Open the file in binary mode.
            while chunk := file.read(8192):  
                hasher.update(chunk)
        return hasher.hexdigest()  
    except FileNotFoundError:
        print(f"[Error] File not found: {file_path}")
        return None
    except PermissionError:
        print(f"[Error] Permission denied: {file_path}")
        return None

#To save the hash value in a file.
def save_hash(file_path, hash_value, hash_file='hashes.txt'):
    
    if not os.path.exists(hash_file):
        with open(hash_file, 'w') as hf:  
            hf.write(f"{file_path} {hash_value}\n")
    else:
        with open(hash_file, 'r') as hf:
            lines = hf.readlines()
        # Avoid duplicate entries
        if any(file_path in line for line in lines):
            return
        with open(hash_file, 'a') as hf:
            hf.write(f"{file_path} {hash_value}\n")

# To load previously saved hashes.
def load_hashes(hash_file='hashes.txt'):
    
    if not os.path.exists(hash_file):
        return {}
    try:
        with open(hash_file, 'r') as hf:
            return dict(line.strip().split(' ', 1) for line in hf.readlines())
    except ValueError:
        print("[Error] Malformed hashes.txt file.")
        return {}

# To check file integrity.
def check_integrity(file_path, saved_hash):
    
    current_hash = calculate_hash(file_path)
    return current_hash == saved_hash

def main():
    print("    File Integrity Checker    ")
    print("Monitoring files for changes...\n")

    # Files to monitor (Update this list with your file paths).
    file_to_monitor = ['example.txt', 'sample.exe', 'kali-linux-2025.1a-vmware-amd64.7z']

    hash_file = 'hashes.txt'
    saved_hashes = load_hashes(hash_file)

    for file in file_to_monitor:
        current_hash = calculate_hash(file)
        if current_hash:
            print(f"[Hash Value] {file}: {current_hash}")  # Show hash value in terminal.

            if file in saved_hashes:
                # Verify integrity against saved hash.
                if check_integrity(file, saved_hashes[file]):
                    print(f"[OK] {file} - File integrity verified ✅")
                else:
                    print(f"[Warning] {file} - File integrity compromised ⚠️")
            else:
                # Save new hashes if not monitored before.
                print(f"[New] {file} - Adding to monitoring list...")
                save_hash(file, current_hash, hash_file)

    print("\nHashes saved to 'hashes.txt'.")

if __name__ == "__main__":
    main()