# Migrating Databases to Amazon RDS
## Preparation

This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

### In the root of this Chapter’s repo cd to the  “407-Migrating-Databases-to-Amazon-RDS/cdk-AWS-Cookbook-407” directory and follow the subsequent steps:
```
cd 407-Migrating-Databases-to-Amazon-RDS/cdk-AWS-Cookbook-407/
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cdk deploy
```

### Wait for the cdk deploy command to complete. 

### We created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

`python helper.py`

### For this recipe, you will need to create a modified environment variable from the output: 

`ISOLATED_SUBNETS=$(echo ${ISOLATED_SUBNETS} | tr -d ',"')`

### Navigate up to the main directory for this recipe (out of the “cdk-AWS-Cookbook-407” directory):

`cd ..`

### Execute a lambda to seed the Database with some sample tables:
```
aws lambda invoke \
--function-name $LAMBDA_ARN \
response.json
```


## Clean up 
### Delete the replication task:
```
aws dms delete-replication-task \
--replication-task-arn $REPLICATION_TASK_ARN
```

### After the replication task has finished deleting, delete the replication instance:
```
aws dms delete-replication-instance \
--replication-instance-arn $REP_INSTANCE_ARN
```

### Delete the security group references from the RDS Security Groups:
```
aws ec2 revoke-security-group-ingress \
--protocol tcp --port 3306 \
--source-group $DMS_SG_ID \
--group-id $SOURCE_RDS_SECURITY_GROUP

aws ec2 revoke-security-group-ingress \
--protocol tcp --port 3306 \
--source-group $DMS_SG_ID \
--group-id $TARGET_RDS_SECURITY_GROUP
```

### Detach the DMS policy from the role you created:
```
aws iam detach-role-policy --role-name dms-vpc-role --policy-arn \
arn:aws:iam::aws:policy/service-role/AmazonDMSVPCManagementRole
```

### Delete the role you created for DMS:

`aws iam delete-role --role-name dms-vpc-role`

### Delete the Source and Target DMS endpoints:
```
aws dms delete-endpoint --endpoint-arn $SOURCE_ENDPOINT_ARN
aws dms delete-endpoint --endpoint-arn $TARGET_ENDPOINT_ARN
```

### After the endpoints have been deleted, delete the DMS Security group you created:

`aws ec2 delete-security-group --group-id $DMS_SG_ID`

### Delete the DMS subnet groups:
```
aws dms delete-replication-subnet-group \
--replication-subnet-group-identifier awscookbook407
```

### Go to the cdk-AWS-Cookbook-407 directory:

`cd cdk-AWS-Cookbook-407/`

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Unset the environment variable that you created manually:
```
unset DMS_SG_ID
unset REP_SUBNET_GROUP
unset REP_INSTANCE_ARN
unset RDS_SOURCE_PASSWORD
unset RDS_TARGET_PASSWORD
unset SOURCE_ENDPOINT_ARN
unset TARGET_ENDPOINT_ARN
unset REPLICATION_TASK_ARN
```

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`
