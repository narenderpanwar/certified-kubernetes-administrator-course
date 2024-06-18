from paginator import PAGE
class RDS:
    def instances(rds_tags, workbook, session, region_name):
        rds_client = session.client('rds', region_name=region_name)
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        filters = []
        matching_instances = []
        if (len(rds_tags)):
            print('tag found')
            for key in rds_tags:
                tag_object = {"Name": f"tag:{key}", "Values": rds_tags[key]}
                filters.append(tag_object)
            db_instances = PAGE.paginator('Marker',rds_client,'describe_db_instances','DBInstances')
            for instance in db_instances:
                tags = instance.get('TagList', [])
                service_tags = {tag['Key']: tag['Value'] for tag in tags}
                if any(key == 'Project' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                    if any(key == 'Environment' and value in tag['Values'] for tag in filters for key, value in service_tags.items()):
                        matching_instances.append(instance)
        else:
            db_instances = PAGE.paginator('Marker',rds_client,'describe_db_instances','DBInstances')
            for instance in db_instances:
                matching_instances.append(instance)
        
        if matching_instances:
            worksheet = workbook.add_worksheet('RDS')
            headers = [
                'DBInstanceIdentifier', 'DBInstanceClass', 'Engine', 'DBInstanceStatus', 'MasterUsername',
                'DBName', 'Endpoint', 'AllocatedStorage', 'InstanceCreateTime', 'PreferredBackupWindow',
                'BackupRetentionPeriod', 'DBSecurityGroups', 'VpcSecurityGroups', 'DBParameterGroups',
                'AvailabilityZone', 'DBSubnetGroup', 'PreferredMaintenanceWindow', 'PendingModifiedValues',
                'MultiAZ', 'EngineVersion', 'AutoMinorVersionUpgrade', 'ReadReplicaDBInstanceIdentifiers',
                'LicenseModel', 'OptionGroupMemberships', 'PubliclyAccessible', 'StorageType',
                'DbInstancePort', 'DBClusterIdentifier', 'StorageEncrypted', 'KmsKeyId', 'DbiResourceId',
                'CACertificateIdentifier', 'DomainMemberships', 'CopyTagsToSnapshot', 'MonitoringInterval',
                'EnhancedMonitoringResourceArn', 'MonitoringRoleArn', 'PromotionTier', 'DBInstanceArn',
                'IAMDatabaseAuthenticationEnabled', 'PerformanceInsightsEnabled', 'EnabledCloudwatchLogsExports',
                'DeletionProtection', 'AssociatedRoles', 'TagList', 'CustomerOwnedIpEnabled', 'BackupTarget',
                'NetworkType', 'StorageThroughput', 'CertificateDetails', 'DedicatedLogVolume'
            ]
            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header,workbook_format)

            for row_num, instance in enumerate(matching_instances, start=1):
                for col_num, header in enumerate(headers):
                    value = instance.get(header, '')
                    if header == 'VpcSecurityGroups' and isinstance(value, list):
                        value = ', '.join([f"{entry.get('VpcSecurityGroupId', '')} ({entry.get('Status', '')})" for entry in value])
                    elif header == 'DBParameterGroups' and isinstance(value, list):
                        value = ', '.join([f"{entry.get('DBParameterGroupName', '')}" for entry in value])
                    elif header == 'DBSubnetGroup' and isinstance(value, dict):
                        subnet_group_name = value.get('DBSubnetGroupName', '')
                        value = f"{subnet_group_name}"
                    worksheet.write(row_num, col_num, str(value))
            print(f"Workbook 'RDS' created successfully.")
        else:
            print(f'No RDS instances found for project')
        
        
        
        
        
        
        
        
        
        
        
# filter_tags = [{'Name': 'tag:Project', 'Values': ['LandingPlatform', 'sws']}, {'Name': 'tag:Environment', 'Values': ['uat', 'dev', 'non-prod']}]
# service_tags = {'Project': 'LandingPlatform', 'CreatedBy': 'Terraform', 'Scope': 'RDS', 'Environment': 'non-prod', 'Module': 'RDS', 'Feature': 'shared-services', 'Name': 'non-prod-landing-mysql-bq8gpk-read-replica', 'Workspace': 'non-prod'}

# matching_instances = []

# for tag in filter_tags:
#     key = tag['Name'].split(':')[-1]
#     if key in service_tags and service_tags[key] in tag['Values']:
#         matching_instances.append(instance)

# print(matching_instances)
        