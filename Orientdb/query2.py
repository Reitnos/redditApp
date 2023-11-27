#create a http post to a certain text field

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

query2 = "SELECT FROM( SELECT expand(outE('body_hyperlink')) FROM subreddit WHERE subreddit_name = 'leagueoflegends') WHERE is_negative = true"
queryurl = f'http://localhost:2480/query/new_db/sql/{query2}'
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

    #get the rid of the subreddit
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
    

    #get the rid of the subreddit
    out_rid = node['out']
    #remove the # from the rid
    out_rid = out_rid[1:]
    out_name = '' 
    query_for_name_out = f"SELECT * FROM subreddit WHERE @rid = '{out_rid}'"
    queryurl = f'http://localhost:2480/query/new_db/sql/{query_for_name_out}'
    response = requests.get(queryurl, headers=headers)
    #save the response as a json
    response_json_names = json.loads(response.text)

    for name in response_json_names['result']:
        out_name = name['subreddit_name']

    G.add_node(in_name)
    G.add_node(out_name)
    G.add_edge(in_name, out_name)
    #add a label to the edge
    G.edges[in_name, out_name]['is_negative'] = node['is_negative']
    G.edges[in_name, out_name]['LIWC_anger'] = node['LIWC_anger']

    # G.edges[edge['in'], edge['out']]['is_negative'] = edge['is_negative']
    # G.edges[edge['in'], edge['out']]['LIWC_anger'] = edge['LIWC_anger']

# Define layout (circular layout in this case)
pos = nx.circular_layout(G)

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')

# Draw edges
nx.draw_networkx_edges(G, pos)

# Draw labels
nx.draw_networkx_labels(G, pos)

# Draw edge labels
# nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): G.edges[u, v]['is_negative'] for u, v in G.edges})
# nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): G.edges[u, v]['LIWC_anger'] for u, v in G.edges})

edge_labels = {(u, v): f"{G.edges[u, v]['is_negative']}, {G.edges[u, v]['LIWC_anger']}" for u, v in G.edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)


#make the background black

plt.show()

#disconnect
disconnecturl= 'http://localhost:2480/disconnect'
response = requests.get(disconnecturl, headers=headers)