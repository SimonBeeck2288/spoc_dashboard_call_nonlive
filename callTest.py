import json
import boto3
import os
#import botocore.session
from requests_html import HTMLSession
import requests 

def lambda_handler(event,context):

  session = HTMLSession()
  r = session.get('https://dashboard.nonlive.spoc.cloud.otto.de/monitoring',verify=False)
  status = r.html.search('<h1>{}</h1>')[0]
  service = r.html.search('<li>{}</li>')[0]

  errorMessage = f'This is a critical alert message! Service {service} is critical.'
  
  destPhoneNumber = os.environ['destPhoneNumber']
  contactFlowId = os.environ['contactFlowId']
  instanceId = os.environ['instanceId']
  sourcePhoneNumber = os.environ['sourcePhoneNumber']
  
  connectclient = boto3.client('connect', region_name='eu-central-1')
  snsclient = boto3.client('sns')
  
  if status != 'OK':
    OutboundResponse = connectclient.start_outbound_voice_contact(
                        DestinationPhoneNumber=destPhoneNumber,
                        ContactFlowId=contactFlowId,
                        InstanceId=instanceId,
                        SourcePhoneNumber=sourcePhoneNumber,
                        Attributes={'Message': errorMessage }
    )
    response = snsclient.publish(
      PhoneNumber= destPhoneNumber,
      Message= errorMessage,
    )