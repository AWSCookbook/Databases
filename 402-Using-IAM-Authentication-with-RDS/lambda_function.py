import boto3
import botocore
import sys
import pymysql
import logging
import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3 = boto3.resource('s3')
session = boto3.session.Session()


def lambda_handler(event, context):

    rds_host = os.environ["DB_HOST"]
    username = "db_user"
    ssl = {'ca': '/opt/python/rds-combined-ca-bundle.pem'}

    rds_client = session.client(
        service_name='rds',
        region_name=os.environ["AWS_REGION"]
    )

    try:
        auth_token = rds_client.generate_db_auth_token(rds_host, 3306, username)
        logger.info("Got auth token!")
    except botocore.exceptions.ClientError as e:
        logger.error("ERROR: Could not get auth token!")
        logger.error(e)
        sys.exit(e)

    try:
        pymysql.connect(rds_host, user=username, passwd=auth_token, connect_timeout=5, ssl=ssl)
        logger.info("SUCCESS: Connected to the MySQL RDS Database!")
    except pymysql.MySQLError as e:
        logger.error("ERROR: Could not connect to MySQL RDS Database!")
        logger.error(e)
        sys.exit(e)

    return("Successfully connected to RDS with IAM!")
