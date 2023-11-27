import requests
import base64

from bs4 import BeautifulSoup

connecturl = 'http://localhost:2480/connect/new_db'
#Authorization HTTP header

username = 'root'
password = 'root'

# Encode credentials in Base64
credentials = f"{username}:{password}"
credentials_encoded = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

# Create Authorization header
headers = {'Authorization': f'Basic {credentials_encoded}'}
response = requests.get(connecturl, headers=headers)

print(f"Connection: {response.status_code}")



#in fact query 3
query4 = 'SELECT in, count(*) as amount FROM body_hyperlink GROUP BY in ORDER BY amount desc LIMIT 10'

queryurl = f'http://localhost:2480/query/new_db/sql/{query4}'
response = requests.get(queryurl, headers=headers)





# Parse HTML content
soup = BeautifulSoup(response.content, 'html.parser')

#print(soup.prettify())

#create a graph visualization of the json response
import json
import networkx as nx
import matplotlib.pyplot as plt

# Parse JSON response
response_json = json.loads(response.text)

# Create a directed graph
G = nx.DiGraph()

# Add nodes
for node in response_json['result']:

    in_rid = node['in']
    #remove the # from the rid
    in_rid = in_rid[1:]
    in_name = ''
    query_for_name_in = f"SELECT * FROM subreddit WHERE @rid = '{in_rid}'"
    queryurl = f'http://localhost:2480/query/new_db/sql/{query_for_name_in}'
    response = requests.get(queryurl, headers=headers)
    #save the response as a json
    response_json_names = json.loads(response.text)

    for name in response_json_names['result']:
        in_name = name['subreddit_name']

    G.add_node(in_name)
   
    

# Define layout (circular layout in this case)
pos = nx.circular_layout(G)

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')



# Draw labels
nx.draw_networkx_labels(G, pos)

nx.draw_networkx_edge_labels(G, pos)


#make the background black

plt.show()

#disconnect
disconnecturl= 'http://localhost:2480/disconnect'
response = requests.get(disconnecturl, headers=headers)