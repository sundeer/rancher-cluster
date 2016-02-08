variable "aws_access_key" {
  description = "AWS access key"
}

variable "aws_secret_key" {
  description = "AWS secert access key"
}

variable "aws_region"     {
  description = "AWS region"
  default     = "us-east-1"
}

variable "vpc_name" {
  default = "rancher"
}

variable "vpc_cidr" {
  description = "CIDR for VPC"
  default = {
    octet_1 = "10"
    octet_2 = "99"
    octet_3 = "0"
    octet_4 = "0"
    mask    = "16"
  }
}

variable "aws_instance_type" {
  description = "Size of aws instance for both the server and hosts"
  default = "t2.small"
}

variable "server_count" {
  description = "Number or Rancher servers to create"
  default = 0
}

variable "server_hostname" {
  description = "Rancher server name"
  default = "b4kk83"
}

variable "server_domain_name" {
  default = "corngoodness.com"
}

/*variable "stage_domain" {
  default = ".com"
}*/

variable "host_count" {
  description = "Number or Rancher hosts to create"
  default = 2
}

variable "agent_registration_url" {
  description = ""
  default = ""
}

variable "rancher_agent_image" {
  description = ""
  default = ""
}

variable "rancher_environment" {
  description = ""
  default = ""
}

variable "region_az_count" {
  default = {
    "us-east-1" = 4
    "eu-west-1" = 3
  }
}

variable "us_east_1_azs" {
  default = {
    "0" = "us-east-1a"
    "1" = "us-east-1b"
    "2" = "us-east-1d"
    "3" = "us-east-1e"
  }
}

variable "eu_west_1_azs" {
  default = {
    "0" = "eu-west-1a"
    "1" = "eu-west-1b"
    "2" = "eu-west-1c"
  }
}

variable "subnet_name" {
  default = {
    "0" = "a"
    "1" = "b"
    "2" = "d"
    "3" = "e"
  }
}

variable "public_subnet" {
  default = {
    octet_3 = "101"
    octet_4 = "0"
    mask    = "24"
  }
}

variable "private_subnet" {
  default = {
    octet_3 = "1"
    octet_4 = "0"
    mask    = "24"
  }
}

/* RanchOS amis by region */
variable "rancheros-amis" {
  description = "Base AMI to launch the instances with"
  default = {
    us-west-1 = "ami-6d2d470d"
    us-east-1 = "ami-53045239" # v0.4.2
    /*us-east-1 = "ami-11740e7b" # v0.4.1
    us-east-1 = "ami-95c09ff0" # v0.4.0*/
    eu-west-1 = "ami-7989240a"
  }
}
