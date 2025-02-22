# python/modify_data.py

import sys
import json

def modify_data(input_data):
    # Simple modification: append "modified" to the data
    return f"{input_data} modified"

if __name__ == "__main__":
    # Get the input data from command line (passed from JS)
    input_data = sys.argv[1]  # The data comes as a string
    modified_data = modify_data(input_data)
    
    # Return the modified data as JSON string
    print(json.dumps({"modified_data": modified_data}))
