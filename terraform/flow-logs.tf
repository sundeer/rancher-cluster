resource "aws_cloudwatch_log_group" "rancher" {
  name = "Rancher"
  retention_in_days = "30"
}

resource "aws_flow_log" "rancher_vpc" {
  log_group_name = "Rancher"
  iam_role_arn = "${aws_iam_role.test_role.arn}"
  vpc_id = "${aws_vpc.rancher.id}"
  traffic_type = "ALL"
}

resource "aws_iam_role" "test_role" {
    name = "test_role"
    assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "vpc-flow-logs.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "test_policy" {
    name = "test_policy"
    role = "${aws_iam_role.test_role.id}"
    policy = <<EOF
{
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
        "logs:PutLogEvents"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}
