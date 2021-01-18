from bs4 import BeautifulSoup
import urllib.request
import tkinter
from tkinter import *
from tkinter import messagebox
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
import os.path
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.query import *

base_url = 'https://www.meneame.net/'

schema = Schema(
    titulo=TEXT,
    autor=TEXT,
    fuente=TEXT(stored=True),
    link=TEXT,
    fecha=TEXT,
    contenido=TEXT(stored=True)
)


def create_urls(n=0):
    urls = [base_url]
    if n == 0:
        return urls
    for i in range(n+1):
        urls.append(base_url + f'/?page={i+2}')
    return urls


def create_index():
    if not os.path.exists("index"):
        os.mkdir("index")
    ix = create_in("index", schema)
    return ix


def write(pages=3):
    ix = open_dir("index")
    writer = ix.writer()
    
    urls = create_urls(pages)
    for url in urls:
        f = urllib.request.urlopen(url)
        soup = BeautifulSoup(f, 'lxml')
        h2s = soup.findAll('h2')
        for h2 in h2s:
            print(h2)

        # writer.add_document(
        #     titulo=u"My document",
        #     autor=u"This is my document!",
        #     fuente=u"/a",
        #     link=u"first short",
        #     fecha=u"/icons/star.png",
        #     contenido=''
        # )

    writer.commit()


def cargar():
    return None


def buscar_por_noticia():
    return None


def buscar_por_fuente():
    return None


def principal_window():
    raiz = Tk()

    menu = Menu(raiz)

    # DATOS
    menudatos = Menu(menu, tearoff=0)
    menudatos.add_command(label="Cargar", command=cargar)
    menudatos.add_command(label="Salir", command=raiz.quit)
    menu.add_cascade(label="Datos", menu=menudatos)

    # BUSCAR
    menubuscar = Menu(menu, tearoff=0)
    menubuscar.add_command(label="Noticia", command=buscar_por_noticia)
    menubuscar.add_command(label="Fuente", command=buscar_por_fuente)
    menu.add_cascade(label="Buscar", menu=menubuscar)

    raiz.config(menu=menu)
    raiz.mainloop()


if __name__ == '__main__':
    create_index()
    write()
