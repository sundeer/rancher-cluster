resource "aws_key_pair" "insecure" {
  key_name   = "rancher(insecure)-${aws_vpc.default.id}"
  public_key = "${file(\"${path.module}/secrets/ssh/insecure-key.pub\")}"
}
