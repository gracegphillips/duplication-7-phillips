def filter_properties(properties, min_size=None, max_size=None, min_price=None, max_price=None, client_id=None, city=None, state=None):
    filtered = properties
    if min_size:
        filtered = [prop for prop in filtered if prop['house_size'] >= int(min_size)]
    if max_size:
        filtered = [prop for prop in filtered if prop['house_size'] <= int(max_size)]
    if min_price:
        filtered = [prop for prop in filtered if prop['price'] >= float(min_price)]
    if max_price:
        filtered = [prop for prop in filtered if prop['price'] <= float(max_price)]
    if client_id:
        filtered = [prop for prop in filtered if prop['client_id'] == int(client_id)]
    if city:
        filtered = [prop for prop in filtered if prop['city'] == city]
    if state:
        filtered = [prop for prop in filtered if prop['state'] == state]
    return filtered


def filter_by_name(data, name=None, email=None, phone=None):
    filtered_data = data
    if name:
        filtered_data = [item for item in filtered_data if name.lower() in item['name'].lower()]
    if email:
        filtered_data = [item for item in filtered_data if email.lower() in item['email'].lower()]
    if phone:
        filtered_data = [item for item in filtered_data if phone in item['phone']]
    return filtered_data



