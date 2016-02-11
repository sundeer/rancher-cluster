/* Public subnets */
resource "aws_subnet" "public" {
  vpc_id = "${aws_vpc.rancher.id}"
  count  = "${lookup(var.region_az_count, var.aws_region)}"
  cidr_block = "${var.vpc_cidr.octet_1}.${var.vpc_cidr.octet_2}.${var.public_subnet.octet_3 + count.index}.${var.public_subnet.octet_4}/${var.public_subnet.mask}"
  availability_zone = "${lookup(var.us_east_1_azs, count.index)}"
  map_public_ip_on_launch = true
  depends_on = ["aws_internet_gateway.default"]

  tags { Name = "public_${lookup(var.subnet_name, count.index)}" }
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

/* Associate the routing table to public subnets */
resource "aws_route_table_association" "public" {
  count = "${lookup(var.region_az_count, var.aws_region)}"
  subnet_id = "${element(aws_subnet.public.*.id, count.index)}"
  route_table_id = "${aws_route_table.public.id}"
}
