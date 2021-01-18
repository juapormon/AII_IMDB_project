from tkinter import *
import os
import datetime
import urllib
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, DATETIME
from tkinter import messagebox
import shutil
from bs4 import BeautifulSoup
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser

def extraer_peliculas():
    #devuelve una lista de tuplas. Cada tupla tiene la información requerida de una noticia
    lista_peliculas = []
    
    for i in range(1,4):
        lista_pagina = extraer_pagina("https://www.elseptimoarte.net/estrenos/"+str(i)+"/")
        lista_peliculas.extend(lista_pagina)
        
    return lista_peliculas


def extraer_pagina(url):
    lista =[]
    
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")
    lista_link_peliculas = s.find("ul", class_="elements").find_all("li")
    for link_pelicula in lista_link_peliculas:
        f = urllib.request.urlopen("https://www.elseptimoarte.net/"+link_pelicula.a['href'])
        s = BeautifulSoup(f, "lxml")
        datos = s.find("main", class_="informativo").find("section",class_="highlight").div.dl
        titulo_original = datos.find("dt",string="Título original").find_next_sibling("dd").string.strip()
        #si no tiene título se pone el título original
        if (datos.find("dt",string="Título")):
            titulo = datos.find("dt",string="Título").find_next_sibling("dd").string.strip()
        else:
            titulo = titulo_original      
        pais = "".join(datos.find("dt",string="País").find_next_sibling("dd").stripped_strings)
        fecha = datetime.strptime(datos.find("dt", string="Estreno en España").find_next_sibling("dd").string.strip(), '%d/%m/%Y')
        generos_director = s.find("div", id="datos_pelicula")
        generos = "".join(generos_director.find("p", class_="categorias").stripped_strings)
        director = "".join(generos_director.find("p", class_="director").stripped_strings)
        sinopsis = ''
        if s.find('div', class_='info'):
            sinopsis = s.find('div', class_='info').string

        lista.append((titulo, titulo_original, pais, fecha, director, generos, sinopsis))



def almacenar_datos():
    #define el esquema de la información
    schem = Schema(titulo=TEXT(stored=True,commas=True), titulo_original=TEXT(stored=True,commas=True), pais=TEXT(stored=True,commas=True), fecha=DATETIME(stored=True,commas=True), director=TEXT(stored=True,commas=True), generos=TEXT(stored=True,commas=True), sinopsis=Text(stored=True,commas=True))
    
    #eliminamos el directorio del índice, si existe
    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    
    #creamos el índice
    ix = create_in("Index", schema=schem)
    #creamos un writer para poder añadir documentos al indice
    writer = ix.writer()
    i=0
    lista=extraer_peliculas()
    for pelicula in lista:
        #añade cada pelicula de la lista al índice
        writer.add_document(titulo=str(pelicula[0]), titulo_original=str(pelicula[1]), pais=str(pelicula[2]), estreno_espanya=pelicula[3], director=str(pelicula[4]), categorias=str(pelicula[5]))    
        i+=1
    writer.commit()
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " películas")

def buscar_generos():
    def mostrar_lista(evento):
        ix=open_dir("Index")
        with ix.searcher as searcher:
            query = QueryParser("contenido", ix.schema).parse(str(en.get()))
            results = searcher.search(query, limit=25)
            v = Toplevel()
            v.title("Listado de películas")
            v.geometry('800x150')
            sc = Scrollbar(v)
            sc.pack(side=RIGHT, fill=Y)
            lb = Listbox(v, yscrollcommand=sc.set)
            lb.pack(side=BOTTOM, fill = BOTH)
            sc.config(command = lb.yview)
            for r in results:
                lb.insert(END, r['titulo'])
                lb.insert(END, r['titulo_original'])
                lb.insert(END, r['pais'])
                lb.insert(END, '')
    v = Toplevel()
    v.title("Busqueda por Género")
    la = Label(v, text="Introduzca palabra a buscar:")
    la.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)


def buscar_titulo_sinopsis():
    def mostrar_lista(event):
        #abrimos el índice
        ix=open_dir("Index")
        #creamos un searcher en el índice
        with ix.searcher() as searcher:
            #se crea la consulta: buscamos en el campo "titulo" y "sinopsis" la palabra que hay en el Entry "en"
            query = MultifieldParser(["contenido","sinopsis"], ix.schema, group.OrGroup).parse(str(en.get()))
            #llamamos a la función search del searcher, pasándole como parámetro la consulta creada
            results = searcher.search(query)
            #recorremos los resultados obtenidos(es una lista de diccionarios) y mostramos lo solicitado
            v = Toplevel()
            v.title("Listado de Películas - Búsqueda: " + str(en.get()))
            v.geometry('800x150')
            sc = Scrollbar(v)
            sc.pack(side=RIGHT, fill=Y)
            lb = Listbox(v, yscrollcommand=sc.set)
            lb.pack(side=BOTTOM, fill = BOTH)
            sc.config(command = lb.yview)
            #Importante: el diccionario solo contiene los campos que han sido almacenados(stored=True) en el Schema
	    p = 0
            for r in results:
		p += 1
	    	lb.insert(END, '['+str(p)+']--------------------------------------------------')
                lb.insert(END, "Título: "+r['titulo'])
                lb.insert(END, "Título original: "+r['titulo_original'])
                lb.insert(END, "Director: "+r['link'])
                lb.insert(END,'')
    
    v = Toplevel()
    v.title("Busqueda por Título o Sinopsis")
    l = Label(v, text="Introduzca palabra a buscar:")
    l.pack(side=LEFT)
    en = Entry(v)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)


def ventana_principal():
    
    root = Tk()
    menubar = Menu(root)
    
    datosmenu = Menu(menubar, tearoff=0)
    datosmenu.add_command(label="Cargar", command=almacenar_datos)
    datosmenu.add_separator()   
    datosmenu.add_command(label="Salir", command=root.quit)
    
    menubar.add_cascade(label="Datos", menu=datosmenu)
    
    buscarmenu = Menu(menubar, tearoff=0)
    buscarmenu.add_command(label="Título o Sinopsis", command=buscar_titulo_sinopsis)
    buscarmenu.add_command(label="Géneros", command=buscar_generos)
    buscarmenu.add_command(label="Fecha", command=buscar_fecha)
    
    menubar.add_cascade(label="Buscar", menu=buscarmenu)
    
    root.config(menu=menubar)
    root.mainloop()


if __name__ == "__main__":
    ventana_principal()
