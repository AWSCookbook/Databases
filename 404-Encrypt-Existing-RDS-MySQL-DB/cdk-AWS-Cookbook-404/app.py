#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_404.cdk_aws_cookbook_404_stack import CdkAwsCookbook404Stack


app = cdk.App()
CdkAwsCookbook404Stack(app, "cdk-aws-cookbook-404")

app.synth()
