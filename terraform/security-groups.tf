/* Default security group */
resource "aws_security_group" "default" {
  name = "rancher-vpc-default"
  description = "Default security group that allows inbound and outbound traffic from all instances in the VPC"
  vpc_id = "${aws_vpc.default.id}"

  ingress {
    from_port   = "0"
    to_port     = "0"
    protocol    = "-1"
    self        = true
  }

  egress {
    from_port   = "0"
    to_port     = "0"
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags {
    Name = "Default"
  }
}


/* Security group for ssh */
resource "aws_security_group" "ssh" {
  name = "ssh"
  description = "Security group for instances that allows SSH traffic from internet"
  vpc_id = "${aws_vpc.default.id}"

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = "0"
    to_port     = "0"
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags {
    Name = "ssh"
  }
}

/* Security group for the web */
resource "aws_security_group" "web" {
  name = "web"
  description = "Security group for web that allows web traffic from internet"
  vpc_id = "${aws_vpc.default.id}"

  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 8080
    to_port   = 8080
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags {
    Name = "web"
  }
}

/* Security group for VPN */
resource "aws_security_group" "vpn" {
  name = "vpn"
  description = "Security group for instances that allows vpn traffic from internet"
  vpc_id = "${aws_vpc.default.id}"

  ingress {
    from_port = 1194
    to_port   = 1194
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 2222
    to_port   = 2222
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = "0"
    to_port     = "0"
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags {
    Name = "vpn"
  }
}

/* Security group for rancher */
resource "aws_security_group" "rancher" {
  name = "rancher"
  description = "Security group for instances that allows vpn traffic from internet"
  vpc_id = "${aws_vpc.default.id}"

  ingress {
    from_port = 500
    to_port   = 500
    protocol  = "udp"
    self      = true
  }

  ingress {
    from_port = 4500
    to_port   = 4500
    protocol  = "udp"
    self      = true
  }

  ingress {
    from_port = 2376
    to_port   = 2376
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    /*self      = true*/
  }

  egress {
    from_port   = "0"
    to_port     = "0"
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags {
    Name = "rancher"
  }
}

/* Everything security group */
resource "aws_security_group" "all" {
  name = "rancher-all"
  description = "Wide open for testing"
  vpc_id = "${aws_vpc.default.id}"

  ingress {
    from_port   = "0"
    to_port     = "0"
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = "0"
    to_port     = "0"
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags {
    Name = "all"
  }
}
