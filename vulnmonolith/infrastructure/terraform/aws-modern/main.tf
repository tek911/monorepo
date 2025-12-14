# Terraform AWS Modern Configuration (1.x syntax)
# WARNING: INTENTIONALLY VULNERABLE - DO NOT DEPLOY

terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  # VULNERABILITY: No state locking configured
  # backend "s3" { ... }
}

provider "aws" {
  region = var.region

  # VULNERABILITY: Default tags not comprehensive
  default_tags {
    tags = {
      Environment = var.environment
    }
  }
}

variable "region" {
  default = "us-east-1"
}

variable "environment" {
  default = "production"
}

# VULNERABILITY: Sensitive variable with default
variable "database_password" {
  type      = string
  sensitive = true
  default   = "ProductionPassword123!"
}

# VPC Configuration
# VULNERABILITY: No VPC flow logs
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "main-vpc"
  }
}

# VULNERABILITY: Public subnet for sensitive resources
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true # VULNERABILITY
  availability_zone       = "${var.region}a"

  tags = {
    Name = "public-subnet"
  }
}

# S3 Bucket - Modern syntax but still vulnerable
resource "aws_s3_bucket" "logs" {
  bucket = "vulnmonolith-logs-${var.environment}"

  tags = {
    Name = "Logs Bucket"
  }
}

# VULNERABILITY: No encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "logs" {
  bucket = aws_s3_bucket.logs.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256" # Should use KMS
    }
  }
}

# VULNERABILITY: No versioning enabled
resource "aws_s3_bucket_versioning" "logs" {
  bucket = aws_s3_bucket.logs.id

  versioning_configuration {
    status = "Disabled" # VULNERABILITY
  }
}

# VULNERABILITY: Public access not blocked
resource "aws_s3_bucket_public_access_block" "logs" {
  bucket = aws_s3_bucket.logs.id

  block_public_acls       = false # VULNERABILITY
  block_public_policy     = false # VULNERABILITY
  ignore_public_acls      = false # VULNERABILITY
  restrict_public_buckets = false # VULNERABILITY
}

# Lambda Function
# VULNERABILITY: Overly permissive execution role
resource "aws_iam_role" "lambda_role" {
  name = "lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# VULNERABILITY: Lambda has admin access
resource "aws_iam_role_policy_attachment" "lambda_admin" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess" # VULNERABILITY
}

resource "aws_lambda_function" "processor" {
  filename      = "lambda.zip"
  function_name = "data-processor"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "nodejs14.x"

  # VULNERABILITY: Environment variables with secrets
  environment {
    variables = {
      DB_PASSWORD = var.database_password
      API_KEY     = "sk_live_FAKEFAKEFAKEFAKE_NOTREAL"
      JWT_SECRET  = "super-secret-jwt-key"
    }
  }

  # VULNERABILITY: No VPC configuration (can access internet)
  # VULNERABILITY: No reserved concurrency limits
  # VULNERABILITY: No dead letter queue

  tags = {
    Name = "Data Processor"
  }
}

# EKS Cluster
# VULNERABILITY: Public endpoint access
resource "aws_eks_cluster" "main" {
  name     = "vulnmonolith-cluster"
  role_arn = aws_iam_role.eks_cluster.arn

  vpc_config {
    subnet_ids              = [aws_subnet.public.id]
    endpoint_private_access = false          # VULNERABILITY
    endpoint_public_access  = true           # VULNERABILITY
    public_access_cidrs     = ["0.0.0.0/0"] # VULNERABILITY
  }

  # VULNERABILITY: No encryption for secrets
  # encryption_config { ... }

  # VULNERABILITY: No logging enabled
  enabled_cluster_log_types = []
}

resource "aws_iam_role" "eks_cluster" {
  name = "eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  role       = aws_iam_role.eks_cluster.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

# Secrets Manager Secret
# VULNERABILITY: Secret value in Terraform
resource "aws_secretsmanager_secret" "db_credentials" {
  name = "db-credentials"

  # VULNERABILITY: No rotation
  # VULNERABILITY: No KMS key specified
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id

  # VULNERABILITY: Secret value in state file
  secret_string = jsonencode({
    username = "admin"
    password = var.database_password
  })
}

# CloudWatch Log Group
# VULNERABILITY: No encryption, unlimited retention
resource "aws_cloudwatch_log_group" "app_logs" {
  name = "/app/logs"

  # VULNERABILITY: Logs retained forever
  retention_in_days = 0

  # VULNERABILITY: No KMS encryption
}

# API Gateway
resource "aws_api_gateway_rest_api" "main" {
  name = "main-api"

  endpoint_configuration {
    types = ["EDGE"]
  }
}

# VULNERABILITY: No authorization on API Gateway method
resource "aws_api_gateway_method" "root" {
  rest_api_id   = aws_api_gateway_rest_api.main.id
  resource_id   = aws_api_gateway_rest_api.main.root_resource_id
  http_method   = "ANY"
  authorization = "NONE" # VULNERABILITY
}

# Outputs
output "eks_endpoint" {
  value = aws_eks_cluster.main.endpoint
}

output "database_password" {
  value     = var.database_password
  sensitive = true
}
