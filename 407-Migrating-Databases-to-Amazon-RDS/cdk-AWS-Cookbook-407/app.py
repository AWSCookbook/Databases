#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_407.cdk_aws_cookbook_407_stack import CdkAwsCookbook407Stack


app = cdk.App()
CdkAwsCookbook407Stack(app, "cdk-aws-cookbook-407")

app.synth()
