#!/usr/bin/python3
"""
Queries the Reddit API and returns the number of subscribers
for a given subreddit
"""
import requests

def count_words(subreddit, word_list, after=None, counts=None):
    if counts is None:
        counts = {word.lower(): 0 for word in word_list}
    
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"after": after, "limit": 100}
    url = f"https://www.reddit.com/r/{subreddit}/hot/.json"
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    
    if response.status_code != 200:
        return None
    
    data = response.json().get("data", {}).get("children", [])
    
    if not data:
        return counts
    
    for post in data:
        title = post.get("data", {}).get("title", "").lower()
        for word in word_list:
            word_lower = word.lower()
            counts[word_lower] += title.count(word_lower)

    after = data[-1].get("data", {}).get("name")
    return count_words(subreddit, word_list, after, counts)

if __name__ == "__main__":
    subreddit = input("Enter subreddit: ").strip()
    words = input("Enter words (comma-separated): ").split(',')
    word_counts = count_words(subreddit, words)
    
    if word_counts is None:
        print(f"Invalid subreddit: {subreddit}")
    else:
        for word, count in word_counts.items():
            print(f"{word.strip()}: {count}")
   
