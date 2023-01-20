"""
This file houses the functions to parse paradox text files.

Public function that should be called is parse_text_file()
    Args: string containing path
    Returns: nested dictionary
"""
import re
from collections import deque


def _read_file_as_string(location):
    with open(location, encoding='utf-8-sig') as file:
        data = file.read()

    return data


def _parse_pop(data_stack):
    """Pops the top of the data stack and determines what to do with it

    Returns
        popped: the popped data string paired with a keyword
        """
    popped = data_stack.popleft()

    try:
        next_pop = data_stack[0]
    except IndexError as E:
        next_pop = 'end_of_file'

    # popped is a word or (negative)number
    if re.match(r'-*\w+', popped):

        if 'end_of_file' in next_pop:
            return popped, 'value'       # the values always have the last word

        if re.match(r'=', next_pop):
            return popped, 'key'

        if re.match(r'\w+', next_pop):
            return popped, 'value'

        if re.match(r',', next_pop):
            return popped, 'value'

        if re.match(r'}', next_pop):
            return popped, 'value'

        if re.match(r'{', next_pop):
            return popped, 'key'

    if re.match(r'{', popped):
        return popped, 'up'

    if re.match(r'}', popped):
        return popped, 'down'

    if re.match('=', popped):
        return _parse_pop(data_stack)

    if re.match(',', popped):
        return _parse_pop(data_stack)

    if re.match(r'[\w/.]*', popped):      # popped is link, most likely a value
        return popped, 'value'

    raise NotImplementedError('Popped item does not match any switches')


def _parse_data(data_stack):
    """Loops through all the items on the datastack and builds a dictionary

    Create an empty dictionary and list of values
    Then start a loop through the data stack till it is empty. The top item is
    taken off and assigned an action.

    DOWN:
        Check if there are values left to add to the dictionary and return
        the current dictionary or list to the lower layer.
    VALUE:
        Add the value to the list of values.
    KEY:
        Add the last unique key value pair to the dictionary, remove the added
        value's from the list and store the new key.
    UP:
        Run this function and store the received data. Update the dictionary
        with this data. Contains a check to see if the key already exists and
        if it does it create a list for all values that belong to that key.

    """
    data_dict = {}
    list_of_values = []

    while len(data_stack) > 1:
        popped, action = _parse_pop(data_stack)

        if 'down' in action:
            if 'last_key' in locals() and len(list_of_values) == 1:
                data_dict.update({last_key: list_of_values.pop()})
            if 'last_key' in locals() and len(list_of_values) > 1:
                data_dict.update({last_key: []})
                for i in list_of_values:
                    data_dict[last_key].append(i)
                list_of_values.clear()
            if 'last_key' not in locals() and len(list_of_values) > 0:
                return list_of_values

            return data_dict

        if 'value' in action:
            list_of_values.append(popped)

        if 'key' in action:
            if 'last_key' in locals():
                if popped != last_key:
                    if len(list_of_values) == 1:
                        if last_key in data_dict.keys():
                            """This key already contains data, create list
                            with the old and new data"""
                            data_dict[last_key] = '{0}, {1}'.format(
                                data_dict[last_key], list_of_values.pop())
                        else:
                            data_dict.update({last_key: list_of_values.pop()})
                    if len(list_of_values) > 1:
                        data_dict.update({last_key: []})
                        for i in list_of_values:
                            data_dict[last_key].append(i)
                        list_of_values.clear()

            last_key = popped

        if 'up' in action:
            up_dict = _parse_data(data_stack)
            if 'last_key' in locals():
                if last_key in data_dict:
                    """Key already exists in this dictionary """
                    if isinstance(data_dict[last_key], list):
                        data_dict[last_key].append(up_dict)
                    else:
                        new_list = [data_dict[last_key], up_dict]
                        data_dict.update({last_key: new_list})
                else:
                    """Key is unique for this dictionary"""
                    data_dict.update({last_key: up_dict})
            else:
                """Dictionary does not have a key, and it might be a list 
                instead of a dictionary
                
                Data from UP is written to the dictionary.
                If there is already data in the dictionary the data is
                converted or appended to a list of UP dictionaries
                """

                if isinstance(data_dict, list):
                    data_dict.append(up_dict)

                if isinstance(data_dict, dict):
                    if len(data_dict) > 1:
                        merge_dict = [data_dict, up_dict]
                        data_dict = merge_dict
                    if len(data_dict) == 0:
                        data_dict = up_dict

    return data_dict


def parse_text_file(file_path):
    """Parses file and returns dictionary

    This function reads file in the provided path and formats it into a flat
    list that is then passed to the main data parsing function that loops
    through the list and creates a nested dictionary.

    Arg:
        file_path: string containing the path of file that has to be parsed
    Returns:
        Nested dictionary containing all information from the parsed file
    """

    ds = _read_file_as_string(file_path)

    ds = re.sub(r'(#.*)', '', ds)    # remove comment
    ds = re.sub(r'\b\s\b', ',', ds)  # newlines and whitespaces to list items
    ds = re.sub(r'\b\s(-\w)', r',\1', ds)   # whitespace before neg to list
    ds = re.sub(r'\t', '', ds)  # flatten by removing tabs
    ds = re.sub(r'(\n)*', r'\1', ds)  # remove empty lines
    ds = re.sub(r'([^}]\s+)}\s+{', r'\1,', ds)    # remove redundant dictionary
    ds = re.sub(r' ', '', ds)          # remove meaningless whitespace
    ds = re.sub(r'"', '', ds)           # remove ""
    ds = re.split(r'(\n|{|}|,|=)', ds)  # split
    ds[:] = [x for x in ds if x]         # remove whitespace
    ds[:] = [x for x in ds if x != '\n']  # remove newlines

    ds_deque = deque(ds)

    dictionary_from_file = _parse_data(data_stack=ds_deque)

    return dictionary_from_file
