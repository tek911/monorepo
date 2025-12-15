#!/bin/bash
# Database Migration Script
# Contains security vulnerabilities for scanner testing

set -e

# VULNERABILITY: Hardcoded database credentials
MYSQL_HOST="db.production.internal"
MYSQL_USER="root"
MYSQL_PASS="mysql_root_password_123"
MYSQL_DB="app_production"

# VULNERABILITY: Insecure temporary file creation
MIGRATION_LOG="/tmp/migration_$$.log"
touch $MIGRATION_LOG
chmod 666 $MIGRATION_LOG  # World-writable!

# VULNERABILITY: Password on command line (visible in ps)
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASS $MYSQL_DB << EOF
    SELECT VERSION();
EOF

# VULNERABILITY: Unquoted variables allowing injection
MIGRATION_FILE=$1
echo "Running migration: $MIGRATION_FILE"

# VULNERABILITY: Command injection via filename
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASS $MYSQL_DB < migrations/$MIGRATION_FILE

# VULNERABILITY: Race condition with temp file
TEMP_SQL=$(mktemp)
cat > $TEMP_SQL << 'EOSQL'
-- Migration script
ALTER TABLE users ADD COLUMN temp_data TEXT;
EOSQL

# VULNERABILITY: Temp file not securely deleted
rm $TEMP_SQL

# VULNERABILITY: Unsafe use of eval for dynamic SQL
SQL_COMMAND=$2
eval "mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASS $MYSQL_DB -e \"$SQL_COMMAND\""

# VULNERABILITY: Storing credentials in environment visible to child processes
export DATABASE_URL="mysql://$MYSQL_USER:$MYSQL_PASS@$MYSQL_HOST/$MYSQL_DB"

# VULNERABILITY: Logging sensitive information
echo "Connected to $DATABASE_URL" >> $MIGRATION_LOG

# VULNERABILITY: Using predictable seed for "random" operations
RANDOM_SUFFIX=$RANDOM
BACKUP_NAME="backup_$RANDOM_SUFFIX.sql"

# VULNERABILITY: World-readable backup with credentials
mysqldump -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASS $MYSQL_DB > /var/backups/$BACKUP_NAME
chmod 644 /var/backups/$BACKUP_NAME

# VULNERABILITY: Command substitution with user input
TABLE_NAME=$3
ROWS=$(mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASS $MYSQL_DB -N -e "SELECT COUNT(*) FROM $TABLE_NAME")
echo "Table $TABLE_NAME has $ROWS rows"

echo "Migration complete"
