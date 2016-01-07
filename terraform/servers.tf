/* Create Rancher servers */
resource "aws_instance" "server" {
  count = "${var.server_count}"
  ami = "${lookup(var.rancheros-amis, var.aws_region)}"
  instance_type = "t2.micro"
  subnet_id = "${aws_subnet.public.id}"
  vpc_security_group_ids = [
    "${aws_security_group.default.id}",
    "${aws_security_group.web.id}",
    "${aws_security_group.ssh.id}",
    "${aws_security_group.rancher.id}"
  ]
  key_name = "${aws_key_pair.insecure.key_name}"
  source_dest_check = false
  user_data = "${file(\"./terraform/cloud-config/server.yml\")}"
  tags = {
    Name = "server-${count.index}"
  }
}

/* Load balancer */
/*resource "aws_elb" "app" {
  name = "airpair-example-elb"
  subnets = ["${aws_subnet.public.id}"]
  security_groups = ["${aws_security_group.default.id}", "${aws_security_group.web.id}"]
  listener {
    instance_port = 80
    instance_protocol = "http"
    lb_port = 80
    lb_protocol = "http"
  }
  instances = ["${aws_instance.app.*.id}"]
}*/
