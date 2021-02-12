#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_403.cdk_aws_cookbook_403_stack import CdkAwsCookbook403Stack


app = core.App()
CdkAwsCookbook403Stack(app, "cdk-aws-cookbook-403")

app.synth()
