import os
import json

def valid_zipcode(valid_zipcodes_list, low, high, zipcode):

    if high >= low:

        mid = (high + low) // 2

        # If element is present at the middle itself
        if valid_zipcodes_list[mid] == zipcode:
            return True

        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif valid_zipcodes_list[mid] > zipcode:
            return valid_zipcode(valid_zipcodes_list, low, mid - 1, zipcode)

        # Else the element can only be present in right subarray
        else:
            return valid_zipcode(valid_zipcodes_list, mid + 1, high, zipcode)

    else:
        # Element is not present in the array
        return False

def load_valid_zipcodes():
    cur_path = os.path.dirname(os.path.abspath(__file__))
    test_data_path = os.path.join(cur_path, 'user_data/valid_zipcodes.json')

    with open(test_data_path) as zipcodes:
        valid_zipcodes = json.load(zipcodes)

    return valid_zipcodes