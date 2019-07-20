import requests
from bs4 import BeautifulSoup as bs
import datetime as dt

now = dt.datetime.now()

a = { "RCB": 0 ,"CSK": 0 ,"Mumbai Indians": 0 ,"Delhi Capitals": 0 ,"Rajasthan Royals": 0 ,"Kings XI Punjab": 0 ,"Hyderabad": 0 ,"KKR": 0}

url = "https://www.rediff.com/cricket/report/check-out-the-complete-ipl-12-schedule-indian-premier-league/20190319.htm"
page = requests.get(url)

soup = bs(page.text, 'html.parser')
table = soup.find_all(class_='ptstable')	

td = []

for i in table:
	for j in (i.find_all('td')):
		td.append(j)

count = 0
ignore = 0
for i in td:
	if(ignore >= 18):
		if((ignore-17)%6 == 2 or (ignore-17)%6 == 4):
			for j in i:
				a[j] = a[j] + 1
	ignore = ignore + 1

for i in a:
	print(i + " -> " + str(a[i]))


