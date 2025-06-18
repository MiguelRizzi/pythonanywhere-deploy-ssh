#!/bin/bash
set -e

SSH_HOST=$1
USERNAME=$2
PASSWORD=$3
SSH_PRIVATE_KEY=$4
WORKING_DIRECTORY=$5
VENV_DIRECTORY=$6
WSGI_FILE=$7

if [ -z "$USERNAME" ] || [ -z "$WORKING_DIRECTORY" ] || [ -z "$VENV_DIRECTORY" ] || [ -z "$WSGI_FILE" ]; then
  echo "Error: Debes proporcionar USERNAME, WORKING_DIRECTORY, VENV_DIRECTORY y WSGI_FILE."
  exit 1
fi

if [ -z "$PASSWORD" ] && [ -z "$SSH_PRIVATE_KEY" ]; then
  echo "Error: Debes proporcionar al menos PASSWORD o SSH_PRIVATE_KEY."
  exit 1
fi

echo "🌐 Connecting to PythonAnywhere server..."

REMOTE_COMMANDS=$(cat <<EOF
echo "📂 Changing to working directory..."
cd "$WORKING_DIRECTORY"
echo "🐍 Activating virtual environment..."
source "$VENV_DIRECTORY/bin/activate"

echo "⬇️ Pulling latest changes from main branch..."

PREV_HEAD=\$(git rev-parse HEAD)
git pull origin main
CHANGED_FILES=$(git diff --name-only HEAD@{1} HEAD)
echo "Archivos cambiados>>>>>>>>>>>>>>>>: $CHANGED_FILES"
echo "Archivos cambiados:"
echo "\$CHANGED_FILES"



if echo "$CHANGED_FILES" | grep -q '^requirements.txt$'; then
  echo "📦 requirements.txt changed, installing dependencies..."
  pip install -r requirements.txt
else
  echo "📦 requirements.txt not changed, skipping pip install."
fi

echo "DEBUG: CHANGED_FILES:"
printf '%q\n' "$CHANGED_FILES"
echo "$CHANGED_FILES"
echo "🔍 Checking for static-like files changes..."
echo "$CHANGED_FILES" | grep -E -q '.*static.*'
echo "Archivos estáticos cambiados:"
echo "$CHANGED_FILES" | grep -E -q 'static'
if echo "$CHANGED_FILES" | grep -E -q '.*static.*'; then
  echo "🗂️ Static-like files changed, collecting static files..."
  python manage.py collectstatic --noinput
else
  echo "🗂️ Static-like files not changed, skipping collectstatic."
fi


if echo "$CHANGED_FILES" | grep -E -q 'migrations/|.*models.*\.py$'; then
  echo "🛠️ Migration files or models.py changed, applying migrations..."
  python manage.py makemigrations
  python manage.py migrate
else
  echo "🛠️ No migration or models.py changes, skipping migrate."
fi

echo "🔄 Touching WSGI file to restart server..."
touch "$WSGI_FILE"

echo "✅ Deployment completed successfully!"
EOF
)

if [ -n "$SSH_PRIVATE_KEY" ]; then
  echo "$SSH_PRIVATE_KEY" > /tmp/deploy_key
  chmod 600 /tmp/deploy_key
  ssh -i /tmp/deploy_key -o StrictHostKeyChecking=no "$USERNAME@$SSH_HOST" bash -s <<< "$REMOTE_COMMANDS"
  rm /tmp/deploy_key
else
  sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USERNAME@$SSH_HOST" bash -s <<< "$REMOTE_COMMANDS"
fi