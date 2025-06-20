import paramiko
import tempfile


class SSHDeployer:
    def __init__(self, host, username, password=None, private_key=None):
        self.host = host
        self.username = username
        self.password = password
        self.private_key = private_key
        self.client = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.private_key:
            # Autenticación por clave privada
            key_file = tempfile.NamedTemporaryFile(delete=False, mode="w")
            key_file.write(self.private_key)
            key_file.close()

            key = paramiko.RSAKey.from_private_key_file(key_file.name)

            self.client.connect(
                hostname=self.host,
                username=self.username,
                pkey=key
            )
        elif self.password:
            # Autenticación por contraseña
            self.client.connect(
                hostname=self.host,
                username=self.username,
                password=self.password
            )
        else:
            raise ValueError("Either password or private key must be provided.")

    def run(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        out = stdout.read().decode()
        err = stderr.read().decode()
        if err:
            print(f"[stderr] {err}")
        return out.strip()

    def close(self):
        if self.client:
            self.client.close()
