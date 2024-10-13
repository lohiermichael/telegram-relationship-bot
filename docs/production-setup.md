# Production Setup

This guide will help you set up the **Telegram Relationship Bot** for
production. The deployment is made on an [AWS EC2
instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html).

## Create an EC2 instance

Choose an Elastic IP

## Set Up the EC2 server

Follow the steps described in [the ec2_setup.sh file](../aws/ec2_setup.sh)

## Set Up GitHub Actions

To make the GitHub Action for the deployment script work, you need to set up a
few essential GitHub Secrets (variables). These secrets will be used during the
deployment process to securely connect to your EC2 instance.

1. Navigate to your GitHub repository

1. Go to Settings:

    On the top-right corner of the repository page, click on the Settings tab.

1. Access Secrets:

    - In the left sidebar, scroll down and click on Secrets and variables.
    - Select Actions.

1. Add New Repository Secrets:

    - Click on the New repository secret button.

    - You will need to add the following secrets:

        - EC2_USER: This is the SSH user for your EC2 instance (it should be
        `ec2_user`).
        - EC2_KEY: This is your EC2 encrypted private key generated in
        [the ec2_setup.sh file](../aws/ec2_setup.sh) as `key.64`.
        - EC2_IP: This is the Elastic IP (EIP) of your EC2 instance.


From now, every time you push it should update the running production instance.
