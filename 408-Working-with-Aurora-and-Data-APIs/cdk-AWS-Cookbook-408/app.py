#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_408.cdk_aws_cookbook_408_stack import CdkAwsCookbook408Stack


app = cdk.App()
CdkAwsCookbook408Stack(app, "cdk-aws-cookbook-408")

app.synth()
