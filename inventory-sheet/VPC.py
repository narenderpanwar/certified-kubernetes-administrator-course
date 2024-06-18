from paginator import PAGE

class VPC:     
    def network(vpc_tags, workbook, session, region_name):
        ec2_client = session.client('ec2', region_name=region_name)
        vpcs = PAGE.paginator('NextToken',ec2_client,'describe_vpcs','Vpcs')
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        matching_vpcs = []
        filters = []
        if (len(vpc_tags)):
            for key in vpc_tags:
                tag_object = {"Name": f"tag:{key}", "Values": vpc_tags[key]}
                filters.append(tag_object)
            vpcs = PAGE.paginator('NextToken',ec2_client,'describe_vpcs','Vpcs', Filters=filters)
            for vpc in vpcs:
                matching_vpcs.append(vpc)
        else:
            vpcs = PAGE.paginator('NextToken',ec2_client,'describe_vpcs','Vpcs')
            for vpc in vpcs:
                matching_vpcs.append(vpc)

        if matching_vpcs:
            worksheet = workbook.add_worksheet('VPC')
            headers = [
                'VpcId', 'CidrBlock', 'InstanceTenancy', 'State', 'DhcpOptionsId', 'Tags', 'IsDefault'
            ]
            worksheet.write(0, 0, "VPC",workbook_format)
            for col_num, header in enumerate(headers):
                worksheet.write(1, col_num, header,workbook_format)

            row_num = 2
            for vpc in matching_vpcs:
                for col_num, header in enumerate(headers):
                    value = vpc.get(header, '')
                    if header == 'State' and isinstance(value, dict):
                        value = value.get('Name', '')
                    worksheet.write(row_num, col_num, str(value))
                row_num += 1
            row_num += 2
            
            # SUBNETS
            list_subnets = []
            for vpc in matching_vpcs:
                subnets = PAGE.paginator('NextToken',ec2_client, 'describe_subnets', 'Subnets', Filters=[{'Name': 'vpc-id', 'Values': [vpc['VpcId']]}])
                if subnets:
                    for subnet in subnets:
                        list_subnets.append(subnet)
            if len(list_subnets):
                worksheet.write(row_num, 0, "SUBNETS",workbook_format)
                row_num += 1
                subnet_headers = ['Name'] + list(ec2_client.describe_subnets()['Subnets'][0].keys()) if ec2_client.describe_subnets()['Subnets'] else []
                for col_num, header in enumerate(subnet_headers):
                    worksheet.write(row_num, col_num, header,workbook_format)
                row_num += 1
                for subnet in list_subnets:
                    subnet_name = next((tag['Value'] for tag in subnet.get('Tags', []) if tag['Key'] == 'Name'), '')
                    subnet_values = [subnet_name] + [subnet.get(header, '') for header in subnet_headers[1:]]
                    for col_num, value in enumerate(subnet_values):
                        worksheet.write(row_num, col_num, str(value))
                    row_num += 1
            # INTERNET GATEWAY
            list_igs = []
            for vpc in matching_vpcs:
                igws = PAGE.paginator('NextToken',ec2_client,'describe_internet_gateways','InternetGateways',Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc['VpcId']]}])
                if igws:
                    for igw in igws:
                        list_igs.append(igw)
            if len(list_igs):
                row_num += 1
                worksheet.write(row_num, 0, "INTERNET GATEWAY",workbook_format)
                row_num += 1
                igw_headers = list(ec2_client.describe_internet_gateways()['InternetGateways'][0].keys()) if ec2_client.describe_internet_gateways()['InternetGateways'] else []
                igw_headers.remove('Attachments')  # Remove Attachments to avoid nested structure
                igw_headers = ['Name'] + igw_headers + ['State']
                for col_num, header in enumerate(igw_headers):
                    worksheet.write(row_num, col_num, header,workbook_format)
                row_num += 1
                for igw in list_igs:
                    igw_name = next((tag['Value'] for tag in igw.get('Tags', []) if tag['Key'] == 'Name'), '')
                    igw_state = igw['Attachments'][0]['State'] if igw.get('Attachments') else ''
                    igw_values = [igw_name] + [igw.get(header, '') for header in igw_headers[1:-1]] + [igw_state]
                    for col_num, value in enumerate(igw_values):
                        worksheet.write(row_num, col_num, str(value))
                    row_num += 1
                    
        
            # NAT GATEWAY
            list_nat = []
            for vpc in matching_vpcs:
                nat_gateways = PAGE.paginator('NextToken',ec2_client,'describe_nat_gateways','NatGateways',Filters=[{'Name': 'vpc-id', 'Values': [vpc['VpcId']]}])
                if nat_gateways:
                    for nat_gateway in nat_gateways:
                        list_nat.append(nat_gateway)
            if len(list_nat):
                row_num += 1
                worksheet.write(row_num, 0, "NAT GATEWAY",workbook_format)
                row_num += 1
                nat_headers = list(ec2_client.describe_nat_gateways()['NatGateways'][0].keys()) if ec2_client.describe_nat_gateways()['NatGateways'] else []
                nat_headers = ['Name'] + nat_headers
                other_headers = [f"{header}" for header in nat_headers if header != 'Name']
                other_headers.remove('CreateTime')
                headers = list(nat_headers)
                headers.remove('NatGatewayAddresses')
                nat_address_headers = headers + ['AllocationId','NetworkInterfaceId','PrivateIp','PublicIp','AssociationId','IsPrimary','Status']
                for col_num, header in enumerate(nat_address_headers):
                    worksheet.write(row_num, col_num, header,workbook_format)
                row_num += 1
                for nat_gateway in list_nat:
                    nat_name = next((tag['Value'] for tag in nat_gateway.get('Tags', []) if tag['Key'] == 'Name'), '')
                    NatGatewayAddresses = nat_gateway.get('NatGatewayAddresses', [])
                    nat_gateway.pop('NatGatewayAddresses')
                    nat_values = [nat_name] + [nat_gateway.get(header) for header in headers[1:]]
                    for address in NatGatewayAddresses:
                        for key, value in address.items():
                            nat_values.append(value)
                    for col_num, value in enumerate(nat_values):
                        worksheet.write(row_num, col_num, str(value))
                    row_num += 1

            # ROUTE TABLE
            list_route = []
            for vpc in matching_vpcs:
                route_tables = PAGE.paginator('NextToken',ec2_client, 'describe_route_tables', 'RouteTables', Filters=[{'Name': 'vpc-id', 'Values': [vpc['VpcId']]}])
                if route_tables:
                    for route_table in route_tables:
                        list_route.append(route_table)
                        
            if len(list_route):
                row_num += 1
                worksheet.write(row_num, 0, "ROUTE TABLES",workbook_format)
                row_num += 1
                route_table_headers = [
                    'Name', 'RouteTableId', 'Associations', 'Main', 'Routes', 'PropagatingVgws', 'RouteTableAssociationIds'
                ]
                for col_num, header in enumerate(route_table_headers):
                    worksheet.write(row_num, col_num, header,workbook_format)
                row_num += 1
                for route_table in list_route:
                    route_table_name = next((tag['Value'] for tag in route_table.get('Tags', []) if tag['Key'] == 'Name'), '')
                    route_table_id = route_table['RouteTableId']
                    main_route_table = route_table.get('Main', False)
                    associations = [assoc.get('SubnetId', '') for assoc in route_table.get('Associations', [])]
                    routes = [route.get('DestinationCidrBlock', '') for route in route_table.get('Routes', [])]
                    propagating_vgws = [propagating_vgw['GatewayId'] for propagating_vgw in route_table.get('PropagatingVgws', [])]
                    association_ids = [assoc['RouteTableAssociationId'] for assoc in route_table.get('Associations', [])]
                    route_table_values = [
                        route_table_name, route_table_id, associations, main_route_table, routes,
                        propagating_vgws, association_ids
                    ]
                    for col_num, value in enumerate(route_table_values):
                        worksheet.write(row_num, col_num, str(value))
                    row_num += 1

            # VPC ENDPOINTS
            list_vpc_endpoints = []
            for vpc in matching_vpcs:
                vpc_endpoints = PAGE.paginator('NextToken',ec2_client, 'describe_vpc_endpoints', 'VpcEndpoints', Filters=[{'Name': 'vpc-id', 'Values': [vpc['VpcId']]}])
                if vpc_endpoints:
                    for vpc_endpoint in vpc_endpoints:
                        list_vpc_endpoints.append(vpc_endpoint)
            if len(list_vpc_endpoints):
                row_num += 1
                worksheet.write(row_num, 0, "VPC ENDPOINTS",workbook_format)
                row_num += 1
                vpc_endpoint_headers = ['ServiceName', 'VpcEndpointId', 'VpcId', 'State', 'CreationTimestamp', 'RouteTableIds','DnsEntries']
                for col_num, header in enumerate(vpc_endpoint_headers):
                    worksheet.write(row_num, col_num, header,workbook_format)
                row_num += 1
                for vpc_endpoint in list_vpc_endpoints:
                    service_name = vpc_endpoint['ServiceName']
                    vpc_endpoint_id = vpc_endpoint['VpcEndpointId']
                    vpc_id = vpc_endpoint['VpcId']
                    state = vpc_endpoint['State']
                    creation_timestamp = vpc_endpoint['CreationTimestamp']
                    route_table_ids = vpc_endpoint['RouteTableIds']
                    dns_entries = vpc_endpoint['DnsEntries']
                    vpc_endpoint_values = [
                        service_name, vpc_endpoint_id, vpc_id, state, creation_timestamp, route_table_ids, dns_entries
                    ]
                    for col_num, value in enumerate(vpc_endpoint_values):
                        worksheet.write(row_num, col_num, str(value))
                    row_num += 1
            print(f"Workbook 'VPC' created successfully.")
        else:
            print(f'No VPC found for project ')