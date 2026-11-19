terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}


resource "aws_instance" "servidor" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = "practica04"
  vpc_security_group_ids = [aws_security_group.servidor_sg.id]

  tags = {
    Name = "practica06-terraform"
  }
}


resource "aws_security_group" "servidor_sg" {
  name        = "practica06-security-group"
  description = "Security Group para practica06"

  ingress {
    description = "Acceso SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Acceso HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Acceso HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "practica06-security-group"
  }
}
