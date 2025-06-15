# 🚀 PythonAnywhere Redeploy Action

This GitHub Action automates the redeployment process of a Django application hosted on **PythonAnywhere** using SSH.  
It simplifies the workflow of pulling the latest code, installing dependencies, running migrations, and restarting the web server with minimal configuration.   


## ✅ Requirements

Before using this action, make sure that:

- You have a **paid PythonAnywhere account**, as SSH access is only available for paid plans.
- SSH access is enabled on your PythonAnywhere account.
- Your Django project is deployed on PythonAnywhere and cloned via Git.


## 📦 What does this action do?

- Connects to PythonAnywhere via SSH  
- Pulls the latest code from the `main` branch  
- Installs Python dependencies with `pip`  
- Runs `collectstatic` and `migrate`  
- Restarts the web server by touching the `WSGI` file


## 🛠️ Usage

### Workflow example

```yaml
name: Deploy to PythonAnywhere

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Redeploy to PythonAnywhere
        uses: MiguelRizzi/pythonanywhere-deploy-ssh@v1.0.0
        with:
          ssh_host: ssh.eu.pythonanywhere.com # Optional - defaults to ssh.pythonanywhere.com
          username: ${{ secrets.PA_USERNAME }}
          password: ${{ secrets.PA_PASSWORD }}
          working_directory: ${{ secrets.PA_WORKING_DIRECTORY }}
          venv_directory: ${{ secrets.PA_VENV_DIRECTORY }}
          wsgi_file: /var/www/webapp_name_wsgi.py
```

## Inputs

| Name      | Description | Required | Example |
|-----------|-------------|----------|---------|
| `ssh_host`  | Optional SSH host for PythonAnywhere (default: `ssh.pythonanywhere.com`) | No | `ssh.eu.pythonanywhere.com` |
| `username`  | Your PythonAnywhere username | Yes | `username` |
| `password`  | Your PythonAnywhere password | Yes | `password` |
| `working_directory`  | Target working directory on PythonAnywhere | Yes | `/home/username/webapp_name` |
| `venv_directory`  | Path to the Python virtual environment | Yes | `/home/username/webapp_name/.venv` |
| `wsgi_file` | Path to the WSGI file to reload the app | Yes | `/var/www/webapp_name_wsgi.py` |


## 🔐 Security

- **Always** use secrets for:
  - `username`
  - `password`
  - any sensitive tokens or credentials

These values can expose your account if leaked, even in public forks or workflow logs.

- For paths such as `working_directory`, `venv_directory`, and `wsgi_file`:
  - Using secrets is **optional**.
  - You can define them directly in the YAML file if they do not contain sensitive data and remain consistent across environments.
  - **Using secrets is recommended if:**
    - They include your username
    - You want to keep the configuration more private or flexible


## 📁 Repository Structure

This action is composed of:

- `action.yml`  
Defines the input interface of the GitHub Action (required inputs) and specifies the execution environment. In this case, it sets up execution in a Docker container that runs the `deploy.sh` script.

- `deploy.sh`  
Main script executed inside the container. It uses `sshpass` to connect to PythonAnywhere via SSH, performs `git pull`, installs dependencies, runs migrations, and restarts the web server by touching the `WSGI.py` file.

- `Dockerfile`  
Defines a custom Docker image based on `ubuntu`, installs `sshpass`, and copies the required scripts. This ensures the environment has all necessary tools to perform the redeploy process without relying on the host runner.

- `.github/workflows/example.yml`  
Provides an example of how to use the action in a workflow. You can use it as a template or reference when setting up your own deployment workflow.


## 📝 License

This GitHub Action is distributed under the [MIT License](https://github.com/MiguelRizzi/pythonanywhere-deploy-ssh/blob/main/LICENSE).
