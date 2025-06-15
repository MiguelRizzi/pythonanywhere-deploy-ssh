#!/bin/bash
set -e

USERNAME=$1
PASSWORD=$2
WORKING_DIRECTORY=$3
VENV_DIRECTORY=$4
WSGI_FILE=$5

echo "Connecting to PythonAnywhere server..."

sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USERNAME@ssh.pythonanywhere.com" << EOF
  echo "Changing to working directory..."
  cd "$WORKING_DIRECTORY"
  echo "Activating virtual environment..."
  source "$VENV_DIRECTORY/bin/activate"
  echo "Pulling latest changes from main branch..."
  git pull origin main
  echo "Installing dependencies..."
  pip install -r requirements.txt
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
  echo "Applying migrations..."
  python manage.py migrate
  echo "Touching WSGI file to restart server..."
  touch "$WSGI_FILE"
  echo "Deployment completed successfully!"
EOF
