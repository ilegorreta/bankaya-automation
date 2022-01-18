variable "rds_id" {
  type        = string
  default     = "bankaya-db-dev"
  description = "Type a name for your DB instance. The name must be unique across all DB instances owned by your AWS account in the current AWS Region"
}

variable "rds_db_name" {
  type        = string
  default     = "bankaya_db"
  description = "The name of the database to create when the DB instance is created"
}

variable "rds_user" {
  type        = string
  default     = "postgres"
  description = "RDS Master username"
}

variable "rds_password" {
  type        = string
  default     = "BankayaTest567"
  description = "RDS Master password"
}
