output "instance_id" {
  description = "ID de la instancia EC2"
  value       = aws_instance.servidor.id
}

output "public_ip" {
  description = "IP publica de la instancia EC2"
  value       = aws_instance.servidor.public_ip
}