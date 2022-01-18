variable "rds_id" {
  type        = string
  description = "Type a name for your DB instance. The name must be unique across all DB instances owned by your AWS account in the current AWS Region"
  sensitive   = true
}

variable "rds_db_name" {
  type        = string
  description = "The name of the database to create when the DB instance is created"
  sensitive   = true
}

variable "rds_user" {
  type        = string
  description = "RDS Master username"
  sensitive   = true
}

variable "rds_password" {
  type        = string
  description = "RDS Master password"
  sensitive   = true
}
