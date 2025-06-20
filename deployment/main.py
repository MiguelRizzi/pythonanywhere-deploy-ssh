import sys
from deployment.ssh import SSHConnector
from deployment.manager import DeploymentManager



def main():
    if len(sys.argv) != 8:
        print("Usage: main.py <ssh_host> <username> <password> <ssh_key> <workdir> <venvdir> <wsgi>")
        sys.exit(1)

    ssh_host, username, password, ssh_key, workdir, venvdir, wsgi = sys.argv[1:]

    # En caso de que no uses password, pásalo vacío: ""
    # En caso de que no uses ssh_key, pásalo vacío: ""

    ssh = SSHConnector(ssh_host, username, password if password else None, ssh_key if ssh_key else None)
    ssh.connect()

    manager = DeploymentManager(ssh, workdir, venvdir, wsgi)
    try:
        manager.deploy()
    finally:
        ssh.close()


        
if __name__ == "__main__":
    main()
