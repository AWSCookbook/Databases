# Auto Scaling DynamoDB Table Provisioned Capacity
## Preparation

### Create a DynamoDB table with fixed capacity of 1 Read Capacity Units and 1 Write Capacity Units:
```
aws dynamodb create-table \
--table-name 'AWSCookbook406' \
--attribute-definitions 'AttributeName=UserID,AttributeType=S' \
--key-schema 'AttributeName=UserID,KeyType=HASH' \
--sse-specification 'Enabled=true,SSEType=KMS' \
--provisioned-throughput \
'ReadCapacityUnits=1,WriteCapacityUnits=1'
```

### Put a few records in the table:

`aws ddb put AWSCookbook406 '[{UserID: value1}, {UserID: value2}]'`


## Clean up 
### Delete the DynamoDB table:
```
aws dynamodb delete-table \
--table-name 'AWSCookbook406'
```
