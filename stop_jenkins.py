import boto3
import logging

#region = 'us-east-1'
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    logger.info('got event{}'.format(event))
    logger.info('TAG={}'.format(event['tag']))
    logger.info('Value={}'.format(event['value']))
    logger.info('Region={}'.format(event['region']))
    
    ec2client = boto3.client('ec2')
    region = event['region']

    response = ec2client.describe_instances(
        Filters=[
            {
                'Name': 'tag:'+ event['tag'],
                'Values': [event['value']]
            }
        ]
    )
    instancelist = []
    for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            instancelist.append(instance["InstanceId"])
    ec2 = boto3.client('ec2', region_name=region)
    ec2.stop_instances(InstanceIds=instancelist)
    print 'stopped your instances: ' + str(instancelist)
