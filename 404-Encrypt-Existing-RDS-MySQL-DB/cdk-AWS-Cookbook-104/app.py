#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_104.cdk_aws_cookbook_104_stack import CdkAwsCookbook104Stack

app = core.App()
CdkAwsCookbook104Stack(app, "cdk-aws-cookbook-104")

app.synth()
