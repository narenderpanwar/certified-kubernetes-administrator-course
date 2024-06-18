from paginator import PAGE

class EC2:
    def instances(ec2_tags, workbook, session, region_name):
        ec2_client = session.client('ec2', region_name=region_name)
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        filters = []
        matching_instances = []
        if (len(ec2_tags)):
            for key in ec2_tags:
                tag_object = {"Name": f"tag:{key}", "Values": ec2_tags[key]}
                filters.append(tag_object)
            reservations = PAGE.paginator('NextToken', ec2_client, 'describe_instances', 'Reservations', Filters=filters)
            for reservations_list in reservations:
                for instance in reservations_list.get('Instances', []):
                    matching_instances.append(instance)
        else:
            reservations = PAGE.paginator('NextToken', ec2_client, 'describe_instances', 'Reservations')
            for reservations_list in reservations:
                for instance in reservations_list.get('Instances', []):
                    matching_instances.append(instance)

        if matching_instances:
            worksheet = workbook.add_worksheet('EC2')
            headers = [
                'Name','InstanceId', 'InstanceType', 'OS', 'Architecture','LaunchTime', 'PrivateIpAddress', 'PublicIpAddress',
                'PrivateDnsName','State', 'SubnetId', 'VpcId', 'KeyName', 'SecurityGroups', 'VolumeID', 'VolumeType','VolumeSize', 'VolumeEncrption','Tag:Project','Tag:Environment','Tags'
            ]
            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header,workbook_format)
            for row_num, instance in enumerate(matching_instances, start=1):
                for col_num, header in enumerate(headers):
                    if header == 'Name':
                        name_tag = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'), '')
                        value = name_tag
                    elif header == 'Tag:Project':
                        name_tag = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Project'), '')
                        value = name_tag
                    elif header == 'Tag:Environment':
                        name_tag = next((tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Environment'), '')
                        value = name_tag
                    elif header == 'OS':
                        platform = instance.get('Platform', 'Linux')
                        if platform is None:
                            image_id = instance.get('ImageId')
                            image = ec2_client.describe_images(ImageIds=[image_id])['Images'][0]
                            platform_details = image.get('PlatformDetails', 'Linux/UNIX')
                            value = platform_details
                        else:
                            value = platform
                    else:
                        value = instance.get(header, '')
                        if header == 'State' and isinstance(value, dict):
                            value = value.get('Name', '')
                        elif header == 'SecurityGroups' and isinstance(value, list):
                            value = ', '.join([f"{group['GroupName']} ({group['GroupId']})" for group in value])
                        elif header == 'VolumeID':
                            volumes = instance.get('BlockDeviceMappings', '')
                            volume_list = []
                            for volume in volumes:
                                ebs = volume.get('Ebs','')
                                id = ebs.get('VolumeId','')
                                volume_list.append(id)
                            value = ', '.join(volume_list)
                        elif header == 'VolumeSize':
                            volumes = instance.get('BlockDeviceMappings', '')
                            for volume in volumes:
                                ebs = volume.get('Ebs','')
                                id = ebs.get('VolumeId','')
                                volume_info = ec2_client.describe_volumes(VolumeIds=[id])['Volumes'][0]
                                value =  volume_info.get('Size','')
                        elif header == "VolumeEncrption":
                            volumes = instance.get('BlockDeviceMappings', '')
                            for volume in volumes:
                                ebs = volume.get('Ebs','')
                                id = ebs.get('VolumeId','')
                                volume_info = ec2_client.describe_volumes(VolumeIds=[id])['Volumes'][0]
                                value =  volume_info.get('Encrypted','')
                        elif header == "VolumeType":
                            volumes = instance.get('BlockDeviceMappings', '')
                            for volume in volumes:
                                ebs = volume.get('Ebs','')
                                id = ebs.get('VolumeId','')
                                volume_info = ec2_client.describe_volumes(VolumeIds=[id])['Volumes'][0]
                                value =  volume_info.get('VolumeType','')
                        elif header == 'BlockDeviceMappings' and isinstance(value, list):
                            value = ', '.join([f"{mapping['DeviceName']}:{mapping['Ebs']['VolumeId']}" for mapping in value])
                    worksheet.write(row_num, col_num, str(value))
            print(f"Workbook 'EC2' created successfully.")
        else:
            print(f'No EC2 instances found for project')
            
    def volumes(ec2_tags, workbook, session, region_name):
        ec2_client = session.client('ec2', region_name=region_name)
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        filters = []
        matching_volumes = []

        if len(ec2_tags):
            for key in ec2_tags:
                tag_object = {"Name": f"tag:{key}", "Values": ec2_tags[key]}
                filters.append(tag_object)
            volumes = PAGE.paginator('NextToken', ec2_client, 'describe_volumes', 'Volumes', Filters=filters)
            for volume in volumes:
                matching_volumes.append(volume)
        else:
            volumes = PAGE.paginator('NextToken', ec2_client, 'describe_volumes', 'Volumes')
            for volume in volumes:
                matching_volumes.append(volume)

        if matching_volumes:
            worksheet = workbook.add_worksheet('EC2 Volumes')
            headers = ['VolumeId', 'Size', 'VolumeType', 'Encrypted', 'CreateTime', 'AvailabilityZone', 'State', 'Tags']
            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header, workbook_format)

            for row_num, volume in enumerate(matching_volumes, start=1):
                for col_num, header in enumerate(headers):
                    if header == 'Tags':
                        tags = volume.get('Tags', [])
                        tag_values = ', '.join([f"{tag['Key']}:{tag['Value']}" for tag in tags])
                        worksheet.write(row_num, col_num, tag_values)
                    else:
                        value = volume.get(header, '')
                        worksheet.write(row_num, col_num, str(value))

            print(f"Workbook 'Volumes' created successfully.")
        else:
            print('No volumes found for the specified tags.')
            
    def amis(ec2_tags, workbook, session, region_name):
        ec2_client = session.client('ec2', region_name=region_name)
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        filters = []
        matching_amis = []

        if len(ec2_tags):
            for key in ec2_tags:
                tag_object = {"Name": f"tag:{key}", "Values": ec2_tags[key]}
                filters.append(tag_object)
            amis = PAGE.paginator('NextToken', ec2_client, 'describe_images', 'Images', Filters=filters)
            for ami in amis:
                matching_amis.append(ami)
        else:
            amis = PAGE.paginator('NextToken', ec2_client, 'describe_images', 'Images', Owners=["self"])
            for ami in amis:
                matching_amis.append(ami)

        if matching_amis:
            worksheet = workbook.add_worksheet('AMIs')
            headers = ['ImageId', 'Name', 'Description', 'CreationDate', 'Architecture', 'RootDeviceType', 'State', 'Tags']
            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header, workbook_format)

            for row_num, ami in enumerate(matching_amis, start=1):
                for col_num, header in enumerate(headers):
                    if header == 'Tags':
                        tags = ami.get('Tags', [])
                        tag_values = ', '.join([f"{tag['Key']}:{tag['Value']}" for tag in tags])
                        worksheet.write(row_num, col_num, tag_values)
                    else:
                        value = ami.get(header, '')
                        worksheet.write(row_num, col_num, str(value))

            print(f"Workbook 'AMIs' created successfully.")
        else:
            print('No AMIs found for the specified tags.')

    def asg(asg_tags, workbook, session, region_name):
        asg_client = session.client('autoscaling', region_name=region_name)
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        filters = []
        matching_asgs = []

        if len(asg_tags):
            for key in asg_tags:
                tag_object = {"Name": f"tag:{key}", "Values": asg_tags[key]}
                filters.append(tag_object)
            asgs = PAGE.paginator('NextToken', asg_client, 'describe_auto_scaling_groups', 'AutoScalingGroups', Filters=filters)
            matching_asgs.extend(asgs)
        else:
            asgs = PAGE.paginator('NextToken', asg_client, 'describe_auto_scaling_groups', 'AutoScalingGroups')
            matching_asgs.extend(asgs)
        if matching_asgs:
            worksheet = workbook.add_worksheet('AutoScalingGroups')
            headers = [
                'AutoScalingGroupName', 'AutoScalingGroupARN','DesiredCapacity', 'MinSize', 'MaxSize', 'AvailabilityZones',
                'VPCZoneIdentifier', 'LaunchTemplateName','LaunchTemplateId','LaunchTemplateVersion', 'Overrides', 'InstancesDistribution','HealthCheckType','HealthCheckGracePeriod', 
                'CreatedTime', 'Tags'
            ]

            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header, workbook_format)

            for row_num, asg in enumerate(matching_asgs, start=1):
                for col_num, header in enumerate(headers):
                    value = asg.get(header, '')
                    if header == 'Instances' and isinstance(value, list):
                        instance_ids = [instance['InstanceId'] for instance in value]
                        value = ', '.join(instance_ids)
                    if 'LaunchTemplate' in asg:
                        if header == 'LaunchTemplateName':
                            lt = asg.get('LaunchTemplate', '')
                            value = lt.get('LaunchTemplateName','')
                        elif  header == 'LaunchTemplateId':
                            lt = asg.get('LaunchTemplate', '')
                            value = lt.get('LaunchTemplateId','')
                        elif  header == 'LaunchTemplateVersion':
                            lt = asg.get('LaunchTemplate', '')
                            value = lt.get('Version','')    
                    elif 'MixedInstancesPolicy' in asg:
                        if header == 'LaunchTemplateName':
                            lt = asg.get('MixedInstancesPolicy', '').get('LaunchTemplate','')
                            value = lt.get('LaunchTemplateSpecification','').get('LaunchTemplateName','')
                        elif header == 'LaunchTemplateId':
                            lt = asg.get('MixedInstancesPolicy', '').get('LaunchTemplate','')
                            value = lt.get('LaunchTemplateSpecification','').get('LaunchTemplateId','')
                        elif header == 'LaunchTemplateVersion':
                            lt = asg.get('MixedInstancesPolicy', '').get('LaunchTemplate','')
                            value = lt.get('LaunchTemplateSpecification','').get('Version','')
                        elif header == 'Overrides':
                            lt = asg.get('MixedInstancesPolicy', '').get('LaunchTemplate','')
                            value = lt.get('Overrides','')
                        elif header == 'InstancesDistribution':
                            value = asg.get('MixedInstancesPolicy','').get('InstancesDistribution','')
                        worksheet.write(row_num, col_num, str(value))

            print(f"Workbook 'AutoScalingGroups' created successfully.")
        else:
            print(f'No Auto Scaling Groups found for the specified tags')

    def snapshots(ec2_tags, workbook, session, region_name):
        ec2_client = session.client('ec2', region_name=region_name)
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        filters = []
        matching_snapshots = []
        if len(ec2_tags):
            for key in ec2_tags:
                tag_object = {"Name": f"tag:{key}", "Values": ec2_tags[key]}
                filters.append(tag_object)
            snapshots = PAGE.paginator('NextToken', ec2_client, 'describe_snapshots', 'Snapshots', Filters=filters)
            for snapshot in snapshots:
                matching_snapshots.append(snapshot)
        else:
            snapshots = PAGE.paginator('NextToken', ec2_client, 'describe_snapshots', 'Snapshots',OwnerIds=["self"])
            for snapshot in snapshots:
                matching_snapshots.append(snapshot)

        if matching_snapshots:
            worksheet = workbook.add_worksheet('Snapshots')
            headers = [
                'SnapshotId', 'VolumeId', 'StartTime', 'VolumeSize', 'Description', 'Encrypted',
                'State', 'Tags'
            ]

            for col_num, header in enumerate(headers):
                worksheet.write(0, col_num, header, workbook_format)

            for row_num, snapshot in enumerate(matching_snapshots, start=1):
                for col_num, header in enumerate(headers):
                    if header == 'Tags':
                        tags = ', '.join([f"{tag['Key']}:{tag['Value']}" for tag in snapshot.get('Tags', [])])
                        value = tags
                    else:
                        value = snapshot.get(header, '')
                        if header == 'StartTime':
                            value = str(value)
                    worksheet.write(row_num, col_num, str(value))
                    
            print(f"Workbook 'Snapshots' created successfully.")
        else:
            print(f'No snapshots found for specified tags')
