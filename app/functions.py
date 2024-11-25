def filter_by_price(properties, min_price=None, max_price=None):
    """
    Filters a list of properties based on price.

    :param properties: List of properties (each property is a dictionary)
    :param min_price: Minimum price (optional)
    :param max_price: Maximum price (optional)
    :return: List of properties that match the criteria
    """
    filtered_properties = []

    for property in properties:
        if min_price is not None and property['price'] < min_price:
            continue
        if max_price is not None and property['price'] > max_price:
            continue
        filtered_properties.append(property)

    return filtered_properties
