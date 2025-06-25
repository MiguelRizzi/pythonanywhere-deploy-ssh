import os

from .logger import logger
from .ssh_connector import SSHConnector
from .deploy_manager import DeployManager

def verify_env_variables():
    required_vars = [
        "SSH_HOST", "USERNAME", "WORKING_DIRECTORY", "VENV_DIRECTORY", "WSGI_FILE"
    ]

    missing = [var for var in required_vars if not os.environ.get(var)]
    if missing:
        msg = f"Missing environment variables: {', '.join(missing)}"
        logger.critical(msg)
        raise EnvironmentError(msg)

    if not (os.environ.get("PASSWORD") or os.environ.get("SSH_PRIVATE_KEY")):
        msg = "Neither PASSWORD nor SSH_PRIVATE_KEY is set"
        logger.error(msg)
        raise EnvironmentError(msg)


def main():
    verify_env_variables()
    ssh = SSHConnector(
        hostname=os.environ.get("SSH_HOST"),
        port=22,
        username=os.environ.get("USERNAME"),
        password=os.environ.get("PASSWORD"),
        key_filename=None,
        private_key_str=os.environ.get("SSH_PRIVATE_KEY"),
    )
    try:
        ssh.connect()
        if ssh.client:
            manager = DeployManager(
                ssh,
                workdir=os.environ.get("WORKING_DIRECTORY"),
                venvdir=os.environ.get("VENV_DIRECTORY"),
                wsgi=os.environ.get("WSGI_FILE")
            )
            manager.deploy()
    except Exception:
        logger.exception("Fatal error during deployment")
    finally:
        ssh.disconnect()

if __name__ == "__main__":
    main()