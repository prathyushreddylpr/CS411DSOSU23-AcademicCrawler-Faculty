import time
from selenium import webdriver
import json
import urllib.request
from urllib.request import urlopen
from get_data_from_multiple_lists import view_html_structure
from datetime import datetime
import sys
import re
import urllib.parse
import pickle
import csv
import codecs

forbidden = ['google', 'wiki', 'news', 'instagram', 'twitter', 'linkedin', 'criminal', 'course', 'facebook']


def find(university, department):
    possibleURLs = []
    query = university + ' ' + department
    url = 'https://www.google.com/search?q=' + query.replace(' ', '+').replace('/', "%2F").replace('–', '') + '+faculty'
    #print(url)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.google.com/'})
    with urllib.request.urlopen(req) as response:
        r = response.read()
    plaintext = r.decode('utf8')
    links = re.findall("href=[\"\'](.*?)[\"\']", plaintext)
    for i in links:
        k = '/url?q=http'
        flag = True
        for j in forbidden:
            if j in i:
                flag = False
        if len(i) > len(k) and i[:len(k)] == k and flag:
            link = i[7:].split('&amp')[0]
            link = urllib.parse.unquote(link)
            possibleURLs.append(link)

    # for i in possibleURLs:
    #     print(i)

    res_data = {}
    res_url = ''
    res_num = 0

    for url in possibleURLs:
        for option in ['urllib', 'urllibs']:
            # print(option, url)
            try:
                r = view_html_structure(url, option)
            except:
                continue

            if len(r) > 1:
                return r, url
    return res_data, res_url

#universities = ['University Of Illinois at Urbana Champaign']
departments = ['cs', 'ece', 'Math', 'Physics', 'Economics', 'Sociology']
#data, url = find('ucsd', 'cs')
#print(data, url)

universities = []
count = 0
with open('University_updated1.csv', mode ='r')as file: 
  # reading the CSV file
  csvFile = csv.reader(file)
  # displaying the contents of the CSV file
  for lines in csvFile:
        count = count + 1
        if count == 1:
            continue
        universities.append(lines[1])

csv_columns = ['Id','Name','Email','Position','Research Interest', 'Phone number', 'University_Name', 'Department_Id']
id = 1
csv_file = "FacultyCE.csv"
with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for university in universities:
        print(university)
        for department in departments:
            dataset, url = find(university, department)
            for data in dataset:
                data['Id'] = id
                data['University_Name'] = university
                if department == 'cs':
                    data['Department_Id'] = 0
                elif department == 'ece':
                    data['Department_Id'] = 1
                elif department == 'Math':
                    data['Department_Id'] = 2
                elif department == 'Physics':
                    data['Department_Id'] = 3
                elif department == 'Economics':
                    data['Department_Id'] = 4
                else:
                    data['Department_Id'] = 5
                id = id + 1
                for element in csv_columns:
                    if element not in data.keys():
                        data[element] = 'null'
                writer.writerow(data)
        

