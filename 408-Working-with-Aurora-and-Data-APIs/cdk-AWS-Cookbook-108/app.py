#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_108.cdk_aws_cookbook_108_stack import CdkAwsCookbook108Stack


app = core.App()
CdkAwsCookbook108Stack(app, "cdk-aws-cookbook-108")

app.synth()
