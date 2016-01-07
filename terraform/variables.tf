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
  default     = "10.99.0.0/16"
}

variable "server_count" {
  description = "Number or Rancher servers to create"
  default = 0
}

variable "server_host_name" {
  description = "Rancher server name"
  default = "b4kk83"
}

variable "server_user_data" {
  description = "Rancher cloud-config server user_data"
  default = "cloud-config/server.yml"
}

variable "host_count" {
  description = "Number or Rancher hosts to create"
  default = 0
}

variable "agent_registration_url" {
  description = ""
  default = ""
}

variable "public_subnet" {
  description = "CIDR for public subnet"
  default     = {
    cidr = "10.99.101.0/24"
    /*az = "us-west-1a"*/
  }
}

variable "private_subnet" {
  description = "CIDR for private subnet"
  default     = {
    cidr = "10.99.1.0/24"
    az = "us-east-1a"
  }
}

variable "test_domain" {
  default = "corngoodness.com"
}

/*variable "stage_domain" {
  default = ".com"
}*/

/* Ubuntu 14.04 amis by region */
variable "ubuntu_amis" {
  description = "Base AMI to launch the instances with"
  default = {
    us-west-1 = "ami-ec87e98c"
    us-east-1 = "ami-d92e6bb3"
    eu-west-1 = "ami-87cb11f4"
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
