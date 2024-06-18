from paginator import PAGE 

class WAF:
    def web_acls(waf_tags, workbook, session, region_name):
        waf_client = session.client('wafv2', region_name=region_name)
        workbook_format = workbook.add_format({'bold': True, 'align': 'center'})
        matching_web_acls = []
        
        web_acls = PAGE.paginator('NextMarker', waf_client, 'list_web_acls', 'WebACLs', Scope='REGIONAL')
        for web_acl_id in web_acls:
            web_acl_details = waf_client.get_web_acl(Name=web_acl_id['Name'], Scope='REGIONAL', Id=web_acl_id['Id'])
            matching_web_acls.append(web_acl_details['WebACL'])
        waf_client = session.client('wafv2', region_name="us-east-1")
        web_acls = PAGE.paginator('NextMarker', waf_client, 'list_web_acls', 'WebACLs', Scope='CLOUDFRONT')
        for web_acl_id in web_acls:
            web_acl_details = waf_client.get_web_acl(Name=web_acl_id['Name'], Scope='CLOUDFRONT', Id=web_acl_id['Id'])
            matching_web_acls.append(web_acl_details['WebACL'])

        if matching_web_acls:
            worksheet = workbook.add_worksheet('WAF')
            headers = [
                'Id', 'Name', 'ARN', 'DefaultAction', 'Rules', 'VisibilityConfig', 'Capacity',
                'ManagedByFirewallManager'
            ]
            row_num = 0
            worksheet.write(0, 0, "WEB ACL")
            for col_num, header in enumerate(headers):
                worksheet.write(row_num, col_num, header, workbook_format)
            row_num += 1
            for web_acl in matching_web_acls:
                for col_num, header in enumerate(headers):
                    value = web_acl.get(header, '')
                    if isinstance(value, dict):
                        value = ', '.join([f"{key}: {val}" for key, val in value.items()])
                    worksheet.write(row_num, col_num, str(value))
                row_num += 1

            print(f"Workbook 'WAF' created successfully.")
        else:
            print(f'No WAF WebACLs found for the project')
