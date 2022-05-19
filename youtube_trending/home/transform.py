import csv
import re
import pandas as pd
import json
from pathlib import Path
region_list = [
        ('VN', 'Vietnam'),
        ('GB', 'United Kingdom'),
        ('CA', 'Canada'),
        ('DE', 'Germany'),
        ('KR', 'South Korea'),
        ('RU', 'Russia'),
        ('UA', 'Ukraine'),
        ('JP', 'Japan'),
        ('US', 'United States'),
        ('HK', 'Hong Kong'),
]

for region in region_list:

    path_json = Path(__file__).parent / f"category_list/{region[0]}_category_id.json"
    # f = open(f'./category_list/{region[0]}_category_id.json')
    f = open(path_json)
    data = json.load(f)
    print(data)
    category_list = []
    count = 0
    for i in data:
        print(f"id: {i['id']}")
        print(f"title: {i['snippet']['title']}")
        category_list.append({ 'id': i['id'], 'title': i['snippet']['title']})
        print(f"category_list[{count}]: {category_list[count]}")
        print(f"id: {category_list[count]['id']}")
        print(f"title: {category_list[count]['title']}")
        count = count + 1

    f.close()
    def TransformDate(date):
        #print(f"date: {date}")
        for i in range(10):
            print(f"date[{i}]: {date[i]}")       
            pass
        c = 0
        for i in date:
            s = i.split(".")
            
            r = "20" + s[0] + "-" + s[2] + "-" + s[1]
            if(c<10):
                print(f"c = {c}, s = {s}, r = {r}") # s = [<20>"yy", "dd", "mm"]
            date[c] = r
            c = c + 1
            pass
        pass

    def TransformCategoryId(cateid):
        c = 0
        r = []
        l = len(category_list)
        for i in cateid:
            print(f"\t- i: {i}")
            flag = False
            for j in range(l):
                if(int(i) == int(category_list[j]["id"])):
                    #print(f"j: {j}")
                    r.append(category_list[j]["title"])
                    flag = True
            if(flag == False):
                r.append("unknown")
            print(f"r[{c}] = {r[c]}")
            c = c + 1
            pass
        pass
        return r

    path_csv = Path(__file__).parent / f"data/{region[0]}_*.csv"
    data = pd.read_csv("CAvideos.csv")
    print(data.columns)
    print(data.head(20)["trending_date"])
    print(data.head(20)["trending_date"])

    print("=========")

    data["category_name"] = TransformCategoryId(data["category_id"])
    TransformDate(data["trending_date"])

    print(data.head(20)["trending_date"])

    data.to_csv("CAvideos_new.csv", index=False)
    print(data.columns)
