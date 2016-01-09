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
  user_data = "${template_file.server.rendered}"
  tags = {
    Name = "server-${count.index}"
  }
}

resource "template_file" "server" {
  template = "${file("./terraform/templates/server_user_data.tftmpl")}"

  vars {
    hostname = "${var.server_hostname}"
    domain_name = "${var.server_domain_name}"
    letsencrypt_image = "sundeer/com.corngoodness.letsencrypt:latest"
  }
}
