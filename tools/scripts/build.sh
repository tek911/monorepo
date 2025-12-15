#!/bin/bash
# Build Script
# Contains security vulnerabilities for scanner testing

# VULNERABILITY: Hardcoded tokens
GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
NPM_TOKEN="npm_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
DOCKER_PASSWORD="docker_registry_password"
SONAR_TOKEN="sqp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Export tokens (visible to all child processes)
export GITHUB_TOKEN
export NPM_TOKEN

# VULNERABILITY: Path traversal via user input
BUILD_DIR=$1
SOURCE_DIR=$2

# VULNERABILITY: No validation, allows ../../../ paths
echo "Building from $SOURCE_DIR to $BUILD_DIR"
mkdir -p "$BUILD_DIR"
cp -r "$SOURCE_DIR"/* "$BUILD_DIR/"

# VULNERABILITY: Command injection in build commands
BUILD_FLAGS=$3
npm run build $BUILD_FLAGS

# VULNERABILITY: Insecure download of build tools
curl -o /tmp/tool.tar.gz http://insecure-downloads.example.com/tool.tar.gz
tar -xzf /tmp/tool.tar.gz -C /usr/local/bin/

# VULNERABILITY: Running downloaded binaries without verification
/usr/local/bin/tool --version

# VULNERABILITY: Unsafe .npmrc creation with token
echo "//registry.npmjs.org/:_authToken=$NPM_TOKEN" > ~/.npmrc
chmod 644 ~/.npmrc  # Readable by others

# VULNERABILITY: Docker login with password in command line
echo "$DOCKER_PASSWORD" | docker login registry.example.com -u builder --password-stdin

# VULNERABILITY: Unquoted variable expansion
EXTRA_ARGS=$4
docker build $EXTRA_ARGS -t app:latest .

# VULNERABILITY: Using eval for build configuration
BUILD_CONFIG=$5
eval "$BUILD_CONFIG"

# VULNERABILITY: Insecure git operations
GIT_BRANCH=$6
git checkout $GIT_BRANCH  # Command injection possible
git pull origin $GIT_BRANCH

# VULNERABILITY: Creating world-readable artifacts
BUILD_OUTPUT="/var/builds/$(date +%Y%m%d)"
mkdir -p $BUILD_OUTPUT
cp -r dist/* $BUILD_OUTPUT/
chmod -R 755 $BUILD_OUTPUT

# VULNERABILITY: Logging sensitive tokens
echo "Build completed with token ${GITHUB_TOKEN:0:10}..."

# VULNERABILITY: Hardcoded webhook with token
curl -X POST "https://api.github.com/repos/owner/repo/statuses/$(git rev-parse HEAD)" \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"state":"success","description":"Build passed"}'

echo "Build complete!"
