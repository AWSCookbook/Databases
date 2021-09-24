# Recipe Title
## Preparation
This recipe requires some “prep work” that deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

### In the root of this Chapter’s repo cd to the  “401-Creating-an-Aurora-Serverless-DB/cdk-AWS-Cookbook-401” directory and follow the subsequent steps: 
```
cd 401-Creating-an-Aurora-Serverless-DB/cdk-AWS-Cookbook-401/
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cdk deploy
```

### Wait for the cdk deploy command to complete. 

### We created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

`python helper.py`


## Clean up 
### Revoke the access from the instance to that database:
```
aws ec2 revoke-security-group-ingress \
--protocol tcp --port 5432 \
--source-group $INSTANCE_SG \
--group-id $DB_SECURITY_GROUP_ID
```

### Delete the RDS database cluster:
```
aws rds delete-db-cluster \
--db-cluster-identifier awscookbook401dbcluster \
--skip-final-snapshot
```

### Wait for the Status to read “deleted”:
```
aws rds describe-db-clusters \
--db-cluster-identifier awscookbook401dbcluster \
--output text --query DBClusters[0].Status
```
                          
### Delete the RDS Subnet Group: 
```
aws rds delete-db-subnet-group \
--db-subnet-group-name awscookbook401subnetgroup
```

### Delete the security group for the database:
```
aws ec2 delete-security-group \
--group-id $DB_SECURITY_GROUP_ID
```

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Unset the environment variable that you created manually: 
```
unset ADMIN_PASSWORD
unset DB_SECURITY_GROUP_ID
```

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:
`cdk destroy && deactivate && rm -r .venv/ && cd ../..`

