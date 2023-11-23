def query_1():
    print("______ Reddit Analyzer ______")
    print("Select all subreddits mentioned alongside subreddit X")
    x = input("Subreddit X name \n >>")
    # TODO make query
    print(f"Subreddits mentioned alongside {x}:")
    # TODO print result
    print(" _ ")


def query_2():
    print("______ Reddit Analyzer ______")
    print("Select all subreddits mentioned in negative way in subreddit X")
    x = input("Subreddit X name \n >>")
    # TODO make query
    print(f"Subreddits mentioned negatively in {x}:")
    # TODO print result
    print(" _ ")


def query_3():
    print("______ Reddit Analyzer ______")
    print("Find subreddit mentioned the most often in not negative manner:")
    # TODO make query
    # TODO print result
    print(" _ ")


def query_4():
    print("______ Reddit Analyzer ______")
    print("Return X top subreddits that where mentioned the most")
    x = int(input("Number of top subreddits \n >>"))
    # TODO make query
    print(f"{x} top subreddits that where mentioned the most:")
    # TODO print result
    print(" _ ")


def query_5():
    print("______ Reddit Analyzer ______")
    print("Find subreddit with the most posts with LIWC_X > 0")
    x = input("Which LIWC (\n1. LIWC_Swear, \n2. LIWC_Anger, \n3. LIWC_Sad, \n4. LIWC_Dissent) \n >>")
    int_to_liwc = {
        "1": "Swear",
        "2": "Anger",
        "3": "Sad",
        "4": "Dissent",
    }
    x = int_to_liwc[x]
    # TODO make query
    print(f"Subreddit with the most posts with LIWC_{x}:")
    # TODO print result
    print(" _ ")


def query_6():
    print("______ Reddit Analyzer ______")
    print("Find all subreddits mentioned in subreddits mentioned in subreddit X (neighbours of neighbours of X)")
    x = input("Subreddit X name \n >>")
    # TODO make query
    print(f"Neighbours of neighbours of {x}:")
    # TODO print result
    print(" _ ")


def query_7():
    print("______ Reddit Analyzer ______")
    print("From subreddits mentioned in subreddit X, select subreddits which mentioned subreddit X")
    x = input("Subreddit X name \n >>")
    # TODO make query
    print(f"Subreddits mentioned in {x}, that mentioned {x} back:")
    # TODO print result
    print(" _ ")


def query_8():
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
        print("0. Exit")
        print("_____________________________")

        i = input(">>")
        if i == "1":
            query_1()
        elif i == "2":
            query_2()
        elif i == "3":
            query_3()
        elif i == "4":
            query_4()
        elif i == "5":
            query_5()
        elif i == "6":
            query_6()
        elif i == "7":
            query_7()
        elif i == "8":
            query_8()
        elif i == "0":
            break
        else:
            print("Not recognized value.")
    print("Closing App")

