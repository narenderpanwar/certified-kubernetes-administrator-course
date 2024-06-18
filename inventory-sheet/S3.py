from paginator import PAGE
class S3:
    def buckets(s3_tags, workbook,session, region_name):
        s3_client = session.client('s3', region_name=region_name)
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        filters = []
        matching_buckets = []
        if (len(s3_tags)):
            for key in s3_tags:
                tag_object = {"Name": f"tag:{key}", "Values": s3_tags[key]}
                filters.append(tag_object)
            buckets = PAGE.paginator('NextToken', s3_client, 'list_buckets', 'Buckets')
            for bucket in buckets:
                try:
                    tags = s3_client.get_bucket_tagging(Bucket=bucket['Name'])['TagSet']
                    service_tags = {tag['Key']: tag['Value'] for tag in tags}
                    if any(key == 'Project' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                        if any(key == 'Environment' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                            matching_buckets.append(bucket)
                except s3_client.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == 'NoSuchTagSet':
                        bucket_tags = {}
                    else:
                        print(e)
                except Exception as e:
                    print(e)
        else:
            buckets = PAGE.paginator('NextToken', s3_client, 'list_buckets', 'Buckets')
            for bucket in buckets:
                matching_buckets.append(bucket)


        if matching_buckets:
            worksheet = workbook.add_worksheet('S3')
            headers = [
                'Name', 'CreationDate', 'Encryption', 'Lifecycle', 'ACL', 'Versioning', 'Logging', 'Permissions', 'Tags'
            ]

            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header,workbook_format)

            row_num = 1
            for bucket in matching_buckets:
                try:
                    tags = s3_client.get_bucket_tagging(Bucket=bucket['Name'])['TagSet']
                except s3_client.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == 'NoSuchTagSet':
                        tags = []
                    else:
                        print(e)
                except Exception as e:
                    print(e)
                
                try:
                    response = s3_client.get_bucket_encryption(Bucket=bucket['Name'])
                    rules = response['ServerSideEncryptionConfiguration']['Rules']
                    encryption = [rule['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] for rule in rules]
                except s3_client.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                        encryption = 'Not encrypted'
                    else:
                        print(e)
                except Exception as e:
                    print(e)
                    
                try:
                    response = s3_client.get_bucket_lifecycle_configuration(Bucket=bucket['Name'])
                    rules = response['Rules']
                    lifecycle = [f"ID: {rule.get('ID', '')}, Filter: {rule.get('Filter', '')},Status: {rule.get('Status', '')},NoncurrentVersionExpiration: {rule.get('NoncurrentVersionExpiration', '')}" for rule in rules]
                except s3_client.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                        lifecycle = 'No lifecycle configuration'
                    else:
                        print(e)
                except Exception as e:
                    print(e)
                    
                try:
                    response = s3_client.get_bucket_acl(Bucket=bucket['Name'])
                    acl = [grant['Permission'] + ': ' + grant['Grantee'].get('ID', grant['Grantee'].get('URI', '')) for grant in response['Grants']]
                except s3_client.exceptions.ClientError as e:
                    print(e)
                except Exception as e:
                    print(e)
                
                try:
                    response = s3_client.get_bucket_versioning(Bucket=bucket['Name'])
                    versioning = response.get('Status', 'N/A')
                except s3_client.exceptions.ClientError as e:
                    print(e)
                except Exception as e:
                    print(e)
                
                try:
                    response = s3_client.get_bucket_logging(Bucket=bucket['Name'])
                    if 'LoggingEnabled' in response:
                        logging_info = [f"Target Bucket: {response['LoggingEnabled']['TargetBucket']}, Target Prefix: {response['LoggingEnabled']['TargetPrefix']}"]
                        logging = ', '.join(logging_info)
                    else:
                        logging = 'Logging not configured'
                except s3_client.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == 'NoSuchBucketLoggingStatus':
                        logging = 'Logging not configured'
                    else:
                        print(e)
                except Exception as e:
                    print(e)

                
                try:
                    response = s3_client.get_bucket_policy(Bucket=bucket['Name'])
                    policy_info = response['Policy']
                    permissions = policy_info
                except s3_client.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                        permissions = 'No bucket policy'
                    else:
                        print(e)
                except Exception as e:
                    print(e)

                for col_num, header in enumerate(headers):
                    value = bucket.get(header, '')
                    if header == 'Tags':
                        value = tags
                    elif header == 'CreationDate':
                        creation_time = bucket.get('CreationDate', '')
                        if creation_time:
                            creation_time = creation_time.strftime("%Y-%m-%d %H:%M:%S")
                            value = str(creation_time)
                    elif header == 'Encryption':
                        value = encryption
                    elif header == 'Lifecycle':
                        value = lifecycle
                    elif header == 'ACL':
                        value = acl
                    elif header == 'Versioning':
                        value = versioning
                    elif header == 'Logging':
                        value = logging
                    elif header == 'Permissions':
                        value = permissions

                    worksheet.write(row_num, col_num, str(value))
                row_num += 1

            print(f"Workbook 'S3' created successfully.")
        else:
            print(f'No S3 buckets found for project')
