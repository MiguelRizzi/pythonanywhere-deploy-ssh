import sys
from deployment.ssh import SSHConnector
from deployment.manager import DeploymentManager


import sys

def main():
    if len(sys.argv) != 8:
        print("Usage: main.py <ssh_host> <username> <password> <ssh_key> <workdir> <venvdir> <wsgi>")
        sys.exit(1)

    ssh_host, username, password, ssh_key, workdir, venvdir, wsgi = sys.argv[1:]

    # Convierte cadenas vacías a None
    password = password if password else None
    ssh_key = ssh_key if ssh_key else None

    ssh = SSHConnector(ssh_host, username, password, ssh_key)
    ssh.connect()

    manager = DeploymentManager(ssh, workdir, venvdir, wsgi)
    try:
        manager.deploy()
    finally:
        ssh.close()

if __name__ == "__main__":
    main()
