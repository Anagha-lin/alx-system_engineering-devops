import requests

def count_words(subreddit, word_list, after=None, count_dic=None):
    """
    Recursively queries the Reddit API, parses the titles of all hot articles,
    and prints a sorted count of given keywords.

    Args:
        subreddit (str): The subreddit to query.
        word_list (list): List of keywords to count occurrences of.
        after (str): Parameter for pagination to get the next set of results (default None).
        count_dic (dict): Dictionary to store the counts of keywords (default None).

    Returns:
        None
    """
    if count_dic is None:
        count_dic = {}

    headers = {'User-Agent': 'Anagha-lin'}
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    params = {'after': after} if after else {}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json().get('data', {})
        after = data.get('after')

        for child in data.get('children', []):
            title = child['data']['title']
            for word in word_list:
                if word.lower() in title.lower().split():
                    count_dic[word.lower()] = count_dic.get(word.lower(), 0) + 1

        if after:
            count_words(subreddit, word_list, after, count_dic)
        else:
            sorted_counts = sorted(count_dic.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print("{}: {}".format(word, count))

    elif response.status_code == 404:
        print("Subreddit '{}' does not exist.".format(subreddit))
    else:
        print("Error fetching data for subreddit '{}' (Status code: {})".format(subreddit, response.status_code))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        count_words(sys.argv[1], sys.argv[2].split())

