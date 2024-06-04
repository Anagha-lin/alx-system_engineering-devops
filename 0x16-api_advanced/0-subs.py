#!/usr/bin/python3
"""
Returns the number of subscribers for a given subreddit
"""

import requests

def number_of_subscribers(subreddit):
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {'User-Agent': 'MyAPI/0.0.1'}
    
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 200:
        data = response.json()
        return data['data']['subscribers']
    else:
        return 0

if __name__ == "__main__":
    subreddit = input("Enter the subreddit: ")
    print(number_of_subscribers(subreddit))

