#!/usr/bin/python3
"""
100-count
"""
import requests

def count_words(subreddit, word_list, after=None, counts={}):
    """
    Recursively queries the Reddit API, parses the titles of all hot articles,
    and prints a sorted count of given keywords.
    """
    if after is None:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?after={after}"

    headers = {'User-Agent': 'Mozilla/5.0'}  # Set a custom User-Agent to prevent errors
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return

    data = response.json()
    posts = data['data']['children']

    if len(posts) == 0:
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print("{}: {}".format(word, count))
        return

    for post in posts:
        title = post['data']['title']
        words = [word.lower() for word in title.split()]
        for word in word_list:
            if word.lower() in words:
                counts[word.lower()] = counts.get(word.lower(), 0) + 1

    after = data['data']['after']
    return count_words(subreddit, word_list, after, counts)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        word_list = sys.argv[2].split()
        count_words(subreddit, word_list)

