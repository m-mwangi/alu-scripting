#!/usr/bin/python3
"""This module uses recursion to get hot articles"""

import json
import requests

def count_words(subreddit, word_list, after=None, hot_list=None):
    """Function that queries the Reddit API."""
    if hot_list is None:
        hot_list = [0] * len(word_list)

    if after is None:
        url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    else:
        url = "https://www.reddit.com/r/{}/hot.json?after={}".format(subreddit, after)

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code == 200:
        data = response.json()

        for topic in data['data']['children']:
            for word in topic['data']['title'].split():
                for i in range(len(word_list)):
                    if word_list[i].lower() == word.lower():
                        hot_list[i] += 1

        after = data['data']['after']

        if after is None:
            save = set()
            for i in range(len(word_list)):
                for j in range(i + 1, len(word_list)):
                    if word_list[i].lower() == word_list[j].lower():
                        save.add(j)
                        hot_list[i] += hot_list[j]

            sorted_indices = sorted(range(len(word_list)), key=lambda k: (-hot_list[k], word_list[k].lower()))
            for i in sorted_indices:
                if hot_list[i] > 0 and i not in save:
                    print("{}: {}".format(word_list[i].lower(), hot_list[i]))
        else:
            count_words(subreddit, word_list, after, hot_list)

if __name__ == '__main__':
    count_words('programming', ['react', 'python', 'java', 'javascript', 'scala', 'no_results_for_this_one'])
