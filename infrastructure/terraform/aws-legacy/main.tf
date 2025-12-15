# Terraform AWS Legacy Configuration (0.11 syntax)
# WARNING: INTENTIONALLY VULNERABLE - DO NOT DEPLOY

# VULNERABILITY: No required_version constraint
# VULNERABILITY: Using deprecated interpolation syntax

# Provider configuration
# VULNERABILITY: Hardcoded credentials
provider "aws" {
  region     = "us-east-1"
  access_key = "AKIAIOSFODNN7EXAMPLE"
  secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

# VULNERABILITY: No backend configuration (local state)
# terraform {
#   backend "s3" { ... }
# }

# Variables using deprecated syntax
variable "environment" {
  default = "production"
}

variable "db_password" {
  # VULNERABILITY: Default password in variable
  default = "SuperSecretPassword123!"
}

# S3 Bucket
# VULNERABILITY: Public bucket with no encryption
resource "aws_s3_bucket" "data" {
  bucket = "vulnmonolith-data-${var.environment}"

  # VULNERABILITY: Public ACL
  acl = "public-read-write"

  # VULNERABILITY: No versioning
  versioning {
    enabled = false
  }

  # VULNERABILITY: No server-side encryption
  # VULNERABILITY: No logging

  tags {
    Name        = "Data Bucket"
    Environment = "${var.environment}"
  }
}

# S3 Bucket Policy - Public Access
# VULNERABILITY: Allows public access to all objects
resource "aws_s3_bucket_policy" "data_policy" {
  bucket = "${aws_s3_bucket.data.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadWrite",
      "Effect": "Allow",
      "Principal": "*",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::${aws_s3_bucket.data.bucket}/*"
    }
  ]
}
EOF
}

# Security Group
# VULNERABILITY: Allows all inbound traffic
resource "aws_security_group" "app" {
  name        = "app-security-group"
  description = "Application security group"

  # VULNERABILITY: Allows SSH from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # VULNERABILITY: Allows all inbound traffic
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # VULNERABILITY: Allows all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags {
    Name = "app-sg"
  }
}

# RDS Instance
# VULNERABILITY: Publicly accessible, no encryption
resource "aws_db_instance" "database" {
  identifier           = "vulnmonolith-db"
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "appdb"

  # VULNERABILITY: Hardcoded credentials
  username = "admin"
  password = "${var.db_password}"

  # VULNERABILITY: Publicly accessible
  publicly_accessible = true

  # VULNERABILITY: No encryption at rest
  storage_encrypted = false

  # VULNERABILITY: No multi-AZ
  multi_az = false

  # VULNERABILITY: No backup retention
  backup_retention_period = 0

  # VULNERABILITY: Skip final snapshot
  skip_final_snapshot = true

  # VULNERABILITY: No deletion protection
  deletion_protection = false

  vpc_security_group_ids = ["${aws_security_group.app.id}"]

  tags {
    Name = "Main Database"
  }
}

# IAM Role
# VULNERABILITY: Overly permissive IAM policy
resource "aws_iam_role" "app_role" {
  name = "app-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

# VULNERABILITY: Full admin access
resource "aws_iam_role_policy" "app_policy" {
  name = "app-policy"
  role = "${aws_iam_role.app_role.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
EOF
}

# EC2 Instance
# VULNERABILITY: No IMDSv2, public IP, root access
resource "aws_instance" "app" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"

  # VULNERABILITY: Public IP assignment
  associate_public_ip_address = true

  # VULNERABILITY: Root block device not encrypted
  root_block_device {
    encrypted = false
  }

  # VULNERABILITY: User data with secrets
  user_data = <<EOF
#!/bin/bash
echo "DB_PASSWORD=${var.db_password}" >> /etc/environment
echo "AWS_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE" >> /etc/environment
echo "AWS_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" >> /etc/environment
EOF

  vpc_security_group_ids = ["${aws_security_group.app.id}"]
  iam_instance_profile   = "${aws_iam_instance_profile.app_profile.name}"

  tags {
    Name = "App Server"
  }
}

resource "aws_iam_instance_profile" "app_profile" {
  name = "app-profile"
  role = "${aws_iam_role.app_role.name}"
}

# Outputs
# VULNERABILITY: Outputting sensitive values
output "db_password" {
  value = "${var.db_password}"
}

output "db_endpoint" {
  value = "${aws_db_instance.database.endpoint}"
}
