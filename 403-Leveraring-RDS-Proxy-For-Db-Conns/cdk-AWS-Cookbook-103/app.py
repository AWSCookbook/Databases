#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_103.cdk_aws_cookbook_103_stack import CdkAwsCookbook103Stack


app = core.App()
CdkAwsCookbook103Stack(app, "cdk-aws-cookbook-103")

app.synth()
