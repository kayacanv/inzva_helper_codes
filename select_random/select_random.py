import requests
import random
import json
import os

def get_json(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    resp = requests.get(url=url,headers=headers)
    json_data = resp.json()
    return json_data

def select_nth_random(contest_name):
    url = "https://www.hackerrank.com/rest/contests/"+contest_name+"/leaderboard?limit=200"
    json_data = get_json(url)
    a = []
    seed = 0
    for i in json_data['models']:
        seed += i['solved_challenges']
        if i['solved_challenges'] > 0:
            a.append(i['hacker'])

    if os.path.isfile("name_data_file.json"):
        with open("name_data_file.json", "r") as read_file:
            names = json.load(read_file)
    print('seed:', seed)
    random.seed(seed) #Here we give number of all solved questions.

    print(len(names.keys()))
    winner = random.choice(a)
    while not winner in names.keys():
        winner = random.choice(a)
    return (winner, names[winner])

if __name__ == '__main__':
    x = int(input('Select contest: '))
    print(select_nth_random("inzva-algorithm-competition-league-3-contest-" + str(x)))
