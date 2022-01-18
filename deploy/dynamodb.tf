resource "aws_dynamodb_table" "customers-table" {
  name         = "customers_data"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "first_name"
  range_key    = "last_name"

  attribute {
    name = "first_name"
    type = "S"
  }

  attribute {
    name = "last_name"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = false
  }
}

resource "aws_dynamodb_table" "items-table" {
  name         = "items_data"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "title"

  attribute {
    name = "title"
    type = "S"
  }

  attribute {
    name = "price"
    type = "N"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = false
  }
}

resource "aws_dynamodb_table" "items-bought-table" {
  name         = "items_bought_data"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "item"
  range_key    = "customer"

  attribute {
    name = "item"
    type = "S"
  }

  attribute {
    name = "customer"
    type = "S"
  }

  attribute {
    name = "price"
    type = "N"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = false
  }
}
