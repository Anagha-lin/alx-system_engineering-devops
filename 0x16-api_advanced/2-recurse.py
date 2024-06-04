#!/usr/bin/python3
"""
2-recurse
"""

import requests

def recurse(subreddit, hot_list=[], after=None):
    """
    Recursively queries the Reddit API and returns a list containing the titles
    of all hot articles for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.
        hot_list (list): List to accumulate the titles of hot articles (default []).
        after (str): Parameter for pagination to get the next set of results (default None).

    Returns:
        list: List containing the titles of all hot articles for the subreddit,
              or None if no results are found.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "reddit-recursion-fetcher"}  # Set a custom User-Agent
    params = {"limit": 100, "after": after}  # Limit the number of posts to fetch and set pagination parameter
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'children' in data['data']:
            children = data['data']['children']
            for post in children:
                hot_list.append(post['data']['title'])
            after = data['data']['after']  # Get the 'after' parameter for pagination
            if after is not None:
                return recurse(subreddit, hot_list, after)  # Recursively call the function with the 'after' parameter
            else:
                return hot_list
        else:
            return None
    else:
        return None

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        result = recurse(sys.argv[1])
        if result is not None:
            print(len(result))
        else:
            print("None")

