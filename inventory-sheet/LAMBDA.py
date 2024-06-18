from paginator import PAGE
class LAMBDA:
    def functions(ld_tags, workbook, session, region_name):
        lambda_client = session.client('lambda', region_name=region_name)
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        filters = []
        matching_functions = []
        if (len(ld_tags)):
            for key in ld_tags:
                tag_object = {"Name": f"tag:{key}", "Values": ld_tags[key]}
                filters.append(tag_object)
            functions = PAGE.paginator('Marker',lambda_client,'list_functions','Functions')
            for function in functions:
                try:
                    service_tags = lambda_client.list_tags(Resource= function['FunctionArn'])['Tags']
                    if any(key == 'Project' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                        if any(key == 'Environment' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                            matching_functions.append(function)
                except lambda_client.exceptions.ResourceNotFoundException:
                    service_tags = {}
        else:
            functions = PAGE.paginator('Marker',lambda_client,'list_functions','Functions')
            for function in functions:
                matching_functions.append(function)

        if matching_functions:
            worksheet = workbook.add_worksheet('Lambda')
            headers = [
                'FunctionName', 'FunctionArn', 'Runtime', 'Role', 'Handler', 'Tags'
            ]
            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header,workbook_format)
            row_num = 1
            for function in matching_functions:
                try:
                    tags = lambda_client.list_tags(Resource=function['FunctionArn'])['Tags']
                except lambda_client.exceptions.ResourceNotFoundException:
                    tags = []
                for col_num, header in enumerate(headers):
                    value = function.get(header, '')
                    if header == 'Tags':
                        value = tags
                    worksheet.write(row_num, col_num, str(value))
                row_num += 1
            print(f"Workbook 'Lambda' created successfully.")
        else:
            print(f'No Lambda functions found for project')