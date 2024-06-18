from paginator import PAGE
class ECS:
    def clusters(ecs_tags, workbook, session, region_name):
        ecs_client = session.client('ecs', region_name=region_name)
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        matching_clusters = []
        filters = []
        if (len(ecs_tags)):
            for key in ecs_tags:
                tag_object = {"Name": f"tag:{key}", "Values": ecs_tags[key]}
                filters.append(tag_object)
            cluster_arns = PAGE.paginator('NextToken',ecs_client,'list_clusters','clusterArns')
            for cluster_arn in cluster_arns:
                cluster_details = ecs_client.describe_clusters(clusters=[cluster_arn])
                cluster = cluster_details.get('clusters', [])[0]
                tag_list_data = ecs_client.list_tags_for_resource(resourceArn=cluster_arn)
                tags = tag_list_data["tags"]
                service_tags = {tag['key']: tag['value'] for tag in tags}
                if any(key == 'Project' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                    if any(key == 'Environment' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                        matching_clusters.append(cluster)
        else:
            cluster_arns = PAGE.paginator('NextToken',ecs_client,'list_clusters','clusterArns')
            for cluster_arn in cluster_arns:
                cluster_details = ecs_client.describe_clusters(clusters=[cluster_arn])
                cluster = cluster_details.get('clusters', [])[0]
                matching_clusters.append(cluster)
                    
        if matching_clusters:
            worksheet = workbook.add_worksheet('ECS')
            headers = [
                'clusterName', 'clusterArn', 'status', 'registeredContainerInstancesCount',
                'runningTasksCount', 'pendingTasksCount', 'activeServicesCount', 'tags', 'capacityProviders', 
                'defaultCapacityProviderStrategy', 'serviceArns'
            ]
            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header,workbook_format)

            for row_num, cluster in enumerate(matching_clusters, start=1):
                tag_list_data = ecs_client.list_tags_for_resource(resourceArn=cluster['clusterArn'])
                tags = tag_list_data["tags"]
                response = ecs_client.list_services(cluster=cluster['clusterName'])
                for col_num, header in enumerate(headers):
                    value = cluster.get(header, '')
                    if header == 'tags':
                        value = ', '.join([f"{tag['key']}: {tag['value']}" for tag in tags])
                    elif header == 'serviceArns':
                        value = response.get('serviceArns', [])
                    elif isinstance(value, (list, dict)):
                        value = ', '.join([str(val) for val in value])
                    
                    worksheet.write(row_num, col_num, str(value))
            print(f"Workbook 'ECS' created successfully.")
        else:
            print(f'No ECS clusters found for project')