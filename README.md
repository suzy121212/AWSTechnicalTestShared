Testing Testing 1 2 3
# AWSTechnicalTest
AWSTechnicalTest - changing demo test 14


This project will perform the following steps as part of the AWS Technical Test:
1 - Locally creates a parquet file with some data in it
2 - Creates an S3 bucket, and uploads the parquet file to the bucket
3 - Creates an IAM Role that gives Read & List access to the S3 bucket
4 - Spins up an EC2 instance that has the above IAM Role attached 
5 - Install R on the EC2 instance
6 - Copies a “Parquet Reader” R Script to the EC2 instance 
7 - Runs the “Parquet Reader” R Script 


The following files exist in folder:
- ec2-role-access-policy.json : policy template to enable Read & List access from EC2 to resource i.e.S3 bucket, required when configuring IAM role for EC2 instance
- ec2-role-trust-policy.json : policy template to configure trust relationship required when configuring IAM role for EC2 instance
- ec2runscript0.sh : Bash script to execute parquetreader.r and test.py
- ec2runscript1.sh:  Bash script to copy 1) parquet file (irisdataset.parquet) and ec2runscript2.sh to EC2 instance and 2) connect to EC2 instance. NB: this script is only created after ec2runscript0.sh is executed
- ec2runscript2.sh: Bash script to configure EC2 instance and execute parquetreader.r  NB: this script is only created after ec2runscript0.sh is executed
- ec2runscripttemplate.sh : Bash script template
- parquetwriter.r : R file to create irisdataset.parquet file locally
- parquetreader.r : R file to read irisdataset.parquet file from S3 bucket
- test.py : Python script which will create and load S3 bucket and spin up an EC2 instance with required permissions

INSTALLATION/CONFIGURATION for MAC

1 - Install Pip (Python package manager). Execute the following command in bash terminal to install:
    
    $ sudo easy_install pip

2 - Install AWS CLI and Boto3 (AWS SDK for Python) library. Execute the following command in bash terminal to install:
    
    $ pip install awscli boto3

3 - Ensure AWS user credentials with the required access are set up. To set up a new AWS user:
    https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html

4 - Configure credentials for the new user using the AWS CLI tool. Execute the following command in the terminal, use the optional flag –-profile if configuring a user which is not the default user:

    $ aws configure  --profile profile_name

    You will be prompted to enter your Access Key ID, Secret Key, Default AWS region (recommended eu-west-1) and output format (recommended json). Once provided, the credentials are saved in a local file with path ~/.aws/credentials (key information) and ~/.aws/config (region and output)

5 - The following python packages must exist json and Uuid. Execute the following command in terminal:

    $ pip install Uuid json

6 - Installation of R must exist. The easiest way to get this is using brew, if brew does not exist
    install brew through the command line:
    
    $ bash -e "$(curl –fsSL 
    https://raw.githubusercontent.com/Homebrew/install/master/install)"

    To install R:
    $ brew install r

7 - Install R package Arrow and dataset. This command should also install required dependencies:
    $ R -e install.packages(c("arrow","datasets"),repos="http://cran.us.r-project.org")


EXECUTE:

In the bash terminal run the following three scripts in turn:

1-	ec2runscript0.sh i.e. bash ec2runscript0.sh
2-	ec2runscript1.sh i.e. bash ec2runscript1.sh

NB: When prompted by ‘Are you sure you want to continue connecting?’, type yes and press return

This will connect you to the EC2 instance created

3-	ec2runscript3.sh i.e. bash ec2runscript3.sh . 

NB: This script is running on the EC2 instance and will return the second row of the parquet file:

Sepal.Length Sepal.Width Petal.Length Petal.Width Species
2          4.9           3          1.4         0.2  setosa

