from paginator import PAGE 
class EKS:
    def clusters(eks_tags, workbook, session, region_name):
        eks_client = session.client('eks', region_name=region_name)
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        matching_clusters = []
        filters = []
        if (len(eks_tags)):
            for key in eks_tags:
                tag_object = {"Name": f"tag:{key}", "Values": eks_tags[key]}
                filters.append(tag_object)
            clusters = PAGE.paginator('NextToken',eks_client,'list_clusters','clusters')
            for cluster_name in clusters:
                cluster_details = eks_client.describe_cluster(name=cluster_name)
                service_tags = cluster_details.get('cluster', {}).get('tags', {})
                if any(key == 'Project' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                    if any(key == 'Environment' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                        matching_clusters.append(cluster_details['cluster'])
        else:
            clusters = PAGE.paginator('NextToken',eks_client,'list_clusters','clusters')
            for cluster_name in clusters:
                cluster_details = eks_client.describe_cluster(name=cluster_name)
                matching_clusters.append(cluster_details['cluster'])

        if matching_clusters:
            worksheet = workbook.add_worksheet('EKS')
            headers = [
                'name', 'arn', 'createdAt', 'version', 'endpoint','status', 'roleArn',
                'resourcesVpcConfig', 'logging', 'identity', 'certificateAuthority', 'platformVersion','tags'
            ]
            node_group_headers = ['nodegroupName', 'nodegroupArn', 'status','capacityType', 
                'scalingConfig', 'instanceTypes','subnets','amiType','nodeRole','labels','taints','diskSize','tags']
            row_num = 0
            worksheet.write(0, 0, "CLUSTER",workbook_format)
            row_num += 1
            for col_num, header in enumerate(headers):
                worksheet.write(row_num, col_num, header,workbook_format)
            row_num += 1
            for cluster in matching_clusters:
                for col_num, header in enumerate(headers):
                    value = cluster.get(header, '')
                    if isinstance(value, dict):
                        value = ', '.join([f"{key}: {val}" for key, val in value.items()])
                    worksheet.write(row_num, col_num, str(value))
                row_num += 1
                
            row_num += 1
            worksheet.write(row_num, 0, "NODE_GROUPS",workbook_format)
            row_num += 1
            for col_num, header in enumerate(node_group_headers):
                worksheet.write(row_num, col_num, header,workbook_format)
            row_num += 1
            for cluster in matching_clusters:
                node_groups = eks_client.list_nodegroups(clusterName=cluster['name']).get('nodegroups', [])
                if node_groups:
                    for node_group in node_groups:
                        try:
                            response = eks_client.describe_nodegroup(clusterName=cluster_name, nodegroupName=node_group)
                            for col_num, node_header in enumerate(node_group_headers):
                                value = response['nodegroup'].get(node_header, '')
                                if isinstance(value, dict):
                                    value = ', '.join([f"{key}: {val}" for key, val in value.items()])
                                worksheet.write(row_num, col_num, str(value))
                            row_num += 1
                        except eks_client.exceptions.ResourceNotFoundException as e:
                            print(f"Node group '{node_group}' not found. Ignoring...")
                        except Exception as e:
                            print(f"An error occurred: {e}")

            print(f"Workbook 'EKS' created successfully.")
        else:
            print(f'No EKS clusters found for project')