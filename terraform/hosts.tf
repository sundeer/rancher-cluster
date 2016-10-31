# Create Rancher hosts
resource "aws_instance" "host" {
  /*depends_on = ["aws_instance.server"]*/
  count = "${var.host_count}"
  ami = "${lookup(var.rancheros-amis, var.aws_region)}"
  instance_type = "${var.aws_instance_type}"
  subnet_id = "${element(aws_subnet.public.*.id, count.index)}"
  vpc_security_group_ids = [
    "${aws_security_group.tcos.id}",
    "${aws_security_group.web.id}",
    "${aws_security_group.rancher.id}"
  ]
  key_name = "${aws_key_pair.insecure.key_name}"
  source_dest_check = false
  user_data = "${data.template_file.host.rendered}"
  tags = {
    Name = "host-${count.index}"
    environment = "${var.rancher_environment}"
  }
}

data "template_file" "host" {
  template = "${file("${path.module}/templates/host_user_data.tftmpl")}"

  vars {
    rancher_agent_image = "${var.rancher_agent_image}"
    agent_registration_url = "${var.agent_registration_url}"
  }
}

output "hosts" {
  value = "${join(",", aws_instance.host.*.tags.Name)}"
}
