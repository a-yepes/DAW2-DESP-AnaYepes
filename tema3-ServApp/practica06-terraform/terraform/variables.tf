
variable "aws_region" {
  description = "Region de AWS"
  type        = string
}

variable "ami_id" {
  description = "ID de la AMI de Ubuntu"
  type        = string
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
