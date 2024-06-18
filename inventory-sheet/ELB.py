from paginator import PAGE
class ELB:
    def data(elb_tags, workbook, session, region_name):
        elbv2_client = session.client('elbv2', region_name=region_name)
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        filters = []
        matching_load_balancers = []
        if (len(elb_tags)):
            for key in elb_tags:
                tag_object = {"Name": f"tag:{key}", "Values": elb_tags[key]}
                filters.append(tag_object)
            load_balancers = PAGE.paginator('NextToken',elbv2_client,'describe_load_balancers','LoadBalancers')
            for lb in load_balancers:
                try:
                    tags = elbv2_client.describe_tags(ResourceArns=[lb['LoadBalancerArn']])['TagDescriptions'][0]['Tags']
                    service_tags = {tag['Key']: tag['Value'] for tag in tags}
                    if any(key == 'Project' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                        if any(key == 'Environment' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                            matching_load_balancers.append(lb)
                except IndexError:
                    service_tags = {}
        else:
            load_balancers = PAGE.paginator('NextToken',elbv2_client,'describe_load_balancers','LoadBalancers')
            for lb in load_balancers:
                matching_load_balancers.append(lb)
        if matching_load_balancers:
            worksheet = workbook.add_worksheet('ELB')
            headers = [
                'LoadBalancerName', 'LoadBalancerArn', 'DNSName', 'Scheme', 'VpcId', 'Type',
                'State', 'CreatedTime', 'SecurityGroups', 'Subnets', 'Tags'
            ]

            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header,workbook_format)

            row_num = 1
            for lb in matching_load_balancers:
                tags = elbv2_client.describe_tags(ResourceArns=[lb['LoadBalancerArn']])['TagDescriptions'][0]['Tags']
                for col_num, header in enumerate(headers):
                    value = lb.get(header, '')
                    if header == 'State' and isinstance(value, dict):
                        value = value.get('Code', '')
                    elif header == 'Tags':
                        value = tags
                    elif header == 'Subnets':
                        list = []
                        for az in lb.get('AvailabilityZones',''):
                            list.append(az.get('SubnetId'))
                        value = list
                    worksheet.write(row_num, col_num, str(value))
                row_num += 1

            print(f"Workbook 'ELB' created successfully.")
        else:
            print(f'No ELBs found for project')