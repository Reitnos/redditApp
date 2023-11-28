
import networkx as nx
import matplotlib.pyplot as plt
import time

from query2 import query2
from query3 import query3
from query4 import query4
from query5 import query5


databases = ['reddit_db_1k','reddit_db_5k','reddit_db_10k']
default_db = 'new_db'

def draw(gr, edge_labels):
    # Define layout (circular layout in this case)
    pos = nx.circular_layout(gr)

    # Draw nodes
    nx.draw_networkx_nodes(gr, pos, node_size=700, node_color='lightblue')

    # Draw edges
    nx.draw_networkx_edges(gr, pos)

    # Draw labels
    nx.draw_networkx_labels(gr, pos)

    # Draw edge labels
    if(edge_labels):

        nx.draw_networkx_edge_labels(gr, pos, edge_labels=edge_labels)


    plt.show()

def query_1(benchmark = False):
    print("______ Reddit Analyzer ______")
    print("Select all subreddits mentioned alongside subreddit X")
    x = input("Subreddit X name \n >>")
    # TODO make query

    
    print(f"Subreddits mentioned alongside {x}:")
    # TODO print result
    print(" _ ")


def query_2(benchmark = False):
    print("______ Reddit Analyzer ______")
    print("Select all subreddits mentioned in negative way in subreddit X")
    x = input("Subreddit X name \n >>")
    # TODO make query
    if(benchmark):
        for db in databases:
            query2(x,db,benchmark=True)
    else:
        gr, edge_labels = query2(x, default_db)
        draw(gr, edge_labels)

  
    print(" _ ")


def query_3(benchmark = False):
    print("______ Reddit Analyzer ______")
    print("Find subreddit mentioned the most often in not negative manner:")
    # TODO make query

    if(benchmark):
        for db in databases:
            query3(db,benchmark=True)
    else:
        gr, edge_labels, top_reddit = query3(default_db)

        draw(gr, edge_labels)
        print("Subreddit mentioned the most often in not negative manner: ", top_reddit)
    # TODO print result
   
    print(" _ ")


def query_4(benchmark = False):
    print("______ Reddit Analyzer ______")
    print("Return X top subreddits that where mentioned the most")
    x = int(input("Number of top subreddits \n >>"))
    # TODO make query

    if(benchmark):
        for db in databases:
            query4(x,db,benchmark=True)
    else:
        G, edge_labels, top_list = query4(x, default_db)
        draw(G, edge_labels)

        print(f"{x} top subreddits that where mentioned the most:")
        # TODO print result
        for i in range(x):
            print(f"{i+1}. {top_list[i]}")
    print(" _ ")


def query_5(benchmark = False):
    print("______ Reddit Analyzer ______")
    print("Find subreddit with the most posts with LIWC_X > 0")
    x = input("Which LIWC (\n1. LIWC_swear, \n2. LIWC_anger, \n3. LIWC_sad, \n4. LIWC_dissent) \n >>")
    int_to_liwc = {
        "1": "swear",
        "2": "anger",
        "3": "sad",
        "4": "dissent",
    }
    x = int_to_liwc[x]
    # TODO make query

    if(benchmark):
        for db in databases:
            query5(x,db,benchmark=True)
    else:
        gr, edge_labels, top_reddit = query5(x, default_db)
        draw(gr, edge_labels)
        print(f"Subreddit with the most posts with LIWC_{x}: ", top_reddit)
        # TODO print result
    print(" _ ")


def query_6(benchmark = False):
    print("______ Reddit Analyzer ______")
    print("Find all subreddits mentioned in subreddits mentioned in subreddit X (neighbours of neighbours of X)")
    x = input("Subreddit X name \n >>")
    # TODO make query
    print(f"Neighbours of neighbours of {x}:")
    # TODO print result
    print(" _ ")


def query_7(benchmark = False):
    print("______ Reddit Analyzer ______")
    print("From subreddits mentioned in subreddit X, select subreddits which mentioned subreddit X")
    x = input("Subreddit X name \n >>")
    # TODO make query
    print(f"Subreddits mentioned in {x}, that mentioned {x} back:")
    # TODO print result
    print(" _ ")


def query_8(benchmark = False):
    print("______ Reddit Analyzer ______")
    print("For each subreddit mentioned in subreddit X, decide if it is generally mentioned more often as negative or not-negative")
    x = input("Subreddit X name \n >>")
    # TODO make query
    print(f"Subreddits mentioned in {x} and their negativity:")
    # TODO print result
    print(" _ ")


if __name__ == '__main__':
    while True:
      
        print("______ Reddit Analyzer ______")
        print("1. Select all subreddits mentioned alongside subreddit X")
        print("2. Select all subreddits mentioned in negative way in subreddit X")
        print("3. Find subreddit mentioned the most often in not negative manner")
        print("4. Return X top subreddits that where mentioned the most")
        print("5. Find subreddit with the most posts with LIWC_X > 0")
        print("6. Find all subreddits mentioned in subreddits mentioned in subreddit X (neighbours of neighbours of X)")
        print("7. From subreddits mentioned in subreddit X, select subreddits which mentioned subreddit X")
        print("8. For each subreddit mentioned in subreddit X, decide if it is generally mentioned more often as negative or not-negative")
        print("9. Benchmark")
        print("0. Exit")
        print("_____________________________")

        i = input(">>")
        if i == "1":
            query_1()
            time.sleep(1)
        elif i == "2":
            query_2()
            time.sleep(1)
        elif i == "3":
            query_3()
            time.sleep(1)
        elif i == "4":
            query_4()
            time.sleep(1)
        elif i == "5":
            query_5()
            time.sleep(1)
        elif i == "6":
            query_6()
            time.sleep(1)
        elif i == "7":
            query_7()
            time.sleep(1)
        elif i == "8":
            query_8()
            time.sleep(1)
        elif i == "9":
            query_2(benchmark=True)
            query_3(benchmark=True)
            query_4(benchmark=True)
            query_5(benchmark=True)
            time.sleep(1)
        elif i == "0":
            break
        else:
            print("Not recognized value.")
    print("Closing App")

