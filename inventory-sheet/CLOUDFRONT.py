from paginator import PAGE
class CLOUDFRONT:
    def distributions(cf_tags, workbook, session, region_name):
        cloudfront_client = session.client('cloudfront')
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        filters = []
        matching_distributions = []
        
        if (len(cf_tags)):
            for key in cf_tags:
                tag_object = {"Name": f"tag:{key}", "Values": cf_tags[key]}
                filters.append(tag_object)
            distributions = PAGE.paginator('Marker', cloudfront_client, 'list_distributions', 'DistributionList.Items')
            for distribution in distributions:
                tags = cloudfront_client.list_tags_for_resource(Resource=distribution['ARN'])['Tags']['Items']
                service_tags = {tag['Key']: tag['Value'] for tag in tags}
                if any(key == 'Project' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                    if any(key == 'Environment' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                        matching_distributions.append(distribution)
        else:
            distributions = PAGE.paginator('Marker', cloudfront_client, 'list_distributions', 'DistributionList.Items')
            for distribution in distributions:
                matching_distributions.append(distribution)
                    

        if matching_distributions:
            worksheet = workbook.add_worksheet('CloudFront')
            headers = [
                'Id', 'DomainName', 'Status', 'LastModifiedTime', 'ARN', 'Origins', 'Aliases', 'DefaultCacheBehavior'
            ]

            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header,workbook_format)

            for row_num, distribution in enumerate(matching_distributions, start=1):
                for col_num, header in enumerate(headers):
                    value = distribution.get(header, '')
                    if header == 'Origins' and isinstance(value, dict):
                        value = ', '.join([origin['Id'] for origin in value.get('Items', [])])
                    elif header == 'Aliases' and isinstance(value, dict):
                        value = ', '.join(value.get('Items', []))
                    elif header == 'DefaultCacheBehavior' and isinstance(value, dict):
                        value = value.get('Id', '')
                    worksheet.write(row_num, col_num, str(value))

            print(f"Workbook 'CloudFront' created successfully.")
        else:
            print(f'No CloudFront distributions found for project')