#!/usr/bin/env python

# Run the bless_client.py script

import subprocess
import boto3
import os
import botocore

# Variables you can change
SOURCE_IP = ""# Your source IP Address
SSH_USERNAME = raw_input("Enter your username: ") # Probably should be pulled from access key credentials
SSH_PUB_KEY_PATH = os.path.expanduser("~/.ssh/id_rsa.pub") # You can use your own private key for this project
SSH_CERT_PATH = os.path.expanduser("~/.ssh/id_rsa-cert.pub") # This needs to be saved in the same dir as your private key

REGION = "" # Change for your AWS Region
BLESS_LAMBDA_NAME = "" # Change for your Bless Lambda Function's Name
COMMAND = "bash"

bless_command = subprocess.Popen(['bless_client.py',
	REGION,
	BLESS_LAMBDA_NAME,
	SSH_USERNAME,
	SOURCE_IP,
	"ec2-user",
	SOURCE_IP,
	COMMAND,
	SSH_PUB_KEY_PATH,
	SSH_CERT_PATH], 
	stdout=subprocess.PIPE)
output = bless_command.communicate()[0]
print output