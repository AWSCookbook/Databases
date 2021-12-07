from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_s3 as s3,
    aws_s3_deployment,
    aws_iam as iam,
    aws_rds as rds,
    aws_lambda,
    Stack,
    CfnOutput,
    RemovalPolicy
)


class CdkAwsCookbook405Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create s3 bucket
        s3_Bucket = s3.Bucket(
            self,
            "AWS-Cookbook-Recipe-405",
            removal_policy=RemovalPolicy.DESTROY
        )

        aws_s3_deployment.BucketDeployment(
            self,
            'S3Deployment',
            destination_bucket=s3_Bucket,
            sources=[aws_s3_deployment.Source.asset("./s3_content")],
            retain_on_delete=False
        )

        isolated_subnets = ec2.SubnetConfiguration(
            name="ISOLATED",
            subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
            cidr_mask=24
        )

        # create VPC
        vpc = ec2.Vpc(
            self,
            'AWS-Cookbook-VPC',
            cidr='10.10.0.0/23',
            subnet_configuration=[isolated_subnets]
        )

        vpc.add_interface_endpoint(
            'VPCSecretsManagerInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('secretsmanager'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )

        vpc.add_gateway_endpoint(
            's3GateWayEndPoint',
            service=ec2.GatewayVpcEndpointAwsService('s3'),
            subnets=[ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)],
        )

        subnet_group = rds.SubnetGroup(
            self,
            'rds_subnet_group',
            description='VPC Subnet Group for RDS',
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            )
        )

        rds_security_group = ec2.SecurityGroup(
            self,
            'rds_security_group',
            description='Security Group for the RDS Instance',
            allow_all_outbound=True,
            vpc=vpc
        )

        db_name = 'AWSCookbookRecipe405'

        rds_instance = rds.DatabaseInstance(
            self,
            'DBInstance',
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_8_0_23
            ),
            instance_type=ec2.InstanceType("m5.large"),
            vpc=vpc,
            multi_az=False,
            database_name=db_name,
            instance_identifier='awscookbook405db',
            delete_automated_backups=True,
            deletion_protection=False,
            removal_policy=RemovalPolicy.DESTROY,
            allocated_storage=8,
            subnet_group=subnet_group,
            security_groups=[rds_security_group]
        )

        # mkdir -p lambda-layers/sqlparse/python
        # cd layers/sqlparse/python
        # pip install sqlparse --target="."
        # cd ../../../

        # create Lambda Layer to use for RDS Rotation Arn
        pymysql = aws_lambda.LayerVersion(
            self,
            "pymysql",
            code=aws_lambda.AssetCode('lambda-layers/pymysql'),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_8],
            description="pymysql",
            license="MIT"
        )

        # -------- Begin EC2 Helper ---------
        vpc.add_interface_endpoint(
            'VPCSSMInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ssm'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )

        vpc.add_interface_endpoint(
            'VPCEC2MessagesInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ec2messages'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )

        vpc.add_interface_endpoint(
            'VPCSSMMessagesInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ssmmessages'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
        )

        ami = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )

        iam_role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        iam_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM"))

        instance = ec2.Instance(
            self,
            "Instance",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=ami,
            role=iam_role,
            vpc=vpc,
        )

        CfnOutput(
            self,
            'InstanceId',
            value=instance.instance_id
        )
        # -------- End EC2 Helper ---------

        iam_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerReadWrite"))

        rds_instance.connections.allow_from(
            instance.connections, ec2.Port.tcp(3306), "Ingress")

        # outputs

        CfnOutput(
            self,
            'VpcId',
            value=vpc.vpc_id
        )

        CfnOutput(
            self,
            'PyMysqlLambdaLayerArn',
            value=pymysql.layer_version_arn
        )

        CfnOutput(
            self,
            'RdsDatabaseId',
            value=rds_instance.instance_identifier
        )

        CfnOutput(
            self,
            'RdsSecurityGroup',
            value=rds_security_group.security_group_id
        )

        CfnOutput(
            self,
            'RdsEndpoint',
            value=rds_instance.db_instance_endpoint_address
        )

        isolated_subnets = vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)

        CfnOutput(
            self,
            'IsolatedSubnets',
            value=', '.join(map(str, isolated_subnets.subnet_ids))
        )

        CfnOutput(
            self,
            'DbName',
            value=db_name
        )

        CfnOutput(
            self,
            'RdsSecretArn',
            value=rds_instance.secret.secret_full_arn
        )
