#!/usr/bin/python3
"""Recurse"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """Returns list with titles of all hot articles in a subreddit """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'after': after}
    response = requests.get(
                                url,
                                headers=headers,
                                params=params,
                                allow_redirects=False
                            )

    if response.status_code == 200:
        data = response.json().get('data')
        children = data.get('children') if data else None
        if children:
            for child in children:
                hot_list.append(child.get('data').get('title'))
            after = data.get('after')
            if after:
                return recurse(subreddit, hot_list, after)
            else:
                return hot_list
        else:
            return hot_list
    else:
        return None
