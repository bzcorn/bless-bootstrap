#!/bin/bash

source ./variables.sh

# Create a KMS key and save the KEY ID to a variable
KEYID=$(aws --region $AWS_REGION kms create-key --query 'KeyMetadata.KeyId')

# Create an easy to use Alias for the KMS key created in the previous command
aws --region $AWS_REGION --alias-name bless --target-key-id $KEYID

# Setup Credstash
credstash setup -r $AWS_REGION -t bless-store