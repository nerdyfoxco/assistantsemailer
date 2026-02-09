# EKS Cluster
resource "aws_eks_cluster" "main" {
  name     = "${var.project_name}-cluster"
  role_arn = var.eks_cluster_role_arn

  vpc_config {
    subnet_ids = var.subnet_ids
  }
}

# EKS Node Group
resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "main-nodes"
  node_role_arn   = var.eks_node_role_arn
  subnet_ids      = var.subnet_ids

  scaling_config {
    desired_size = 2
    max_size     = 3
    min_size     = 1
  }

  instance_types = ["t3.medium"]
}

# Lambda Function (Placeholder)
resource "aws_lambda_function" "processor" {
  filename      = "lambda_function_payload.zip"
  function_name = "${var.project_name}-processor"
  role          = var.lambda_role_arn
  handler       = "index.handler"
  runtime       = "nodejs18.x"
  
  # Dummy file for plan validation
  source_code_hash = filebase64sha256("lambda_function_payload.zip")
}
