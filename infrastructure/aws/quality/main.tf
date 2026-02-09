resource "aws_codebuild_project" "quality_check" {
  name          = "spine-quality-check"
  description   = "Code quality and security scans"
  build_timeout = "5"
  service_role  = var.codebuild_role_arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:5.0"
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"
  }

  source {
    type            = "GITHUB"
    location        = "https://github.com/nerdyfoxco/assistantsemailer.git"
    git_clone_depth = 1

    git_submodules_config {
      fetch_submodules = true
    }
  }

  source_version = "main"

  tags = {
    Environment = "Test"
  }
}

variable "codebuild_role_arn" {
  type = string
}
