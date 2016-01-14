# Create Rancher hosts
resource "aws_instance" "host" {
  /*depends_on = ["aws_instance.server"]*/
  count = "${var.host_count}"
  ami = "${lookup(var.rancheros-amis, var.aws_region)}"
  instance_type = "t2.micro"
  subnet_id = "${aws_subnet.public.id}"
  vpc_security_group_ids = [
    "${aws_security_group.default.id}",
    "${aws_security_group.web.id}",
    "${aws_security_group.vpn.id}",
    "${aws_security_group.ssh.id}",
    "${aws_security_group.rancher.id}"
  ]
  key_name = "${aws_key_pair.insecure.key_name}"
  source_dest_check = false
  user_data = "${template_file.host.rendered}"
  tags = {
    Name = "host-${count.index}"
    environment = "${var.rancher_environment}"
  }
}

resource "template_file" "host" {
  template = "${file("${path.module}/templates/host_user_data.tftmpl")}"

  vars {
    rancher_agent_image = "${var.rancher_agent_image}"
    agent_registration_url = "${var.agent_registration_url}"
  }
}

output "hosts" {
  value = "${join(",", aws_instance.host.*.tags.Name)}"
}
