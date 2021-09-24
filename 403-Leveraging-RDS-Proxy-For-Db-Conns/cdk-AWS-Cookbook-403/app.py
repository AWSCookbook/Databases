#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_403.cdk_aws_cookbook_403_stack import CdkAwsCookbook403Stack


app = cdk.App()
CdkAwsCookbook403Stack(app, "cdk-aws-cookbook-403")

app.synth()
