import requests
import random

def get_json(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    resp = requests.get(url=url,headers=headers)
    json_data = resp.json()
    return json_data

def select_nth_random(contest_name, n):
    url = "https://www.hackerrank.com/rest/contests/"+contest_name+"/leaderboard?limit=200"
    json_data = get_json(url)
    random.seed(str(json_data)) #Here we give whole json data as a seed to be fair.
    a = []
    for i in json_data['models']:
        if i['solved_challenges'] > 0:
            a.append(i['hacker'])

    for i in range(n): # if the first selected winner is not registered, we will choose the second winner with the same seed.
        winner = random.choice(a)
    return winner

if __name__ == '__main__':
    print(select_nth_random("inzva-algorithm-competition-league-contest-1", 1))
