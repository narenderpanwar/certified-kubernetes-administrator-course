from paginator import PAGE
class ECR:
    def repos(ecr_tags, workbook, session, region_name):
        ecr_client = session.client('ecr', region_name=region_name)
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        filters = []
        matching_repositories = []
        if (len(ecr_tags)):
            for key in ecr_tags:
                tag_object = {"Name": f"tag:{key}", "Values": ecr_tags[key]}
                filters.append(tag_object)
            repositories = PAGE.paginator('NextToken', ecr_client,'describe_repositories','repositories')
            for repo in repositories:
                try:
                    tags = ecr_client.list_tags_for_resource(resourceArn=repo['repositoryArn'])['tags']
                    service_tags = {tag['Key']: tag['Value'] for tag in tags}
                    if any(key == 'Project' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                        if any(key == 'Environment' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                            matching_repositories.append(repo)
                except ecr_client.exceptions.RepositoryNotFoundException:
                    service_tags = {}
        else:
            repositories = PAGE.paginator('NextToken', ecr_client,'describe_repositories','repositories')
            for repo in repositories:
                matching_repositories.append(repo)
        

        if matching_repositories:
            worksheet = workbook.add_worksheet('ECR')
            headers = [
                'repositoryName', 'repositoryArn', 'registryId', 'CreatedAt', 'imageScanningConfiguration',
                'imageTagMutability', 'encryptionConfiguration', 'Tags'
            ]

            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header,workbook_format)

            row_num = 1
            for repo in matching_repositories:
                tags = ecr_client.list_tags_for_resource(resourceArn=repo['repositoryArn'])['tags']
                for col_num, header in enumerate(headers):
                    value = repo.get(header, '')
                    if header == 'Tags':
                        value = tags
                    elif header == 'CreatedAt':
                        value = str(repo.get('createdAt', ''))
                    elif header == "imageScanningConfiguration":
                        value = str(repo.get('imageScanningConfiguration', {}).get('scanOnPush', '')) 
                    elif header == "encryptionConfiguration":
                        value = str(repo.get('encryptionConfiguration', {}).get('encryptionType', ''))
                    worksheet.write(row_num, col_num, str(value))
                row_num += 1

            print(f"Workbook 'ECR' created successfully.")
        else:
            print(f'No ECR repositories found for project')