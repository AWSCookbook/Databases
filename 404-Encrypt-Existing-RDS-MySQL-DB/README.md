# Encrypting the Storage of an Existing Amazon RDS for MySQL Database 
## Preparation
This recipe requires some “prep work” which deploys resources that you’ll build the solution on. You will use the AWS CDK to deploy these resources.

### In the root of this Chapter’s repo cd to the “404-Encrypt-Existing-RDS-MySQL-DB/cdk-AWS-Cookbook-404” directory and follow the subsequent steps: 
```
cd 404-Encrypt-Existing-RDS-MySQL-DB/cdk-AWS-Cookbook-404/
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
### Delete the read replica:
```
aws rds delete-db-instance --skip-final-snapshot \
--delete-automated-backups \
--db-instance-identifier awscookbook404db-rep
```

### Delete the encrypted RDS database you created:
```
aws rds delete-db-instance --skip-final-snapshot \
--delete-automated-backups \
--db-instance-identifier awscookbook404db-enc
```

### Delete the two snapshots:
```
aws rds delete-db-snapshot \
--db-snapshot-identifier awscookbook404-snapshot
```

```
aws rds delete-db-snapshot \
--db-snapshot-identifier awscookbook404-snapshot-enc
```

### Disable the KMS Key: 

`aws kms disable-key --key-id $KEY_ID`

### Scheduled the KMS Key for deletion:
```
aws kms schedule-key-deletion \
--key-id $KEY_ID \
--pending-window-in-days 7
```

### Delete the Key Alias: 

`aws kms delete-alias --alias-name alias/awscookbook404`


### To clean up the environment variables, run the helper.py script in this recipe’s cdk- directory with the --unset flag, and copy the output to your terminal to export variables:

`python helper.py --unset`

### Unset the environment variable that you created manually 

`unset KEY_ID`

### Use the AWS CDK to destroy the resources, deactivate your Python virtual environment, and go to the root of the chapter:

`cdk destroy && deactivate && rm -r .venv/ && cd ../..`
