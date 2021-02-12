#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_401.cdk_aws_cookbook_401_stack import CdkAwsCookbook401Stack


app = core.App()
CdkAwsCookbook401Stack(app, "cdk-aws-cookbook-401")

app.synth()
