import xlsxwriter
import yaml
import Notification
import AWSSession
from VPC import VPC
from EC2 import EC2
from RDS import RDS
from EKS import EKS
from ECS import ECS
from ELB import ELB
from ECR import ECR
from ROUTE53 import ROUTE53
from S3 import S3
from LAMBDA import LAMBDA
from CLOUDFRONT import CLOUDFRONT
from WAF import WAF
from SM import SM

        
def main():
    with open("inputs.yml", 'r') as file:
        input_data = yaml.safe_load(file)

    email_enabled = input_data["Email"]["enabled"]
    region_name = input_data["region_name"]
    profile_name = input_data["profile_name"]
    role_arn = input_data["role_arn"]
    access_key = input_data["access_key"]
    secret_key = input_data["secret_access_key"]
    session_token = input_data["session_token"]
    session = AWSSession.get_aws_session(region_name, profile_name, role_arn, access_key, secret_key, session_token)
    workbook = xlsxwriter.Workbook(f'Inventory.xlsx')
    services = [
        ('EC2', EC2.instances),
        ('EC2', EC2.volumes),
        ('EC2', EC2.snapshots),
        ('EC2', EC2.amis),
        ('EC2', EC2.asg),
        ('RDS', RDS.instances),
        ('VPC', VPC.network),
        ('EKS', EKS.clusters),
        ('ECS', ECS.clusters),
        ('ELB', ELB.data),
        ('ECR', ECR.repos),
        ('ROUTE53', ROUTE53.zones),
        ('S3', S3.buckets),
        ('LAMBDA', LAMBDA.functions),
        ('CLOUDFRONT', CLOUDFRONT.distributions),
        ('WAF', WAF.web_acls),
        ('SM', SM.secrets)
    ]

    for service, service_func in services:
        service_enable = input_data['Services'][service]['enabled']
        if service_enable:
            try:
                service_tags = input_data['Services'][service]['Tag']
            except:
                service_tags = []
            service_func(service_tags, workbook, session, region_name)
    workbook.close()
    
    if email_enabled:
        script_subject = "AWS Inventory Report"
        script_message = "Please find the generated inventory file attached"
        Notification.send_email(script_message,script_subject,script_message,'Inventory.xlsx')

main()
