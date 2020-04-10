#!/usr/bin/env python3

# initialize django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'arcticapi.settings'
import django
django.setup()

# regular imports
from api.models import Campaign, Category
import json, csv, sys
import json
import urllib
import urllib.request

# main script
def main():
    
    data =  {

        "Inputs": {

                "input1":
                {
                    "ColumnNames": ["current_amount", "goal", "donators", "days_active", "has_beneficiary", "visible_in_search", "is_charity", "num_updates"],
                    "Values": [ [ "0", "5000", "25", "9", "0", "1", "0", "0" ] ]
                },        
        },
        "GlobalParameters": {
        }
    }
    
    body = str.encode(json.dumps(data))
    
    url = 'https://ussouthcentral.services.azureml.net/workspaces/28c200bc63134d0ca21a29c5fd9024ca/services/f4496d433b9b47709873dedb98c1d0ac/execute?api-version=2.0&details=true'
    api_key = '' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers) 

    try:
        response = urllib.request.urlopen(req)

        # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
        # req = urllib.request.Request(url, body, headers) 
        # response = urllib.request.urlopen(req)

        result = response.read()
        print(result) 
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())

        print(json.loads(error.read()))  

# bootstrap
if __name__ == '__main__':
    main()
