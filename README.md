# bless-bootstrap
Quickly get started with Netflix's BLESS

## What's going on here
Netflix BLESS implements a SSH Certificate Authority using AWS Lambda.  What this means is that it implements a more secure way to manage access to your Linux hosts versus the default of adding a keypair.  There's a few resources online that describe what's going on behind the scenes in a much better detail.

This project is to get quickly deploy BLESS for someone who wants to evaluate how it works.  This isn't really designed for production use, but you could certainly modify it to become production ready. Environments will vary, so will your mileage.

## How-to Guide
At first I thought this would be a simple guide, but there's a lot involved in getting this to work.  Hopefully start to finish this only takes 10 minutes.

### Deploying BLESS LAmbda
- Run `venv.sh`.  This installs Ansible, Credstash, Boto3 into a virtual environment.  This is required to easily create resources required for the bless deployment and not mess with your existing system python.
- Run `source venv/bin/activate` to enter your virtualenv
- Ensure that you have active AWS credentials that allow you to create a DynamoDB table, KMS key, IAM roles, and EC2 instance.  Since you're here, I assume that you're not new to how AWS works and know how to set this up
- Update the variables located in `./variables.sh`
- Run `./credstash.sh` to install Credstash into your AWS account.  This makes a KMS key to encrypt your secrets, and a DynamoDB table to store them.
- Setup your CA key password.  Generate a high entropy password, then put it into credstash with this command: 

```
credstash \
  -r $AWS_REGION \
  -t bless-store \
  put -a bless-ca-password $YOUR_PASSWORD_HERE
```

- Update `./bless_user_data.txt` lines 4,5,6 to what makes sense to you.  AWS_REGION is what region you want to be in.  Keep in mind this must be the same as your KMS and Credstash region.  BLESS_LAMBDA_FUNCTION_NAME is the name of the lambda funtion you'll be calling to sign your public keys.  And you AWS_ACCOUNT_NUMBER is your... AWS Account Number.
- Run `./deploy.sh` to have Ansible create an EC2 instance that will compile Bless for you, then push it to Lambda.  This process should take about 2-3 minutes. 
- When it's done you can terminate the instance manually

### Configuring your Instance to trust keys signed by BLESS
- The public keys that your instances can trust should be stored in credstash.  You can get them with `credstash -r $AWS_REGION -t bless-store get ssh-ca-public-keys`
- Launch an Amazon Linux instance and ssh into it
- Create a `/etc/ssh/cas.pub` file, copy the credstash public keys into it
- chmod `/etc/ssh/cas.pub` to 0600 
- Append this line `TrustedUserCAKeys /etc/ssh/cas.pub` to `/etc/ssh/sshd_config`
- Restart the sshd daemon `service sshd restart`

### How to sign your keys

- Update variables inside `./bless.py` lines 24-31
- Run `./bless.py` 

### How to ssh into your instance

- After signing your keys you have 2 minutes to authenticate to the instance
- This does not restrict you to only 2 minutes of access to the instance.  Once you're in you can maintain your session as long as you'd like
- ssh like normal if you're signing your ~/.ssh/id_rsa.pub key `ssh ec2-user@XX.YY.ZZ.AA`

## References
- [Netflix Bless](https://github.com/Netflix/bless)
- [Credstash](https://github.com/fugue/credstash)