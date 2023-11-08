#!/usr/bin/python3
"""
Queries the Reddit API recursively and prints the count of given keywords
"""
import requests

def count_words(subreddit, word_list, after=None, counts=None):
    if counts is None:
        counts = {}
        for word in word_list:
            counts[word.lower()] = 0
    
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"after": after, "limit": 100}
    url = f"https://www.reddit.com/r/{subreddit}/hot/.json"
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    
    if response.status_code != 200:
        return
    
    data = response.json().get("data", {}).get("children", [])
    
    if not data:
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            if count > 0:
                print(f"{word}: {count}")
        return
    
    for post in data:
        title = post.get("data", {}).get("title", "").lower()
        for word in word_list:
            word_lower = word.lower()
            counts[word_lower] += title.count(word_lower)

    after = data[-1].get("data", {}).get("name")
    count_words(subreddit, word_list, after, counts)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        words = sys.argv[2:]
        count_words(subreddit, words)
