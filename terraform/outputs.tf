output "public_ip" {
  value       = aws_instance.cropleaf.public_ip
  description = "Use this in ansible/inventory.ini and then open http://<IP>"
}
output "public_dns" {
  value       = aws_instance.cropleaf.public_dns
  description = "Public DNS name of the CropLeaf server"
}
