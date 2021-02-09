#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_101.cdk_aws_cookbook_101_stack import CdkAwsCookbook101Stack


app = core.App()
CdkAwsCookbook101Stack(app, "cdk-aws-cookbook-101")

app.synth()
