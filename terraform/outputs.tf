output "server-0 name" {
  value = "${aws_instance.server.public_dns}"
}

output "server-0 ip" {
  value = "${aws_instance.server.public_ip}"
}
