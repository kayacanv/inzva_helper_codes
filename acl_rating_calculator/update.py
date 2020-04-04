import os
import sys
import string
import random
import requests
import json
from os import path
def get_json(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    resp = requests.get(url=url,headers=headers)
    json_data = resp.json()
    return json_data
def update_contest(contest_name):
    data= {}
    contest_rank = {}
    names = {}
    if path.isfile("data.json"):
        with open("data.json", "r") as read_file:
            data = json.load(read_file)
    if path.isfile("name_data_file.json"):
        with open("name_data_file.json", "r") as read_file:
            names = json.load(read_file)
    url = "https://www.hackerrank.com/rest/contests/"+contest_name+""
    contest_json = get_json(url)
    start_time_epoch = contest_json["model"]["epoch_starttime"]

    def add_person(nick):
        a = {}
        if nick in names:
            a["FullName"] = names[nick]
        else:
            a["FullName"] = "Not Registered"
        a["Total Problem Solved"] = 0
        a["Secret_Rating"] = 500
        a["Rating"] = 0
        a["Rating History"] = {}
        a["Medals"] = {"Platinum" : 0,"Gold" : 0,"Silver" : 0,"Bronze" : 0}
        data[nick]=a

    def get_rankings():
        url = "https://www.hackerrank.com/rest/contests/"+contest_name+"/leaderboard?limit=200"
        json_data = get_json(url)
        l = []
        plc = 1
        for i in json_data['models']:   
            nick = i['hacker']
            l.append(nick)
            contest_rank[nick]=i['rank']
            if nick not in data:
                add_person(nick)
            data[nick]["Total Problem Solved"]= data[nick]["Total Problem Solved"]+ i['solved_challenges']
        return l

    def test_value(a,i): ## if i. person has rank a, what is her expected seed
        val=1
        for j in l:
            if i is not j:
                val+=1/(1+10**( (a-data[j]["Secret_Rating"])/200))
        return val

    def give_medals(l):
        data[l[0]]["Medals"]["Platinum"]+=1
        last=1
        n = len(l)
        if n > 15 and n < 25:
            n=25
        for i in range(n*4//100):
            data[l[last]]["Medals"]["Gold"]+=1
            last+=1
        for i in range(n*8//100):
            data[l[last]]["Medals"]["Silver"]+=1
            last+=1
        for i in range(n*12//100):
            data[l[last]]["Medals"]["Bronze"]+=1
            last+=1

    l = get_rankings()
    new_ratings = {} # Change ammount

    give_medals(l)

    sums = 0 # Total change
    for i in l:
        seed = test_value(data[i]["Secret_Rating"],i) ## calculate what is ur expected seed 
        geo = (contest_rank[i]*seed)**0.5 ## it is geometric so it is close the higher one , increasing is easier than decreasing
        x=0   # Min Rating Value
        y=10000 # Max Rating Value 
        while x < y: ## binary search to find out new rating 
            if test_value( (x+y)//2 , i )<geo:
                y=(x+y)//2
            else:
                x=(x+y)//2+1
        new_ratings[i] = (x-data[i]["Secret_Rating"])//2 # Again increase as halfway
        sums += new_ratings[i]

    sums//=len(l) ## get avarage total change

    for i in new_ratings:
        new_ratings[i] = data[i]["Secret_Rating"] + new_ratings[i] - sums



    for i in l:
        data[i]["Rating"] = (data[i]["Rating"] + new_ratings[i])//2
        data[i]["Secret_Rating"] = new_ratings[i]
        data[i]["Rating History"][start_time_epoch]=data[i]["Rating"]
    
    with open("data.json", "w") as write_file:
        json.dump(data, write_file)

update_contest("inzva-algorithm-competition-league-contest-1")
update_contest("inzva-algorithm-competition-league-contest-2")
update_contest("inzva-algorithm-competition-league-contest-3")
update_contest("inzva-algorithm-competition-league-contest-4")
update_contest("inzva-algorithm-competition-league-contest-5")
update_contest("inzva-algorithm-competition-league-contest-6")
update_contest("inzva-algorithm-competition-league-contest-7")

