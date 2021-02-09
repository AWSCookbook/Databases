#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_102.cdk_aws_cookbook_102_stack import CdkAwsCookbook102Stack


app = core.App()
CdkAwsCookbook102Stack(app, "cdk-aws-cookbook-102")

app.synth()
