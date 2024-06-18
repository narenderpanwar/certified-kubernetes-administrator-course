from paginator import PAGE
class ROUTE53:
    def zones(rt_tags, workbook, session, region_name):
        route53_client = session.client('route53', region_name=region_name)
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        filters = []
        matching_zones = []
        if (len(rt_tags)):
            for key in rt_tags:
                tag_object = {"Name": f"tag:{key}", "Values": rt_tags[key]}
                filters.append(tag_object)
            hosted_zones = PAGE.paginator('NextToken',route53_client,'list_hosted_zones','HostedZones')
            for zone in hosted_zones:
                try:
                    tags = route53_client.list_tags_for_resource(ResourceType='hostedzone', ResourceId=zone['Id'].split('/')[-1])['ResourceTagSet']['Tags']
                    service_tags = {tag['Key']: tag['Value'] for tag in tags}
                    if any(key == 'Project' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                        if any(key == 'Environment' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                            matching_zones.append(zone)
                except route53_client.exceptions.NoSuchHostedZone:
                    service_tags = {}
        else:
            hosted_zones = PAGE.paginator('NextToken',route53_client,'list_hosted_zones','HostedZones')
            for zone in hosted_zones:
                matching_zones.append(zone)

        if matching_zones:
            worksheet = workbook.add_worksheet('Route53')
            headers = [
                'Id', 'Name', 'CallerReference', 'PrivateZone', 'Tags'
            ]
            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header,workbook_format)
            row_num = 1
            for zone in matching_zones:
                try:
                    tags = route53_client.list_tags_for_resource(ResourceType='hostedzone', ResourceId=zone['Id'].split('/')[-1])['ResourceTagSet']['Tags']
                except route53_client.exceptions.NoSuchHostedZone:
                    tags = []
                for col_num, header in enumerate(headers):
                    value = zone.get(header, '')
                    if header == 'Tags':
                        value = tags
                    elif header == 'Id':
                        value = value.split('/')[2]
                    elif header == 'PrivateZone':
                        value = str(zone.get('Config', '').get('PrivateZone', ''))
                    worksheet.write(row_num, col_num, str(value))
                row_num += 1
            row_num += 1
            for zone in matching_zones:
                Records_headers = [
                    'Zone','Name', 'Type', 'TTL', 'Value'
                ]
                for col_num, header in enumerate(Records_headers):
                    worksheet.write(row_num, col_num, header,workbook_format)
                row_num += 1
                record_sets = route53_client.list_resource_record_sets(HostedZoneId=zone['Id'])['ResourceRecordSets']
                for record in record_sets:
                    for col_num, header in enumerate(Records_headers):
                        value = record.get(header, '')
                        if header == 'Zone':
                            value = zone['Id'].split('/')[2]
                        elif header in ['Value']:
                            type = str(record.get('Type', ''))
                            if type == 'A' and 'AliasTarget' in record and record['AliasTarget'] is not None:
                                value = str(record.get('AliasTarget').get('DNSName'))
                            else:
                                value = ', '.join([f"{r['Value']}" for r in record.get('ResourceRecords')])
                        worksheet.write(row_num, col_num, str(value))
                    row_num += 1
                row_num += 1
            print(f"Workbook 'Route53' created successfully.")
        else:
            print(f'No Route53 hosted zones found for project')
