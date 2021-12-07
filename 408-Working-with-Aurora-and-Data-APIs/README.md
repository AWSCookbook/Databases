# Working with Aurora and Data APIs
## Preparation
This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources 

### In the root of this Chapter’s repo cd to the  “408-Working-with-Aurora-and-Data-APIs/cdk-AWS-Cookbook-408” directory and follow the subsequent steps:
```
cd 408-Working-with-Aurora-and-Data-APIs/cdk-AWS-Cookbook-408/
test -d .venv || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cdk deploy
```

### Wait for the cdk deploy command to complete. 

### We created a helper.py script to let you easily create and export environment variables to make subsequent commands easier. Run the script, and copy the output to your terminal to export variables:

`python helper.py`

### Navigate up to the main directory for this recipe (out of the “cdk-AWS-Cookbook-402” directory):

`cd ..`



## Clean up 
### Delete the SSM parameters:
```
aws ssm delete-parameter --name Cookbook408DatabaseName
aws ssm delete-parameter --name Cookbook408SecretArn
aws ssm delete-parameter --name Cookbook408ClusterArn
```

### Detach the policy from the role:
```
aws iam detach-role-policy --role-name $INSTANCE_ROLE_NAME \
--policy-arn arn:aws:iam::$AWS_ACCOUNT_ID:policy/AWSCookbook408RDSDataPolicy
```

### Delete the IAM Policy:
```
aws iam delete-policy --policy-arn \
arn:aws:iam::$AWS_ACCOUNT_ID:policy/AWSCookbook408RDSDataPolicy
```

### Go to the cdk-AWS-Cookbook-408 directory:

`cd cdk-AWS-Cookbook-408/`

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`
