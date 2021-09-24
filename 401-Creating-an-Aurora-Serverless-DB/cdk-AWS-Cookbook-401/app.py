#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_401.cdk_aws_cookbook_401_stack import CdkAwsCookbook401Stack


app = cdk.App()
CdkAwsCookbook401Stack(app, "cdk-aws-cookbook-401")

app.synth()
