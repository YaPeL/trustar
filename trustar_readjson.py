#!/usr/bin/env python3.8
import json
import re


class TrustarReadJson():
    """ 
    Trustar Read Json, is a class for a challenge from the company Trustar, 
    to extract valuable information from a string representing a json object
    """

    def __init__(self):
        super(TrustarReadJson, self)

    def read_json(self, file):
        """Input Json File & return json to python dict"""

        with open(file) as json_file:
            return json.load(json_file)

    def extract_valuable_information(self, json_data, properties_list):
        """
        Extract valuable information from a array of properties
        and subproperties using dot notation.
        """

        # check if param properties list is correct (list or string)
        if not isinstance(properties_list, list):
            if isinstance(properties_list, str):
                properties_list = [properties_list]
            else:
                raise TypeError(
                    "The function expects to receive a list property or dot string property")

        result = {}
        # walk through the properties
        for prop in properties_list:
            prop_list = prop.split('.')
            # get the information of the property
            data = self.get_recursive_dot_property(
                json_data, prop_list)
            if data != "Property DoesNotExists":
                result[prop] = data

        print(result)
        return result

    def get_recursive_dot_property(self, dict_data, dot_property_list):
        """
        Recursive function, ends when it finds the last dot property or detects that it does not exist.
        Transform the dot property into a list and remove the elements from the first to the last
        """

        # last recursive function control
        if not dot_property_list:
            return dict_data

        dot_property = dot_property_list.pop(0)  # remove the first element

        if isinstance(dict_data, dict):
            array_access = self.check_array_access(
                dot_property)  # Check if porperty has array access
            if array_access:
                dot_property_with_index = dot_property
                dot_property = re.compile(r"(\[\d*])").split(dot_property)[0]

            if dot_property in dict_data:  # Check if property exists in data
                if array_access:
                    # if it is an access array, the property is executed dynamically using eval
                    exec_string = f"dict_data[dot_property]{dot_property_with_index.replace(dot_property,'')}"
                    try:
                        dict_data = eval(exec_string)
                    except IndexError:
                        return "Property DoesNotExists"
                else:
                    dict_data = dict_data[dot_property]
                return self.get_recursive_dot_property(dict_data, dot_property_list)

        return "Property DoesNotExists"

    def check_array_access(self, dot_property):
        """
        Check function if property has access to any array index
        Return True or False
        """
        if re.compile(r"(\[\d*])").search(dot_property):
            return True
        return False


if __name__ == '__main__':
    obj_trustar = TrustarReadJson()
    data = obj_trustar.read_json('test_data.json')
    properties_to_extract = [
        "guid", "content.entities", "score", "score.sign"]

    obj_trustar.extract_valuable_information(
        data, properties_to_extract)
