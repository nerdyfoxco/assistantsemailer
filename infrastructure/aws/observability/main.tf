resource "aws_cloudwatch_log_group" "api" {
  name              = "/aws/ecs/${var.project_name}-api-${var.environment}"
  retention_in_days = 30
  
  tags = {
    Environment = var.environment
    Application = "API"
  }
}

resource "aws_cloudwatch_log_group" "worker" {
  name              = "/aws/lambda/${var.project_name}-worker-${var.environment}"
  retention_in_days = 30

  tags = {
    Environment = var.environment
    Application = "Worker"
  }
}

resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "${var.project_name}-overview-${var.environment}"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "text"
        x      = 0
        y      = 0
        width  = 24
        height = 3
        properties = {
          markdown = "# System Overview\n${var.project_name} - ${var.environment}"
        }
      }
    ]
  })
}
