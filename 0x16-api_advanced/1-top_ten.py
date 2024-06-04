#!/usr/bin/python3
"""
1-top_ten
"""

import requests

def top_ten(subreddit):
    """
    Prints the titles of the first 10 hot posts for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.

    Returns:
        None
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "reddit-top-ten-fetcher"}  # Set a custom User-Agent
    params = {"limit": 10}  # Limit the number of posts to fetch
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'children' in data['data']:
            for post in data['data']['children']:
                print(post['data']['title'])
        else:
            print("No posts found for subreddit '{}'".format(subreddit))
    else:
        print("Error fetching data from Reddit API")

if __name__ == '__main__':
    top_ten(sys.argv[1])

