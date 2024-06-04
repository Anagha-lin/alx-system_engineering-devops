#!/usr/bin/python3
"""
100-count
"""

import requests

def count_words(subreddit, word_list, hot_list=None, after=None, counts=None):
    """
    Recursively queries the Reddit API and counts occurrences of keywords in hot articles.

    Args:
        subreddit (str): The name of the subreddit.
        word_list (list): List of keywords to count occurrences of.
        hot_list (list): List to accumulate the titles of hot articles (default None).
        after (str): Parameter for pagination to get the next set of results (default None).
        counts (dict): Dictionary to store the counts of keywords (default None).

    Returns:
        None
    """
    if hot_list is None:
        hot_list = []
    if counts is None:
        counts = {}

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "reddit-count-words-fetcher"}  # Set a custom User-Agent
    params = {"limit": 100, "after": after}  # Limit the number of posts to fetch and set pagination parameter
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'children' in data['data']:
            children = data['data']['children']
            for post in children:
                hot_list.append(post['data']['title'])
                for word in word_list:
                    word_lower = word.lower()
                    title_lower = post['data']['title'].lower()
                    if word_lower in title_lower.split():
                        counts[word_lower] = counts.get(word_lower, 0) + 1
            after = data['data']['after']  # Get the 'after' parameter for pagination
            if after is not None:
                return count_words(subreddit, word_list, hot_list, after, counts)  # Recursively call the function with the 'after' parameter
            else:
                sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
                for word, count in sorted_counts:
                    print("{}: {}".format(word, count))
        else:
            print("No posts found for subreddit '{}'".format(subreddit))
    elif response.status_code == 404:
        print("Subreddit '{}' does not exist.".format(subreddit))
    else:
        print("Error fetching data for subreddit '{}' (Status code: {})".format(subreddit, response.status_code))

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        count_words(sys.argv[1], sys.argv[2].split())

