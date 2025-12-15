# Legacy Makefile with security vulnerabilities

# VULNERABILITY: Hardcoded credentials
DB_HOST := prod-db.internal
DB_USER := root
DB_PASS := makefile_db_password_123
AWS_KEY := AKIAIOSFODNN7EXAMPLE
AWS_SECRET := wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# VULNERABILITY: Absolute paths that may not exist
BUILD_DIR := /opt/build
DEPLOY_DIR := /var/www/production

.PHONY: all build test deploy clean

all: build test deploy

# VULNERABILITY: Command injection via VERSION variable
build:
	@echo "Building version $(VERSION)"
	javac -d $(BUILD_DIR) src/*.java
	# VULNERABILITY: Unquoted variable
	tar -czf release-$(VERSION).tar.gz $(BUILD_DIR)

# VULNERABILITY: Executing user-provided test command
test:
	$(TEST_COMMAND)

# VULNERABILITY: Downloading and executing remote scripts
setup:
	curl -s http://setup.example.com/install.sh | bash
	wget -O - http://deps.example.com/deps.sh | sh

# VULNERABILITY: SSH with password in command (visible in process list)
deploy:
	sshpass -p '$(DEPLOY_PASSWORD)' scp -r $(BUILD_DIR)/* deploy@prod:/app/
	sshpass -p '$(DEPLOY_PASSWORD)' ssh deploy@prod 'chmod -R 777 /app'

# VULNERABILITY: SQL injection via QUERY variable
db-query:
	mysql -h $(DB_HOST) -u $(DB_USER) -p$(DB_PASS) -e "$(QUERY)"

# VULNERABILITY: Hardcoded tokens in curl
notify:
	curl -X POST https://api.slack.com/webhook/xxx \
		-H "Authorization: Bearer xoxb-slack-token-12345" \
		-d '{"text": "Deployment complete"}'

# VULNERABILITY: World-writable temporary files
temp-build:
	mkdir -p /tmp/build-$$$$
	chmod 777 /tmp/build-$$$$
	cp -r src/* /tmp/build-$$$$/

# VULNERABILITY: Using eval
run-hook:
	eval "$(PRE_BUILD_HOOK)"
	$(MAKE) build
	eval "$(POST_BUILD_HOOK)"

clean:
	rm -rf $(BUILD_DIR)/*
	rm -rf /tmp/build-*
