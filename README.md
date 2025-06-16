# 🚀 PythonAnywhere Redeploy Action

This GitHub Action automates the redeployment process of a Django application hosted on [PythonAnywhere](https://www.pythonanywhere.com) using SSH.  
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
name: Redeploy to PythonAnywhere

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
          # Optional: specify the SSH host (defaults to ssh.pythonanywhere.com)
          # ssh_host: ssh.eu.pythonanywhere.com

          # Required: your PythonAnywhere username
          username: ${{ secrets.PA_USERNAME }}

          # Required (if no ssh_private_key): your PythonAnywhere password
          # password: ${{ secrets.PA_PASSWORD }}

          # Required (if no password): SSH private key
          ssh_private_key: ${{ secrets.PA_SSH_PRIVATE_KEY }}

          # Required: target working directory on PythonAnywhere
          working_directory: ${{ secrets.PA_WORKING_DIRECTORY }}

          # Required: path to your virtual environment
          venv_directory: ${{ secrets.PA_VENV_DIRECTORY }}

          # Required: path to your WSGI file
          wsgi_file: /var/www/webapp_name_wsgi.py
```
-💡 Use `ssh.pythonanywhere.com` for US accounts or `ssh.eu.pythonanywhere.com` for EU-based accounts.  
🔐 You must provide **at least one** of the following:  `password` or `ssh_private_key`


## Inputs

| Name      | Description | Required | Example |
|-----------|-------------|----------|---------|
| `ssh_host`  | Optional SSH host for PythonAnywhere (default: `ssh.pythonanywhere.com`) | No | `ssh.eu.pythonanywhere.com` |
| `username`  | Your PythonAnywhere username | Yes | `username` |
| `password`  | Your PythonAnywhere password | No | `password` |
| `ssh_private_key`  | SSH private key (optional, but required if `password` is not provided) | No | *contents of your private key* |
| `working_directory`  | Target working directory on PythonAnywhere | Yes | `/home/username/webapp_name` |
| `venv_directory`  | Path to the Python virtual environment | Yes | `/home/username/webapp_name/.venv` |
| `wsgi_file` | Path to the WSGI file to reload the app | Yes | `/var/www/webapp_name_wsgi.py` |
 

## 🔐 Security

Always store sensitive data like credentials and SSH keys as [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets):

- **Recommended secrets**:
  - `username`
  - `password`
  - `ssh_private_key`

These values can expose your account if leaked, even in public forks or workflow logs.

- For paths such as `working_directory`, `venv_directory`, and `wsgi_file`:
  - Using secrets is **optional**.
  - You can define them directly in the YAML file if they do not contain sensitive data and remain consistent across environments.
  - **Using secrets is recommended if:**
    - They include your username
    - You want to keep the configuration more private or flexible

## 📂 Creating GitHub Secrets

1. In your GitHub repository, go to **Settings**
2. Navigate to **Secrets and variables → Actions**
3. Click **New repository secret**
4. Name the secret (e.g., `PA_USERNAME`, `PA_SSH_PRIVATE_KEY`, etc.)
5. Paste the corresponding value

Repeat for each required secret.

> ⚠️ **Do not commit secrets directly into your repository.** Always use GitHub Secrets to store sensitive information.


## 📋 Using an SSH Key (Recommended)

### 1. Generate an SSH key (if you don't have one):

If you don’t already have an SSH key pair for authentication, you can generate one using the following command:

```bash
$ ssh-keygen -t ed25519
```
- When prompted, press Enter to accept the default file location (`~/.ssh/id_ed25519`).

- You may set a passphrase for added security (optional).

### 2. Add the **public key** to PythonAnywhere:

To add the public key to PythonAnywhere, run the following command:

```bash
$ ssh-copy-id <username>@ssh.pythonanywhere.com
```
Enter your PythonAnywhere password when prompted.

> 💡 Use `ssh.eu.pythonanywhere.com` for EU-based accounts.


### 3. Store the **private key** securely:
To store the private key securely, follow these steps:
- Copy the contents of the private key file (.ssh/id_ed25519) running the command 
```bash
cat ~/.ssh/id_ed25519
```
- Create a new secret in your GitHub repository following the instructions in the [Creating GitHub Secrets](#-creating-github-secrets) section.
- Paste the contents of the private key into the secret field.

> 💡 Make sure to keep your private key secure and do not share it with anyone.

For more information on SSH setup, refer to: [SSH Access on PythonAnywhere](https://help.pythonanywhere.com/pages/SSHAccess/)

## ⚠️ Repository Structure

This action is composed of:

- `action.yml`  
Defines the input interface of the GitHub Action (required inputs) and specifies the execution environment. In this case, it sets up execution in a Docker container that runs the `deploy.sh` script.

- `deploy.sh`  
Main script executed inside the container. It uses SSH to connect to PythonAnywhere, performs `git pull`, installs dependencies, runs migrations, collects static files and restarts the web server by touching the `WSGI.py` file.

- `Dockerfile`  
Defines a custom Docker image based on ubuntu, installs the necessary tools for SSH connections, and copies the required scripts. This ensures the environment has all the necessary tools to perform the redeploy process without relying on the host runner.

- `.github/workflows/example.yml`  
Provides an example of how to use the action in a workflow. You can use it as a template or reference when setting up your own deployment workflow.


## 📝 License

This GitHub Action is distributed under the [MIT License](https://github.com/MiguelRizzi/pythonanywhere-deploy-ssh/blob/main/LICENSE).


---

Made with ❤️ to simplify PythonAnywhere deployments.