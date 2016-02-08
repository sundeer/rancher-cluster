/* Setup aws provider */
provider "aws" {
  access_key  = "${var.aws_access_key}"
  secret_key  = "${var.aws_secret_key}"
  region      = "${var.aws_region}"
}

/* Define vpc */
resource "aws_vpc" "rancher" {
  cidr_block = "${var.vpc_cidr.octet_1}.${var.vpc_cidr.octet_2}.${var.vpc_cidr.octet_3}.${var.vpc_cidr.octet_4}/${var.vpc_cidr.mask}"
  enable_dns_support = true
  enable_dns_hostnames = true

  tags {
    Name = "${var.vpc_name}"
  }
}

variable "temp" {
  default = "10"
}
