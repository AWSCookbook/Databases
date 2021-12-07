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
    RemovalPolicy,
    Duration
)


class CdkAwsCookbook407Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create s3 bucket
        s3_Bucket = s3.Bucket(
            self,
            "AWS-Cookbook-Recipe-407",
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
            'VPCSSMMessagedInterfaceEndpoint',
            service=ec2.InterfaceVpcEndpointAwsService('ssmmessages'),  # Find names with - aws ec2 describe-vpc-endpoint-services | jq '.ServiceNames'
            private_dns_enabled=True,
            subnets=ec2.SubnetSelection(
                one_per_az=False,
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
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

        source_rds_security_group = ec2.SecurityGroup(
            self,
            'source_rds_security_group',
            description='Security Group for the Source RDS Instance',
            allow_all_outbound=True,
            vpc=vpc
        )

        source_db_name = 'AWSCookbookRecipe407Source'

        source_rds_instance = rds.DatabaseInstance(
            self,
            'source_rds_instance',
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_5_7_33
            ),
            instance_type=ec2.InstanceType("m5.large"),
            vpc=vpc,
            multi_az=False,
            database_name=source_db_name,
            instance_identifier='awscookbook407SourceDb',
            delete_automated_backups=True,
            deletion_protection=False,
            # iam_authentication=
            removal_policy=RemovalPolicy.DESTROY,
            allocated_storage=8,
            subnet_group=subnet_group,
            security_groups=[source_rds_security_group]
        )

        source_rds_instance.connections.allow_from(
            instance.connections, ec2.Port.tcp(3306), "Ingress")

        target_rds_security_group = ec2.SecurityGroup(
            self,
            'target_rds_security_group',
            description='Security Group for the Target RDS Instance',
            allow_all_outbound=True,
            vpc=vpc
        )

        target_db_name = 'AWSCookbookRecipe407Target'

        target_rds_instance = rds.DatabaseInstance(
            self,
            'target_rds_instance',
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_5_7_26
            ),
            instance_type=ec2.InstanceType("m5.large"),
            vpc=vpc,
            multi_az=False,
            database_name=target_db_name,
            instance_identifier='awscookbook407TargetDb',
            delete_automated_backups=True,
            deletion_protection=False,
            # iam_authentication=
            removal_policy=RemovalPolicy.DESTROY,
            allocated_storage=8,
            subnet_group=subnet_group,
            security_groups=[target_rds_security_group]
        )

        target_rds_instance.connections.allow_from(
            instance.connections, ec2.Port.tcp(3306), "Ingress")

        # mkdir -p lambda-layers/sqlparse/python
        # cd layers/sqlparse/python
        # pip install sqlparse --target="."
        # cd ../../../

        # create Lambda Layer
        sqlparse = aws_lambda.LayerVersion(
            self,
            "sqlparse",
            code=aws_lambda.AssetCode('lambda-layers/sqlparse'),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_8],
            description="sqlparse",
            license="https://github.com/andialbrecht/sqlparse/blob/master/LICENSE"
        )

        pymysql = aws_lambda.LayerVersion(
            self,
            "pymysql",
            code=aws_lambda.AssetCode('lambda-layers/pymysql'),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_8],
            description="pymysql",
            license="MIT"
        )

        smartopen = aws_lambda.LayerVersion(
            self,
            "smartopen",
            code=aws_lambda.AssetCode('lambda-layers/smart_open'),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_8],
            description="smartopen",
            license="MIT"
        )

        lambda_function = aws_lambda.Function(
            self,
            'LambdaRDS',
            code=aws_lambda.AssetCode("./mysql-lambda/"),
            handler="lambda_function.lambda_handler",
            environment={
                "DB_SECRET_ARN": source_rds_instance.secret.secret_arn,
                "S3_BUCKET": s3_Bucket.bucket_name
            },
            layers=[sqlparse, pymysql, smartopen],
            memory_size=1024,
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            timeout=Duration.seconds(600),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            )
        )

        source_rds_instance.secret.grant_read(lambda_function)

        source_rds_instance.connections.allow_from(
            lambda_function.connections, ec2.Port.tcp(3306), "Ingress")

        s3_Bucket.grant_read(lambda_function)

        # outputs

        CfnOutput(
            self,
            'VpcId',
            value=vpc.vpc_id
        )

        CfnOutput(
            self,
            'InstanceId',
            value=instance.instance_id
        )

        CfnOutput(
            self,
            'SourceRdsDatabaseId',
            value=source_rds_instance.instance_identifier
        )

        CfnOutput(
            self,
            'SourceRdsSecurityGroup',
            value=source_rds_security_group.security_group_id
        )

        CfnOutput(
            self,
            'SourceDbName',
            value=source_db_name
        )

        CfnOutput(
            self,
            'SourceRdsSecretArn',
            value=source_rds_instance.secret.secret_full_arn
        )

        CfnOutput(
            self,
            'SourceRdsEndpoint',
            value=source_rds_instance.db_instance_endpoint_address
        )

        CfnOutput(
            self,
            'TargetRdsDatabaseId',
            value=target_rds_instance.instance_identifier
        )

        CfnOutput(
            self,
            'TargetRdsSecurityGroup',
            value=target_rds_security_group.security_group_id
        )

        CfnOutput(
            self,
            'TargetDbName',
            value=target_db_name
        )

        CfnOutput(
            self,
            'TargetRdsSecretArn',
            value=target_rds_instance.secret.secret_full_arn
        )

        CfnOutput(
            self,
            'TargetRdsEndpoint',
            value=target_rds_instance.db_instance_endpoint_address
        )

        isolated_subnets = vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)

        CfnOutput(
            self,
            'IsolatedSubnets',
            value=', '.join(map(str, isolated_subnets.subnet_ids))
        )

        CfnOutput(
            self,
            'LambdaArn',
            value=lambda_function.function_arn
        )

        CfnOutput(
            self,
            'RdsSourceSecretName',
            value=source_rds_instance.secret.secret_name
        )

        CfnOutput(
            self,
            'RdsTargetSecretName',
            value=target_rds_instance.secret.secret_name
        )
