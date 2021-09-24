#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_405.cdk_aws_cookbook_405_stack import CdkAwsCookbook405Stack


app = cdk.App()
CdkAwsCookbook405Stack(app, "cdk-aws-cookbook-405")

app.synth()
