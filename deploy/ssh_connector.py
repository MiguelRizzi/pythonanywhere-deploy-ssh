import paramiko
import os
import tempfile
from .logger import logger

class SSHConnector:
    def __init__(self, hostname, port, username, password=None, key_filename=None, private_key_str=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.private_key_str = private_key_str
        self.client = None

    def connect(self):
        try:
            logger.info(f"Connecting to {self.hostname} on port {self.port}...")
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if self.private_key_str:
                logger.info("Using private key for authentication.")
                with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp_key:
                    tmp_key.write(self.private_key_str)
                    tmp_key_path = tmp_key.name
                try:
                    self.client.connect(
                        self.hostname,
                        port=self.port,
                        username=self.username,
                        key_filename=tmp_key_path
                    )
                finally:
                    os.remove(tmp_key_path)
            else:
                logger.info("Using password authentication.")
                self.client.connect(
                    self.hostname,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                )
            logger.info("Connected to the SSH server successfully.")
        except Exception:
            logger.exception("Connection failed")
            self.client = None
            raise

    def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("Disconnected from the SSH server.")

    def exec(self, command):
        if not self.client:
            logger.error("Not connected to SSH server.")
            raise Exception("Not connected to SSH server.")
        logger.info(f"Executing command: {command}")
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            out = stdout.read().decode()
            err = stderr.read().decode()
            if out:
                logger.info(f"STDOUT: {out}")
            if err:
                logger.warning(f"STDERR: {err}")
            return out, err
        except Exception:
            logger.exception(f"Failed to execute command: {command}")
            raise