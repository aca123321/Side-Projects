import requests
import os
from bs4 import BeautifulSoup as bs

a = input("Enter a word to find synonyms for from dictionary.com\n")

url = 'https://www.dictionary.com/browse/' + str(a) 
page = requests.get(url)

soup = bs(page.text, 'html.parser')

find = soup.find_all(class_='css-1an5ojz e15p0a5t0')[0].get_text()

rep = "Related Words for " + str(a)
find = find.replace(rep, "")
find = find.replace(", ", " ")
result = find.split(' ')

for i in result:
    print(i)

os.system("pause")
