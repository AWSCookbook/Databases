import boto3
import botocore
import sys
import pymysql
import logging
import os
import json
import re
import sqlparse
from smart_open import open

logger = logging.getLogger()
logger.setLevel(logging.ERROR)
s3 = boto3.resource('s3')
session = boto3.session.Session()


def exec_sql_parse(cursor, sql_file):
    file = open(sql_file, "rb")
    sql = file.read()
    file.close()

    parsed = sqlparse.split(sql)

    for stmt in parsed:
        parsed_stmt = sqlparse.format(stmt, strip_comments=True).strip()
        if not parsed_stmt.startswith(';') and not re.search(r'flush[ \t]*logs', parsed_stmt):
            logger.info("Parsed Statement: " + parsed_stmt)
            try:
                cursor.execute(parsed_stmt)
            except pymysql.OperationalError as e:
                logger.error("MySQLError OperationalError during execute statement \n\tArgs: " + (str(e.args)))
            except pymysql.ProgrammingError as e:
                logger.error("MySQLError ProgrammingError during execute statement \n\tArgs: " + (str(e.args)))


def lambda_handler(event, context):

    rds_host = ""
    username = ""
    password = ""
    db_name = ""
    s3_bucket = os.environ["S3_BUCKET"]
    secret = os.environ["DB_SECRET_ARN"]
    initial_sql = "employees.sql.gz"
    data_file = ""

    client = session.client(
        service_name='secretsmanager',
        region_name=os.environ["AWS_REGION"]
    )

    try:
        response = client.get_secret_value(SecretId=secret)
        secret = response['SecretString']
        j = json.loads(secret)
        password = j['password']
        db_name = j['dbname']
        username = j['username']
        rds_host = j['host']
    except botocore.exceptions.ClientError as e:
        logger.error("ERROR: Could not get secret!")
        logger.error(e)
        sys.exit(e)

    try:
        conn = pymysql.connect(rds_host, user=username, passwd=password, db=db_name, connect_timeout=5)
        logger.info("SUCCESS: Connected to the MySQL RDS Database!")
    except pymysql.MySQLError as e:
        logger.error("ERROR: Could not connect to MySQL RDS Database!")
        logger.error(e)
        sys.exit(e)

    sql_file = "s3://" + s3_bucket + "/" + initial_sql
    exec_sql_parse(conn.cursor(), sql_file)

    if data_file:
        sql_data_file = "s3://" + s3_bucket + "/" + data_file
        exec_sql_parse(conn.cursor(), sql_data_file)

    with conn.cursor() as cursor:
        cursor.execute("show tables")
        for table_name in cursor:
            logger.info("Table Name: " + str(table_name))
    conn.commit()

    return("SUCCESS!")
