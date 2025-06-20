import sys
from deployment.ssh import SSHConnector
from deployment.manager import DeploymentManager


def main():
    if len(sys.argv) != 7:
        print("Usage: main.py <ssh_host> <username> <ssh_key> <workdir> <venvdir> <wsgi>")
        sys.exit(1)

    ssh_host, username, password, ssh_key, workdir, venvdir, wsgi = sys.argv[1:]

    ssh = SSHConnector(ssh_host, username, password, ssh_key)
    ssh.connect()

    manager = DeploymentManager(ssh, workdir, venvdir, wsgi)
    try:
        manager.deploy()
    finally:
        ssh.close()


if __name__ == "__main__":
    main()
