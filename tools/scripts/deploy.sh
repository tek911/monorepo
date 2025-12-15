#!/bin/bash
# Deployment Script
# Contains multiple security vulnerabilities for scanner testing

# VULNERABILITY: Hardcoded credentials
AWS_ACCESS_KEY="AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DB_PASSWORD="prod_password_123!"
DEPLOY_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# VULNERABILITY: World-readable credential file creation
echo "AWS_KEY=$AWS_ACCESS_KEY" > /tmp/creds.txt
echo "AWS_SECRET=$AWS_SECRET_KEY" >> /tmp/creds.txt
chmod 644 /tmp/creds.txt  # World-readable!

# VULNERABILITY: Command injection via unquoted variable
ENVIRONMENT=$1
echo "Deploying to $ENVIRONMENT"

# VULNERABILITY: Command injection - unquoted variable in command
docker tag app:latest registry.example.com/app:$ENVIRONMENT
docker push registry.example.com/app:$ENVIRONMENT

# VULNERABILITY: Unsafe eval usage
CONFIG_CMD=$2
eval $CONFIG_CMD

# VULNERABILITY: Command injection in curl
API_ENDPOINT=$3
curl -X POST $API_ENDPOINT/deploy -d "env=$ENVIRONMENT"

# VULNERABILITY: Unvalidated input to shell command
VERSION=$4
ssh deploy@production "cd /app && git checkout $VERSION && ./restart.sh"

# VULNERABILITY: Path traversal possible
LOG_FILE=$5
cat /var/log/app/$LOG_FILE

# VULNERABILITY: Unsafe temporary file
TEMP_SCRIPT="/tmp/deploy_script.sh"
echo "#!/bin/bash" > $TEMP_SCRIPT
echo "docker-compose up -d" >> $TEMP_SCRIPT
chmod +x $TEMP_SCRIPT
$TEMP_SCRIPT

# VULNERABILITY: Downloading and executing remote script
curl -s https://install.example.com/setup.sh | bash

# VULNERABILITY: Unsafe use of find with exec
find /app -name "*.log" -exec rm {} \;

# VULNERABILITY: Using eval with user-controlled data
EXTRA_ARGS="${@:6}"
eval "docker run $EXTRA_ARGS app:latest"

echo "Deployment complete"
