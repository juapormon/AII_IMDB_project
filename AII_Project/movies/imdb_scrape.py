import requests
from bs4 import BeautifulSoup
import csv

webiste_url = 'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250'

list_of_titles = []
list_of_years = []
user_ratings = []

source = requests.get(webiste_url).text
soup = BeautifulSoup(source, 'lxml')

print(soup.title.text)

tbody = soup.tbody
table_rows = tbody.find_all('tr')

for td in table_rows:
    titles_column = td.find_all('td', class_="titleColumn")
    imdb_ratings = td.find_all('td', class_="ratingColumn imdbRating")

    for information in titles_column:
        title = information.a.text
        list_of_titles.append(title)
        year = information.span.text
        list_of_years.append(year)

    for rating in imdb_ratings:
        user_rating = rating.text.strip()
        user_ratings.append(user_rating)

csv_file = open('tv_shows.csv', 'w', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Title', 'Year of Release', 'User Rating'])

for i in range(len(user_ratings)):
    print(list_of_titles[i], "Year", list_of_years[i], "| Rating:", user_ratings[i])
    csv_writer.writerow([list_of_titles[i], list_of_years[i], user_ratings[i]])

csv_file.close()