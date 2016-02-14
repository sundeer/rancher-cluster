/* Private subnets */
resource "aws_subnet" "private" {
  vpc_id = "${aws_vpc.rancher.id}"
  count  = "${lookup(var.region_az_count, var.aws_region)}"
  cidr_block = "${var.vpc_cidr.octet_1}.${var.vpc_cidr.octet_2}.${var.private_subnet.octet_3 + count.index}.${var.private_subnet.octet_4}/${var.private_subnet.mask}"
  availability_zone = "${lookup(var.eu_west_1_azs, count.index)}"
  map_public_ip_on_launch = false
  depends_on = ["aws_internet_gateway.default"]

  tags { Name = "private_${lookup(var.subnet_name, count.index)}" }
}
/*
# Routing table for private subnets
resource "aws_route_table" "private" {
  vpc_id = "${aws_vpc.rancher.id}"
  route {
    cidr_block = "0.0.0.0/0"
    instance_id = "${aws_instance.nat.id}"
  }

  tags = { Name = "private" }
}

# Associate the routing table to private subnets
resource "aws_route_table_association" "private" {
  count = "${lookup(var.region_az_count, var.aws_region)}"
  subnet_id = "${element(aws_subnet.private.*.id, count.index)}"
  route_table_id = "${aws_route_table.private.id}"
}*/
