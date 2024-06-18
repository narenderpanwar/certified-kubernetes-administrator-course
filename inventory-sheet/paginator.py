class PAGE:
    def paginator(pagination_type, client, api_method, result_key, *args, **kwargs):
        items = []
        pagination_value = None
        while True:
            if pagination_value:
                kwargs[pagination_type] = pagination_value
            response = getattr(client, api_method)(*args, **kwargs)
            current_items = response
            if result_key != '':
                for key in result_key.split('.'):
                    current_items = current_items.get(key, {})
            items.extend(current_items)
            pagination_value = response.get(pagination_type, '')
            if not pagination_value:
                break
        return items