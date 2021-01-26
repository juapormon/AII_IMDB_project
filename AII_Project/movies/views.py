import re, os, shutil
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import csv
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup

# Create your views here.
def imdb_scrape(request):
    if request.method == "POST":
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

        return render(request, 'bs.html', {'result':'The database has been loaded successfully!'})
    
    return render(request, 'bs.html')

def imdb_search(request):
    almacenar_datos()
    return render(request, 'whoosh.html')

def imdb_search_title(request):
    if request.method == "POST":
        return render(request, 'whoosh.html', {'result':'Title'})
    return render(request, 'whoosh.html')

def imdb_search_year(request):
    if request.method == "POST":
        return render(request, 'whoosh.html', {'result':'Year'})
    return render(request, 'whoosh.html')

def imdb_search_rating(request):
    if request.method == "POST":
        return render(request, 'whoosh.html', {'result':'Rating'})
    return render(request, 'whoosh.html')

def imdb_search_all(request):
    if request.method == "POST":
        return render(request, 'whoosh.html', {'result':'All'})
    return render(request, 'whoosh.html')

def almacenar_datos():
    #define el esquema de la información
    schem = Schema(title=TEXT(stored=True), year=NUMERIC(stored=True), rating=NUMERIC(stored=True))
    
    #eliminamos el directorio del Ã­ndice, si existe
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    
    #creamos el Indice
    ix = create_in("Index", schema=schem)
    #creamos un writer para poder añadir documentos al indice
    writer = ix.writer()
    i=0
    lista=extraer_peliculas()
    for pelicula in lista:
        #añade cada pelicula de la lista al índice
        writer.add_document(title=str(pelicula[0]), year=int(pelicula[1]), rating=int(pelicula[2]))    
        i+=1
    writer.commit()
    print("Fin de indexado", "Se han indexado "+str(i)+" peli­culas")    

def extraer_peliculas():
    result = []

    with open("tv_shows.csv",'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        next(reader, None)
        for row in reader:
            year = row[1].replace("(","").replace(")","") #mapear el año porque viene entre parentesis
            result.append({'title':row[0],'year':year,'rating':row[2]})

    return result
