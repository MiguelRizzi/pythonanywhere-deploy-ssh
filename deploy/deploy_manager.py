from .logger import logger

class DeployManager:
    def __init__(self, ssh, workdir, venvdir, wsgi):
        self.ssh = ssh
        self.workdir = workdir
        self.venv = f"source {venvdir}/bin/activate"
        self.wsgi = wsgi
        self.prev_commit = ""

    def post_pull_tasks(self, changes):
        def changed(path): return any(path in f for f in changes)

        if changed("requirements.txt"):
            logger.info("requirements.txt changed. Installing dependencies...")
            self.ssh.exec(f"cd {self.workdir} && {self.venv} && pip install -r requirements.txt")
        
        if any("models.py" in f or f.startswith("migrations/") for f in changes):
            logger.info("Model or migration changes detected. Running migrations...")
            self.ssh.exec(f"cd {self.workdir} && {self.venv} && python manage.py makemigrations")
            self.ssh.exec(f"cd {self.workdir} && {self.venv} && python manage.py migrate")

        if any("static" in f for f in changes):
            logger.info("Static files changed. Running collectstatic...")
            self.ssh.exec(f"cd {self.workdir} && {self.venv} && python manage.py collectstatic --noinput")
        
        logger.info("Running tests...")
        out, err = self.ssh.exec(f"cd {self.workdir} && {self.venv} && python manage.py test")
        if err and not "Ran 0 tests" in err:
            logger.error("Tests failed")
            raise Exception(err)
        else:
            logger.info("Tests passed successfully.")

    def get_changed_files(self):
        out, _ = self.ssh.exec(f"cd {self.workdir} && git rev-parse HEAD")
        self.prev_commit = out.strip()
        logger.info(f"Previous commit: {self.prev_commit}")

        logger.info("Checking for changes in the remote repository...")
        self.ssh.exec(f"cd {self.workdir} && git fetch origin")
        out, _ = self.ssh.exec(f"cd {self.workdir} && git diff --name-only origin/main..HEAD")
        return out.splitlines()

    def rollback_to_previous_commit(self):
        logger.warning("Rolling back to previous commit...")
        self.ssh.exec(f"cd {self.workdir} && git reset --hard {self.prev_commit}")

    def deploy(self):
        try:
            changes = self.get_changed_files()
            if changes:
                logger.info("Changed files:\n  " + "\n  ".join(changes))
                self.ssh.exec(f"cd {self.workdir} && git pull origin main")
                logger.info("Pulled latest changes from remote repository.")
                try:
                    self.post_pull_tasks(changes)
                except Exception:
                    logger.exception("Error during post-pull tasks")
                    self.rollback_to_previous_commit()
                    logger.warning("Rolled back due to test failure.")
                    raise
            else:
                logger.info("No files changed.")

            logger.info("Reloading application (touch WSGI)...")
            self.ssh.exec(f"touch {self.wsgi}")
            logger.info("Deployment completed successfully!")

        except Exception:
            logger.exception("Error during deployment")
            self.rollback_to_previous_commit()
            raise