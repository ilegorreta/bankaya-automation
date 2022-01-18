resource "aws_db_instance" "rds" {
  identifier                 = var.rds_id
  engine                     = "postgres"
  engine_version             = "13.4"
  instance_class             = "db.t3.micro"
  name                       = var.rds_db_name
  username                   = var.rds_user
  password                   = var.rds_password
  storage_type               = "gp2"
  allocated_storage          = 20
  port                       = 5432
  backup_retention_period    = 0
  max_allocated_storage      = 0
  monitoring_interval        = 0
  skip_final_snapshot        = true
  auto_minor_version_upgrade = true
  delete_automated_backups   = true
  deletion_protection        = false
  publicly_accessible        = true
}
