/* Public subnet */
resource "aws_subnet" "public" {
  vpc_id            = "${aws_vpc.rancher.id}"
  cidr_block        = "${lookup(var.public_subnet, "cidr")}"
  /*availability_zone = "${lookup(var.public_subnet, "az")}"*/
  map_public_ip_on_launch = true
  depends_on = ["aws_internet_gateway.default"]

  tags { Name = "public" }
}

/* Internet gateway for the public subnet */
resource "aws_internet_gateway" "default" {
  vpc_id = "${aws_vpc.rancher.id}"
}

/* Routing table for public subnet */
resource "aws_route_table" "public" {
  vpc_id = "${aws_vpc.rancher.id}"
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.default.id}"
  }

  tags = { Name = "public" }
}

/* Associate the routing table to public subnet */
resource "aws_route_table_association" "public" {
  subnet_id = "${aws_subnet.public.id}"
  route_table_id = "${aws_route_table.public.id}"
}
