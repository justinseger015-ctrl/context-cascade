#!/bin/bash
# Setup Docker secrets for Ruv-Sparc UI Dashboard
# Security: Generate strong random secrets

set -e

SECRETS_DIR="./docker/secrets"
mkdir -p "$SECRETS_DIR"

echo "Generating Docker secrets..."

# Database credentials
echo "postgres" > "$SECRETS_DIR/db_user.txt"
openssl rand -base64 32 > "$SECRETS_DIR/db_password.txt"

# Redis password
openssl rand -base64 32 > "$SECRETS_DIR/redis_password.txt"

# API secret key
openssl rand -base64 64 > "$SECRETS_DIR/api_secret_key.txt"

# Set restrictive permissions
chmod 600 "$SECRETS_DIR"/*.txt

echo "✓ Secrets generated successfully in $SECRETS_DIR"
echo "⚠️  WARNING: Keep these files secure and DO NOT commit to git!"

# Add to .gitignore
if [ ! -f .gitignore ]; then
    echo "docker/secrets/" >> .gitignore
    echo "*.pem" >> .gitignore
    echo "*.key" >> .gitignore
    echo "*.crt" >> .gitignore
fi

echo "✓ Added secrets directory to .gitignore"
