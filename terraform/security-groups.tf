/* The Cone of Silence security group */
resource "aws_security_group" "tcos" {
  name = "tcos"
  description = "Allow any inter security group traffic"
  vpc_id = "${aws_vpc.rancher.id}"

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
    Name = "tcos"
  }
}


/* Security group for ssh */
resource "aws_security_group" "ssh" {
  name = "ssh"
  description = "Security group for instances that allow SSH traffic from internet"
  vpc_id = "${aws_vpc.rancher.id}"

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
  vpc_id = "${aws_vpc.rancher.id}"

  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 8080
    to_port   = 8080
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
  vpc_id = "${aws_vpc.rancher.id}"

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
  description = "Rancher only"
  vpc_id = "${aws_vpc.rancher.id}"

  ingress {
    from_port = 500
    to_port   = 500
    protocol  = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 4500
    to_port   = 4500
    protocol  = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 8080
    to_port   = 8080
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
    Name = "rancher"
  }
}

/* Everything security group */
resource "aws_security_group" "all" {
  name = "rancher-all"
  description = "Wide open for testing"
  vpc_id = "${aws_vpc.rancher.id}"

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
