from paginator import PAGE 

class SM:
    def secrets(sm_tags, workbook, session, region_name):
        secrets_manager_client = session.client('secretsmanager', region_name=region_name)
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        matching_secrets = []

        if len(sm_tags):
            secrets = PAGE.paginator('NextToken', secrets_manager_client, 'list_secrets', 'SecretList')
            for secret in secrets:
                try:
                    secret_metadata = secrets_manager_client.describe_secret(SecretId=secret['Name'])
                    secret_tags = secret_metadata.get('Tags', [])
                    if all(any(tag['Key'] == key and tag['Value'] in values for tag in secret_tags) for key, values in sm_tags.items()):
                        matching_secrets.append(secret)
                except secrets_manager_client.exceptions.ResourceNotFoundException:
                    pass

        else:
            secrets = PAGE.paginator('NextToken', secrets_manager_client, 'list_secrets', 'SecretList')
            for secret in secrets:
                matching_secrets.append(secret)

        if matching_secrets:
            worksheet = workbook.add_worksheet('SecretsManager')
            headers = [
                'Name', 'ARN','Description', 'LastChangedDate', 'LastAccessedDate', 'CreatedDate','RotationEnabled', 'RotationLambdaARN', 'NextRotationDate', 'RotationRules','LastRotated', 'Tags'
            ]

            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header, workbook_format)

            row_num = 1
            for secret in matching_secrets:
                try:
                    secret_metadata = secrets_manager_client.describe_secret(SecretId=secret['Name'])
                    last_rotated = secret_metadata.get('LastRotatedDate', 'N/A')
                    tags = secret_metadata.get('Tags', [])
                except secrets_manager_client.exceptions.ResourceNotFoundException:
                    last_rotated = 'N/A'
                    tags = []

                for col_num, header in enumerate(headers):
                    value = secret.get(header, '')
                    if header == 'Tags':
                        value = tags
                    elif header == 'LastRotated':
                        if last_rotated != 'N/A':
                            last_rotated = last_rotated.strftime("%Y-%m-%d %H:%M:%S")
                            value = str(last_rotated)

                    worksheet.write(row_num, col_num, str(value))
                row_num += 1

            print(f"Workbook 'SecretsManager' created successfully.")
        else:
            print(f'No secrets found for specified tags in Secrets Manager.')
