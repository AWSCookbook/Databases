# Using IAM Authentication with a RDS Database
## Preparation
This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources

### In the root of this Chapter’s repo cd to the “402-Using-IAM-Authentication-with-RDS/cdk-AWS-Cookbook-402” directory and follow the subsequent steps: 
```
cd 402-Using-IAM-Authentication-with-RDS/cdk-AWS-Cookbook-402/
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

### Navigate up to the main directory for this recipe (out of the “cdk-AWS-Cookbook-402” directory)

`cd ..`


## Clean up 
### Detach the policy from the role:
```
aws iam detach-role-policy --role-name $INSTANCE_ROLE_NAME \
--policy-arn arn:aws:iam::$AWS_ACCOUNT_ID:policy/AWSCookbook402EC2RDSPolicy
```

### Delete the IAM Policy:
```
aws iam delete-policy --policy-arn \
arn:aws:iam::$AWS_ACCOUNT_ID:policy/AWSCookbook402EC2RDSPolicy
```

### Go to the cdk-AWS-Cookbook-402 directory:

`cd cdk-AWS-Cookbook-402/`

### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Unset the environment variable that you created manually:
```
unset DB_RESOURCE_ID
unset RDS_ADMIN_PASSWORD
unset ISOLATED_SUBNETS
```

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`
