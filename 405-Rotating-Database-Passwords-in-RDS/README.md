# Automating Password Rotation for RDS Databases
## Preparation
This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

### In the root of this Chapter’s repo cd to the “405-Rotating-Database-Passwords-in-RDS/cdk-AWS-Cookbook-405” directory and follow the subsequent steps: 
```
cd 405-Rotating-Database-Passwords-in-RDS/cdk-AWS-Cookbook-405/
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

`ISOLATED_SUBNETS=$(echo ${ISOLATED_SUBNETS} | tr -d ' "')`

### Navigate up to the main directory for this recipe (out of the “cdk-AWS-Cookbook-405” directory):

`cd ..`


## Clean up 
### Delete the Secret in Secret Manager:
```
aws secretsmanager delete-secret \
--secret-id $AWSCookbook405SecretName \
--recovery-window-in-days 7
```

### Delete the Lambda function:

`aws lambda delete-function --function-name AWSCookbook405Lambda`

### Delete the Lambda CloudWatch log group:
```
aws logs delete-log-group \
--log-group-name /aws/lambda/AWSCookbook405Lambda
```

### Detach the LambdaVPCAccessExecutionPolicy from the role:
```
aws iam detach-role-policy --role-name AWSCookbook405Lambda \
--policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole
```

### Detach the SecretsManagerReadWrite policy from the role:
```
aws iam detach-role-policy --role-name AWSCookbook405Lambda \
--policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite
```

### Delete the IAM Role:

`aws iam delete-role --role-name AWSCookbook405Lambda`

### Remove the ingress rule to the RDS Instance’s Security group that allows access on port 3306/tcp from the Lambda’s Security Group:
```
aws ec2 revoke-security-group-ingress \
--protocol tcp --port 3306 \
--source-group $LAMBDA_SG_ID \
--group-id $RDS_SECURITY_GROUP
```

### Delete the security group that you created for the Lambda function:

`aws ec2 delete-security-group --group-id $LAMBDA_SG_ID`

### Go to the cdk-AWS-Cookbook-405 directory:

`cd cdk-AWS-Cookbook-405/`

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Unset the environment variable that you created manually:
```
unset RDS_ADMIN_PASSWORD
unset LAMBDA_ROTATE_ARN
unset LAMBDA_SG_ID
unset AWSCookbook405SecretName
```

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`

