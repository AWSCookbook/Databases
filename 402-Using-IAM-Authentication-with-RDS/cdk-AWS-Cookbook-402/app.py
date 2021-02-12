#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_402.cdk_aws_cookbook_402_stack import CdkAwsCookbook402Stack


app = core.App()
CdkAwsCookbook402Stack(app, "cdk-aws-cookbook-402")

app.synth()
