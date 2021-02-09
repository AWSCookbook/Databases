#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_107.cdk_aws_cookbook_107_stack import CdkAwsCookbook107Stack


app = core.App()
CdkAwsCookbook107Stack(app, "cdk-aws-cookbook-107")

app.synth()
