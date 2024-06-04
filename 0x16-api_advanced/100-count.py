#!/usr/bin/python3
import requests
from collections import Counter
import re

def count_words(subreddit, word_list, after=None, word_counts=None):
    if word_counts is None:
        word_counts = Counter()

    if after is None:
        url = "https://www.reddit.com/r/{}/hot.json?limit=100".format(subreddit)
    else:
        url = "https://www.reddit.com/r/{}/hot.json?limit=100&after={}".format(subreddit, after)
    
    headers = {'User-Agent': 'MyAPI/0.0.1'}
    response = requests.get(url, headers=headers, allow_redirects=False)
    
    if response.status_code != 200:
        print("")
        return

    data = response.json()
    titles = [post['data']['title'].lower() for post in data['data']['children']]

    for title in titles:
        for word in word_list:
            keyword = word.lower()
            if keyword.endswith(('.', '!', '_')):
                keyword = keyword[:-1]  # remove trailing punctuation
            matches = re.findall(r'\b{}\b'.format(re.escape(keyword)), title)  # match whole words
            word_counts[word] += len(matches)

    if data['data']['after'] is not None:
        count_words(subreddit, word_list, data['data']['after'], word_counts)

    if after is None:
        for word, count in sorted(word_counts.items(), key=lambda x: (-x[1], x[0])):
            if count > 0:  # Print only if the count is greater than 0
                print("{}: {}".format(word.lower(), count))

if __name__ == "__main__":
    subreddit = input("Enter the subreddit: ")
    word_list = input("Enter space-separated list of keywords: ").split()
    count_words(subreddit, word_list)

