/* Public subnet a */
resource "aws_subnet" "public_a" {
  vpc_id            = "${aws_vpc.rancher.id}"
  cidr_block        = "${lookup(var.public_subnet_a, "cidr")}"
  availability_zone = "${lookup(var.public_subnet_a, "az")}"
  map_public_ip_on_launch = true
  depends_on = ["aws_internet_gateway.default"]

  tags { Name = "public_a" }
}

/* Public subnet b */
resource "aws_subnet" "public_b" {
  vpc_id            = "${aws_vpc.rancher.id}"
  cidr_block        = "${lookup(var.public_subnet_b, "cidr")}"
  availability_zone = "${lookup(var.public_subnet_b, "az")}"
  map_public_ip_on_launch = true
  depends_on = ["aws_internet_gateway.default"]

  tags { Name = "public_b" }
}

/* Public subnet d */
resource "aws_subnet" "public_d" {
  vpc_id            = "${aws_vpc.rancher.id}"
  cidr_block        = "${lookup(var.public_subnet_d, "cidr")}"
  availability_zone = "${lookup(var.public_subnet_d, "az")}"
  map_public_ip_on_launch = true
  depends_on = ["aws_internet_gateway.default"]

  tags { Name = "public_d" }
}

/* Public subnet e */
resource "aws_subnet" "public_e" {
  vpc_id            = "${aws_vpc.rancher.id}"
  cidr_block        = "${lookup(var.public_subnet_e, "cidr")}"
  availability_zone = "${lookup(var.public_subnet_e, "az")}"
  map_public_ip_on_launch = true
  depends_on = ["aws_internet_gateway.default"]

  tags { Name = "public_e" }
}

/* Internet gateway for the public subnets */
resource "aws_internet_gateway" "default" {
  vpc_id = "${aws_vpc.rancher.id}"
}

/* Routing table for public subnets */
resource "aws_route_table" "public" {
  vpc_id = "${aws_vpc.rancher.id}"
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.default.id}"
  }

  tags = { Name = "public" }
}

/* Associate the routing table to public subnet a */
resource "aws_route_table_association" "public_a" {
  subnet_id = "${aws_subnet.public_a.id}"
  route_table_id = "${aws_route_table.public.id}"
}

/* Associate the routing table to public subnet b*/
resource "aws_route_table_association" "public_b" {
  subnet_id = "${aws_subnet.public_b.id}"
  route_table_id = "${aws_route_table.public.id}"
}

/* Associate the routing table to public subnet d */
resource "aws_route_table_association" "public_d" {
  subnet_id = "${aws_subnet.public_d.id}"
  route_table_id = "${aws_route_table.public.id}"
}

/* Associate the routing table to public subnet e */
resource "aws_route_table_association" "public_e" {
  subnet_id = "${aws_subnet.public_e.id}"
  route_table_id = "${aws_route_table.public.id}"
}
