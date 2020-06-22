import boto3
import uuid
import json
import time


def create_s3_bucket(bucket_name, region_name):
    
    #create bucket
    buckets = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                                'LocationConstraint': region_name})
    #wait for bucket to exist
    bucket_exists_waiter = s3.get_waiter('bucket_exists')
    bucket_exists_waiter.wait(Bucket=bucket_name)

    return buckets

def load_data(bucket_name,key,file_name):
    
    #load file into bucket
    s3_resource = session.resource('s3')
    obj = s3_resource.Object(bucket_name, key)
    put_response = obj.put(Body=open(file_name, 'rb'))

    return put_response

def create_iam_role(trust_policy,access_policy, role_name, policy_name):
    
    #create IAM role to give read & list access to the S3 bucket
    #load trust policy
    with open(trust_policy, 'r') as f:
        assume_role_trust_policy = json.dumps(json.load(f))
    
    #create role with trust policy
    role_response = iam.create_role(
                                    AssumeRolePolicyDocument = assume_role_trust_policy,
                                    RoleName = role_name
                                    )
    #wait for role to exist
    role_exists_waiter = iam.get_waiter('role_exists')
    role_exists_waiter.wait(RoleName=role_name)

    #load read and list access policy
    with open(access_policy, 'r') as f:
        access_policy = json.dumps(json.load(f))

    # create policy with read and list access
    policy_response = iam.create_policy(
                                        PolicyName=policy_name,
                                        PolicyDocument=access_policy
                                        )
                                    
    # get policy arn
    arn=policy_response['Policy']['Arn']

    #wait for policy to exist
    policy_exists_waiter = iam.get_waiter('policy_exists')
    policy_exists_waiter.wait(PolicyArn=arn)

    #attach policy to role
    attach_policy_response = iam.attach_role_policy(
                                                    RoleName=role_name,
                                                    PolicyArn= arn
                                                    )
    return attach_policy_response

def create_instance_profile(instance_profile_name,role_name):
    
    #create ec2 instance profile
    instance_profile_response = iam.create_instance_profile(
                                                               InstanceProfileName = instance_profile_name
                                                               )
    #wait for instance profile to exist
    instance_profile_waiter = iam.get_waiter('instance_profile_exists')
    instance_profile_waiter.wait(InstanceProfileName=instance_profile_name)
    
    #add role to instance profile
    add_role_response = iam.add_role_to_instance_profile(
                                                        InstanceProfileName = instance_profile_name,
                                                        RoleName            = role_name
                                                        )

def create_key_pair (key_pair_name):

    #create a key pair
    #create a file to store the key locally
    outfile = open(key_pair_name+'.pem','w')
        
    #create a key pair
    key_pair = ec2.create_key_pair(KeyName=key_pair_name)
    
    #capture the key and store it in a file
    KeyPairOut = str(key_pair['KeyMaterial'])
    
    outfile.write(KeyPairOut)


def create_security_group(security_group_name):

    #create a security group to allow ssh access from any ip address
    security= ec2.create_security_group(GroupName=security_group_name, Description=security_group_name)
    ec2.authorize_security_group_ingress(GroupId=security['GroupId'],IpProtocol="tcp",CidrIp="0.0.0.0/0",FromPort=22,ToPort=22)
    
    #get security id
    security_group_id = security['GroupId']
    return security_group_id


def create_ec2_instance(image_id,instance_type,key_pair_name,instance_profile_name,security_group_id):
    
    #create ec2 instance with required configuration
    instances = ec2_resources.create_instances(
                                             ImageId=image_id,
                                             InstanceType=instance_type,
                                             MaxCount=1,
                                             MinCount=1,
                                             SecurityGroupIds=[
                                                               security_group_id,
                                                               ],
                                            IamInstanceProfile={
                                                   'Name': instance_profile_name,
                                                   },
                                            KeyName=key_pair_name,
                                              )
    instance=instances[0]
    #wait for the instance to enter the running state
    instance.wait_until_running()

    # reload the instance attributes and get public dns name
    instance.load()
    return(instance.public_dns_name)

def create_login_script(key_pair_name,public_dns_name):

    # create bash script to set permissions on key pair file and copy scripts to local drives of ec2 instance
    with open ('ec2runscript1.sh', 'w') as rsh:
        rsh.write('''\
            #! /bin/bash
            chmod 400 ''' + key_pair_name+'''.pem
            scp -i "'''+key_pair_name+'''.pem" ec2runscript2.sh ec2-user@'''+public_dns_name+''':~/
            scp -i "'''+key_pair_name+'''.pem" parquetreader.r ec2-user@'''+public_dns_name+''':~/
            ssh -i "'''+key_pair_name+'''.pem" ec2-user@'''+public_dns_name)

def create_ec2_run_script(bucket_name):
    
    # create bash script to be configure the ec2 instance and run parquetreader script
    with open('ec2runscript2.sh', 'w') as fw, open('ec2runscripttemplate.sh', 'r') as fr:
        fw.writelines(l for l in fr)
    
    with open('ec2runscript2.sh', 'a') as fw1:
        fw1.write('''Rscript parquetreader.r ~/virtualenviron/test ''' +bucket_name+''' irisdataset.parquet''')

def main():
    
    #create an s3 bucket and load data, and then spin up an EC2 with IAM with read and list access
    
    region_name = session.region_name
    
    #Set the required parameters
    uid =str(uuid.uuid1())
    bucket_name='my-buckette'+uid
    trust_policy ='ec2-role-trust-policy.json'
    role_name = 's3AccessRole'+ uid
    access_policy = 'ec2-role-access-policy.json'
    policy_name ='s3ReadAndListAccess'+uid
    instance_profile_name=role_name
    image_id = 'ami-0ea3405d2d2522162'
    instance_type ='t2.micro'
    key_pair_name = 'EC2keypair'+uid
    security_group_name = 'SG'+uid
    file_name = 'irisdataset.parquet'
    key = file_name
    
    print('creating bucket...')

    create_s3_bucket(bucket_name, region_name)
    
    print('loading bucket...')

    load_data(bucket_name,key,file_name)
    
    print('creating iam role...')
          
    create_iam_role(trust_policy,access_policy, role_name, policy_name)
    
    create_instance_profile(instance_profile_name,role_name)
    
    create_key_pair(key_pair_name)
    
    security_group_id = create_security_group(security_group_name)
    
    #add wait time to enable ec2 instance profile set up
    time.sleep(10)
    
    print('spinning up ec2 instance...')
    
    p_d_n = create_ec2_instance(image_id,instance_type,key_pair_name,instance_profile_name,security_group_id)
          
    create_login_script(key_pair_name,p_d_n)
    
    create_ec2_run_script(bucket_name)

    print('complete...')

session = boto3.session.Session(profile_name='default')
iam = session.client('iam')
s3 = session.client('s3')
ec2_resources = session.resource('ec2')
ec2 = session.client('ec2')

main()





