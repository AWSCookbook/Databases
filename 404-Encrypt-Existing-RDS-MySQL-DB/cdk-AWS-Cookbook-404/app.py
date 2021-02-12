#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_404.cdk_aws_cookbook_404_stack import CdkAwsCookbook404Stack


app = core.App()
CdkAwsCookbook404Stack(app, "cdk-aws-cookbook-404")

app.synth()
