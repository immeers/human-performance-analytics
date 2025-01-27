import requests
import re
from bs4 import BeautifulSoup
import csv
import pandas as pd

# URL to scrape
url = "https://www.swimcloud.com/swimmer/685653/meets/"

# Set up headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
meets_array = []
dates_array = []
races_array = []

def scrape_page(url, headers):
    # Send a GET request
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    elements = soup.find_all(class_="c-swimmer-meets__content")
    elem_soup = BeautifulSoup(str(elements), "html.parser")

    meets = elem_soup.find_all("h3")
    dates = elem_soup.find_all("ul", class_="o-list-inline o-list-inline--dotted")
    results = soup.find_all("table",class_="c-table-clean c-table-clean--middle table table-hover")
   

    for date in dates:
        date_li = date.find_all('li')[1]
        if int(date_li.get_text(strip=True)[-4:]) < 2020: #only want meets since I've been in college
            break
        dates_array.append(date_li.get_text(strip=True))


    for meet in meets:
        if len(meets_array) ==  len(dates_array): #stops based on dates we want
            break
        print(meet.text)
        meets_array.append(meet.text)

    
    
        


    for result in results:
        races1 = []

        if len(meets_array) ==  len(races_array): #stops based on dates we want
            break

        for race in result.find_all('tr')[1:4]:
            event = race.find('td').get_text(strip=True)
            time = race.find('a').get_text(strip=True)
            imp = race.find_all('td')[-1].get_text(strip=True) 
            races1.append((event, time, imp))

        if len(races1) < 3: #add extra blanks to ensure length is 3
            for i in range(3 - len(races1)):
                races1.append(('','',''))

        races_array.append(races1)



    next = soup.find_all('a', class_='c-pagination__action')
    next = next[len(next)-2]['href']
    return next

next = scrape_page(url, headers)
prev = 0

while (prev < int(next[-1])): #keep going until next button isn"t there so "next page" become "prev page"
    print(url + next)
    prev = int(next[-1])
    print(prev)
    next = scrape_page(url + next, headers)
    
print(len(meets_array))
print(len(dates_array))
print(len(races_array))
all_results = pd.DataFrame({'Meet': meets_array, 'Date': dates_array, 'Results': races_array})

all_results.to_csv('all_swim_results.csv', index=False)