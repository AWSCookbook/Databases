#!/usr/bin/env python3

from aws_cdk import core

from cdk_aws_cookbook_105.cdk_aws_cookbook_105_stack import CdkAwsCookbook105Stack

app = core.App()
CdkAwsCookbook105Stack(app, "cdk-aws-cookbook-105")

app.synth()
