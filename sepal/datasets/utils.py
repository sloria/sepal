'''Utility methods'''

def filter_by_key(key, list_of_dicts):
    '''Filters a list of dicts into a list of values by a given key.

    Example: 
    >> dicts = [{'duration': 1, 'ss': 2}, {'duration': 3, 'ss': 4}]
    >> filter_by_key('duration', dicts)
    [1, 3]

    Arguments:
    key - The key to filter the list on 
    list_of_dicts - List of dictionaries
    '''
    return [d[key] for d in list_of_dicts for k, v in d.iteritems() if k == key]

def find_dict_by_item(item_as_tuple, list_of_dicts):
    '''Finds a dictionary in a list of dictionaries by a given key-value pair

    Arguments:
    item_as_tuple - The key-value pair to use as a search query
    list_of_dicts - List of dictionaries to search from
    '''
    return next((item for item in list_of_dicts if item[item_as_tuple[0]] == item_as_tuple[1]), None)
