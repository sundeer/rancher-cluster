
resource "aws_route53_record" "rancher" {
  zone_id = "ZN1WXKLRSIQUR"
  name = "${var.server_hostname}.${var.server_domain_name}"
  type = "A"
  ttl = "60"
  records = ["${aws_instance.server.public_ip}"]
}

/*resource "aws_route53_record" "dev-ns" {
    zone_id = "${aws_route53_zone.main.zone_id}"
    name = "dev.example.com"
    type = "NS"
    ttl = "30"
    records = [
        "${aws_route53_zone.dev.name_servers.0}",
        "${aws_route53_zone.dev.name_servers.1}",
        "${aws_route53_zone.dev.name_servers.2}",
        "${aws_route53_zone.dev.name_servers.3}"
    ]
}*/
