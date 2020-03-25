import json

names = {}
count = 0

with open("nicknames.txt") as fp: 
    for line in fp: 
        count += 1
        line = line.replace("\t","")
        a = line.strip().split(',')
        a[1] = a[1].replace("@","")
        a[1] = a[1].replace("https://www.hackerrank.com/","")
        names[a[1]] = a[0]

with open("name_data_file.json", "w") as write_file:
    json.dump(names, write_file)