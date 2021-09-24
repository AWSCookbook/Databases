#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_402.cdk_aws_cookbook_402_stack import CdkAwsCookbook402Stack


app = cdk.App()
CdkAwsCookbook402Stack(app, "cdk-aws-cookbook-402")

app.synth()
