#!/usr/bin/python3
"""
2-recurse
"""
import requests

def recurse(subreddit, hot_list=[], after=None):
    """
    Recursively queries the Reddit API and returns a list containing the titles
    of all hot articles for a given subreddit.
    If no results are found for the given subreddit, returns None.
    """
    if after is None:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?after={after}"
        
    headers = {'User-Agent': 'Mozilla/5.0'}  # Set a custom User-Agent to prevent errors
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        posts = data['data']['children']
        if len(posts) == 0:
            return hot_list
        else:
            for post in posts:
                hot_list.append(post['data']['title'])
            after = data['data']['after']
            return recurse(subreddit, hot_list, after)
    else:
        return None

if __name__ == "__main__":
    result = recurse("programming")
    if result is not None:
        print(len(result))
    else:
        print("None")

