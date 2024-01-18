__author__ = 'Bruce.Lu'
__mail__ = 'lzbgt@icloud.com'
__create_time__ = '2023/11/07'
__version__ = '0.0.1'


def dict_schema_diff(dict1, dict2):
    diff = {}

    # Check keys in dict1 that are not in dict2
    for key in dict1.keys() - dict2.keys():
        diff[key] = (get_value_type(dict1[key]), None)

    # Check keys in dict2 that are not in dict1
    for key in dict2.keys() - dict1.keys():
        diff[key] = (None, get_value_type(dict2[key]))

    # Check keys present in both dictionaries
    for key in dict1.keys() & dict2.keys():
        if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            nested_diff = dict_schema_diff(dict1[key], dict2[key])
            if nested_diff:
                diff[key] = nested_diff
        elif isinstance(dict1[key], list) and isinstance(dict2[key], list):
            print("list: ", key, type(dict1[key]), type(dict2[key]))
            if len(dict1[key]) != len(dict2[key]):
                diff[key] = (get_value_type(dict1[key]),
                             get_value_type(dict2[key]))
            else:
                for i in range(len(dict1[key])):
                    if isinstance(dict1[key][i], dict) and isinstance(dict2[key][i], dict):
                        nested_diff = dict_schema_diff(
                            dict1[key][i], dict2[key][i])
                        if nested_diff:
                            if key not in diff:
                                diff[key] = {}
                            diff[key][i] = nested_diff
                    elif isinstance(dict1[key][i], list) and isinstance(dict2[key][i], list):
                        if len(dict1[key][i]) != len(dict2[key][i]):
                            if key not in diff:
                                diff[key] = {}
                            diff[key][i] = (get_value_type(
                                dict1[key][i]), get_value_type(dict2[key][i]))
                        else:
                            types1 = [get_value_type(x) for x in dict1[key][i]]
                            types2 = [get_value_type(x) for x in dict2[key][i]]
                            for x in range(len(types1)):
                                if types1[x] != types2[x]:
                                    diff[key][i][x] = (get_value_type(
                                        dict1[key][i][x]), get_value_type(dict2[key][i][x]))
                                elif types1[x] == dict or types1[x] == list:
                                    nested_diff = dict_schema_diff(
                                        dict1[key][i][x], dict2[key][i][x])
                                    if nested_diff:
                                        diff[key][i][x] = nested_diff
                    elif type(dict1[key][i]) != type(dict2[key][i]):
                        types = {type(dict1[key][i]), type(dict2[key][i])}
                        if types != {int, float}:
                            if key not in diff:
                                diff[key] = {}
                            diff[key][i] = (get_value_type(
                                dict1[key][i]), get_value_type(dict2[key][i]))
        elif type(dict1[key]) != type(dict2[key]):
            types = {type(dict1[key]), type(dict2[key])}
            if types != {int, float}:
                diff[key] = (get_value_type(dict1[key]),
                             get_value_type(dict2[key]))

    return diff


def get_value_type(value):
    if isinstance(value, dict):
        return 'dict'
    elif isinstance(value, list):
        return f'list[{len(value)}]'
    elif isinstance(value, int) or isinstance(value, float):
        return 'number'
    else:
        return type(value).__name__


def dict_value_diff(dict1, dict2):
    diff = {}

    # Iterate over keys in dict1
    for key in dict1:
        if key not in dict2:
            diff[key] = (dict1[key], None)
        elif isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            nested_diff = dict_value_diff(dict1[key], dict2[key])
            if nested_diff:
                diff[key] = nested_diff
        elif isinstance(dict1[key], list) and isinstance(dict2[key], list):
            if len(dict1[key]) != len(dict2[key]):
                diff[key] = (dict1[key], dict2[key])
            else:
                for i in range(len(dict1[key])):
                    if isinstance(dict1[key][i], dict) and isinstance(dict2[key][i], dict):
                        nested_diff = dict_value_diff(
                            dict1[key][i], dict2[key][i])
                        if nested_diff:
                            if key not in diff:
                                diff[key] = {}
                            diff[key][i] = nested_diff
                    elif dict1[key][i] != dict2[key][i]:
                        if key not in diff:
                            diff[key] = {}
                        diff[key][i] = (dict1[key][i], dict2[key][i])
        elif dict1[key] != dict2[key]:
            diff[key] = (dict1[key], dict2[key])

    # Iterate over keys in dict2
    for key in dict2:
        if key not in dict1:
            diff[key] = (None, dict2[key])

    return diff
