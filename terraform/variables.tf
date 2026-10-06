variable "aws_region" {
  type        = string
  description = "AWS region for the EC2 instance"
  default     = "ap-south-1"
}
variable "project_name" {
  type    = string
  default = "cropleaf-fa"
}
variable "instance_type" {
  type    = string
  default = "t3.medium"
}
variable "key_name" {
  type        = string
  description = "Existing EC2 key-pair name; private key stays on your laptop"
}
variable "admin_cidr" {
  type        = string
  description = "Your public IP in CIDR form, e.g. 203.0.113.10/32"
}
variable "web_cidrs" {
  type        = list(string)
  description = "Who may reach the web app; 0.0.0.0/0 is normal for a demo"
  default     = ["0.0.0.0/0"]
}
