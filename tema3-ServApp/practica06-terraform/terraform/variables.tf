variable "aws_region" {
  description = "Region de AWS"
  type        = string
  default     = "us-east-1"
}

variable "ami_id" {
  description = "ID de la AMI de Ubuntu"
  type        = string
  default     = "ami-0109d2b556bd3d7e1"
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t2.micro"
}
variable "key_name" {
  description = "Nombre de la Key Pair de AWS"
  type        = string
  default     = "practica04"
}