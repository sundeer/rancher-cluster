/* Setup aws provider */
provider "aws" {
  access_key  = "${var.aws_access_key}"
  secret_key  = "${var.aws_secret_key}"
  region      = "${var.aws_region}"
}

/* Define vpc */
resource "aws_vpc" "default" {
  cidr_block = "${var.vpc_cidr}"

  enable_dns_support = true
  enable_dns_hostnames = true

  tags {
    Name = "${var.vpc_name}"
  }
}
