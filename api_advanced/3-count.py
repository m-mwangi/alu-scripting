#!/usr/bin/python3
""" This module uses recursion to get hot articles"""

import json
import requests

def count_words(subreddit, word_list, after=None, word_count=None):
    if word_count is None:
        word_count = {}

    if after is None:
        url = 'https://www.reddit.com/r/{}/hot/.json'.format(subreddit)
    else:
        url = 'https://www.reddit.com/r/{}/hot/.json?after={}'.format(subreddit, after)

    headers = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        return

    data = response.json()
    posts = data['data']['children']

    for post in posts:
        title = post['data']['title'].lower().split()
        for word in word_list:
            word_count[word.lower()] = word_count.get(word.lower(), 0) + title.count(word.lower())

    after = data['data']['after']

    if after is not None:
        count_words(subreddit, word_list, after, word_count)
    else:
        sorted_word_count = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
        sorted_word_count = sorted(sorted_word_count, key=lambda x: x[0])  # Sort alphabetically
        for word, count in sorted_word_count:
            print('{}: {}'.format(word.lower(), count))

if __name__ == '__main__':
    count_words('programming', ['react', 'python', 'java', 'javascript', 'scala', 'no_results_for_this_one'])
