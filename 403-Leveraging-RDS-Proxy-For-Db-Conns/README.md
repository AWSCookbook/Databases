# Leveraring RDS Proxy For Database Connections
## Preparation
This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

### In the root of this Chapter’s repo cd to the “403-Leveraging-RDS-Proxy-For-Db-Conns/cdk-AWS-Cookbook-403” directory and follow the subsequent steps: 
```
cd 403-Leveraging-RDS-Proxy-For-Db-Conns/cdk-AWS-Cookbook-403/
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cdk deploy
```

### Wait for the cdk deploy command to complete. 

### We created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

`python helper.py`

### Navigate up to the main directory for this recipe (out of the “cdk-AWS-Cookbook-403” directory):

`cd ..`

### For this recipe, you will need to create a modified environment variable from the output:

`ISOLATED_SUBNETS=$(echo ${ISOLATED_SUBNETS} | tr -d ',"')`


## Clean up 
### Delete the RDS DB Proxy:

`aws rds delete-db-proxy --db-proxy-name $DB_NAME`

### The proxy will take some time to delete, monitor the deletion status with this command:
```
aws rds describe-db-proxies --db-proxy-name $DB_NAME \
    --query DBProxies[0].Status
```

### The Elastic Network Interfaces for the RDS DB Proxy will remain, use this command to delete the associated network interfaces (answer ‘y’ to any that are found to delete): 
```
aws ec2 describe-network-interfaces \
--filters Name=group-id,Values=$RDS_PROXY_SG_ID \
--query NetworkInterfaces[*].NetworkInterfaceId \
--output text | tr '\t' '\n' | xargs -p -I % \
aws ec2 delete-network-interface --network-interface-id %
```

### Revoke security group authorization for RDS Proxy
```
aws ec2 revoke-security-group-ingress \
--protocol tcp --port 3306 \
--source-group $RDS_PROXY_SG_ID \
--group-id $RDS_SECURITY_GROUP


aws ec2 revoke-security-group-ingress \
--protocol tcp --port 3306 \
--source-group $DB_APP_FUNCTION_SG_ID \
--group-id $RDS_PROXY_SG_ID
```

### Delete the security group you created for RDS Proxy:

`aws ec2 delete-security-group --group-id $RDS_PROXY_SG_ID`

### Detach the AWSCookbook403RdsIamPolicy policy from the Lambda role:
```
aws iam detach-role-policy --role-name $DB_APP_FUNCTION_ROLE_NAME \
--policy-arn arn:aws:iam::$AWS_ACCOUNT_ID:policy/AWSCookbook403RdsIamPolicy
```

### Delete the AWSCookbook403RdsIamPolicy policy: 

`aws iam delete-policy --policy-arn arn:aws:iam::$AWS_ACCOUNT_ID:policy/AWSCookbook403RdsIamPolicy`

### Detach the SecretsManager policy from the RDS Proxy role:
```
aws iam detach-role-policy --role-name AWSCookbook403RDSProxy \
--policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite
```

### Delete the IAM Role for the proxy:

`aws iam delete-role --role-name AWSCookbook403RDSProxy`

### Go to the cdk-AWS-Cookbook-403 directory:

`cd cdk-AWS-Cookbook-403/`

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Unset the environment variable that you created manually: 
```
unset RDS_PROXY_SG_ID
unset RDS_PROXY_ENDPOINT_ARN
unset RDS_PROXY_ENDPOINT
unset DB_RESOURE_ID
unset RDSProxyID
```

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`


