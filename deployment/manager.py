class DeploymentManager:
    def __init__(self, ssh, workdir, venvdir, wsgi):
        self.ssh = ssh
        self.workdir = workdir
        self.venv = f"source {venvdir}/bin/activate"
        self.wsgi = wsgi
        self.prev_commit = ""

    def _changed_files(self):
        return self.ssh.run(f"cd {self.workdir} && git diff --name-only {self.prev_commit} HEAD").splitlines()

    def deploy(self):
        try:
            self.prev_commit = self.ssh.run(f"cd {self.workdir} && git rev-parse HEAD")
            print(f"🔁 Previous commit: {self.prev_commit}")

            self.ssh.run(f"cd {self.workdir} && git pull origin main")
            changes = self._changed_files()
            print("📦 Changed files:\n", "\n".join(changes))

            def changed(path): return any(path in f for f in changes)

            if changed("requirements.txt"):
                print("📦 Installing dependencies...")
                self.ssh.run(f"cd {self.workdir} && {self.venv} && pip install -r requirements.txt")

            if any("models.py" in f or f.startswith("migrations/") for f in changes):
                print("🛠️ Running migrations...")
                self.ssh.run(f"cd {self.workdir} && {self.venv} && python manage.py makemigrations")
                self.ssh.run(f"cd {self.workdir} && {self.venv} && python manage.py migrate")

            if any("static" in f for f in changes):
                print("📂 Collecting static files...")
                self.ssh.run(f"cd {self.workdir} && {self.venv} && python manage.py collectstatic --noinput")

            self.ssh.run(f"touch {self.wsgi}")
            print("✅ Deployment completed.")

        except Exception as e:
            print(f"❌ Error during deploy: {e}")
            print("🔁 Rolling back...")
            self.ssh.run(f"cd {self.workdir} && git reset --hard {self.prev_commit}")
            raise
