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
        title = post['data']['title']
        for word in word_list:
            count = title.lower().count(word.lower())
            if word in word_count:
                word_count[word] += count
            else:
                word_count[word] = count

    after = data['data']['after']
    if after is not None:
        count_words(subreddit, word_list, after, word_count)

    return word_count


subreddit = 'unpopular'
word_list = ['down', 'vote', 'downvote', 'you', 'her', 'unpopular', 'politics']
word_count = count_words(subreddit, word_list)
print(word_count)
