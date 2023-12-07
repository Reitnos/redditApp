

import requests
import base64
import json
import networkx as nx
import time


from bs4 import BeautifulSoup

def query8(X,db, benchmark = False):
    if(benchmark):
        start = time.time()

    connecturl = f'http://localhost:2480/connect/{db}'
    #Authorization HTTP header

    username = 'root'
    password = 'root'

    # Encode credentials in Base64
    credentials = f"{username}:{password}"
    credentials_encoded = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    # Create Authorization header
    headers = {'Authorization': f'Basic {credentials_encoded}'}
    response = requests.get(connecturl, headers=headers)





    table = 'title_hyperlink'
    if db == 'new_db':
        table = 'body_hyperlink'
    

    
    query8_1 = f"select DISTINCT subreddit_name from (select expand(out('title_hyperlink')) from Subreddit WHERE subreddit_name = '{X}')"
    
    
    queryurl = f'http://localhost:2480/query/{db}/sql/{query8_1}'
    response = requests.get(queryurl, headers=headers)



    response_json = json.loads(response.text)


    names = []

    # Add nodes
    for node in response_json['result']:

        out_name = node['subreddit_name']

        names.append(out_name)
    


    negativities = []
    for name in names:

        query8_2 = f"SELECT count(*) as neg_count FROM (select from title_hyperlink where out.subreddit_name = '{name}') where is_negative = true"
        query8_3 = f"SELECT count(*) as pos_count FROM (select from title_hyperlink where out.subreddit_name = '{name}') where is_negative = false"

        queryurl = f'http://localhost:2480/query/{db}/sql/{query8_2}'

        response = requests.get(queryurl, headers=headers)
        response_json = json.loads(response.text)

        neg_count = response_json['result'][0]['neg_count']

        queryurl = f'http://localhost:2480/query/{db}/sql/{query8_3}'
        response = requests.get(queryurl, headers=headers)
        response_json = json.loads(response.text)

        pos_count = response_json['result'][0]['pos_count']

    
        if(neg_count > pos_count):
            negativities.append(True)
        else:
            negativities.append(False)
        


    
    
    #disconnect
    disconnecturl= 'http://localhost:2480/disconnect'
    response = requests.get(disconnecturl, headers=headers)

    if(benchmark):
        end = time.time()
        #print(f"Query 8 - Database {db} took {end - start} seconds")
        return end - start
    return names, negativities