output "server-0 name" {
  value = "${aws_instance.server.public_dns}"
}

output "server-0 ip" {
  value = "${aws_instance.server.public_ip}"
}

output "host-0" {
  value = "${aws_instance.host.0.public_dns}"
}

output "host-1" {
  value = "${aws_instance.host.1.public_dns}"
}
