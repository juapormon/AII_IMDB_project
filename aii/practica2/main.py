from bs4 import BeautifulSoup
import urllib.request
import tkinter
from tkinter import *
from tkinter import messagebox
import sqlite3

base_url = 'https://zacatrus.es/juegos-de-mesa.html'


def get_links():
    page = urllib.request.urlopen(base_url)
    soup = BeautifulSoup(page, 'lxml')
    games_links = [a['href'] for a in soup.find('ol').find_all('a', class_="product photo product-item-photo")]
    return games_links


# title, comments_num, categories, player_num, editorial
def scrap():
    links = get_links()
    games = []

    for link in links:
        page = urllib.request.urlopen(link)
        soup = BeautifulSoup(page, 'lxml')

        title = str(soup.find('h1', class_='page-title').find('span').string),
        raw_comments = soup.find('div', class_='product info detailed').find('a', id='tab-label-reviews-title')
        raw_categories = soup.find('td', attrs={'data-th': 'Si buscas...'})
        raw_players = soup.find('td', attrs={'data-th': 'Núm. jugadores'})
        raw_editorial = soup.find('td', attrs={'data-th': 'Editorial'})

        if "Comentarios" in raw_comments.contents[0]:
            comments = 0
        else:
            comments = raw_comments.find('span').string

        if isinstance(raw_categories, type(None)):
            categories = None
        else:
            categories = raw_categories.string

        if isinstance(raw_players, type(None)):
            players = None
        else:
            players = raw_players.string

        if isinstance(raw_editorial, type(None)):
            editorial = None
        else:
            editorial = raw_editorial.string

        game = {
            'title': str(title),
            'comments_num': str(comments),
            'categories': str(categories),
            'player_num': str(players),
            'editorial': str(editorial)
        }
        games.append(game)
    else:
        return games


def save_in_db():
    games = scrap()
    conn = sqlite3.connect('practica2.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS GAMES")
    conn.execute('''CREATE TABLE GAMES
            (TITLE          TEXT    NOT NULL,
            COMMENTS_NUM    TEXT,
            CATEGORIES      TEXT,
            PLAYER_NUM      TEXT,
            EDITORIAL       TEXT);''')
    for game in games:
        conn.execute(
            """INSERT INTO GAMES (TITLE, COMMENTS_NUM, CATEGORIES, PLAYER_NUM, EDITORIAL) VALUES (?,?,?,?,?)""",
            (game['title'], game['comments_num'], game['categories'], game['player_num'], game['editorial']))
        conn.commit()
    conn.close()


def juegos_mas_comentados():
    conn = sqlite3.connect('practica2.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT * FROM GAMES LIMIT 3")
    list_games(cursor)
    conn.close()


def editoriales():
    conn = sqlite3.connect('practica2.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT EDITORIAL, COUNT(TITLE) FROM GAMES GROUP BY EDITORIAL")
    list_games_by_editorial(cursor)
    conn.close()


def buscar_por_categoria():
    def listar(Event):
        conn = sqlite3.connect('practica2.db')
        conn.text_factory = str
        cursor = conn.execute("SELECT * FROM GAMES WHERE CATEGORIES LIKE '%" + str(entry.get())+"%'")
        list_games(cursor)
        conn.close()
    conn = sqlite3.connect('practica2.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT CATEGORIES FROM GAMES")
    categories = set()
    for i in cursor:
        categories_games = i[0].split(", ")
        for category in categories_games:
            categories.add(category.strip())
    v = Toplevel()
    entry = Spinbox(v, values=list(categories))
    entry.bind("<Return>", listar)
    entry.pack()
    conn.close()


def buscar_por_jugadores():
    def listar(Event):
        conn = sqlite3.connect('practica2.db')
        conn.text_factory = str
        cursor = conn.execute("SELECT * FROM GAMES WHERE PLAYER_NUM LIKE '%" + str(entry.get())+"%'")
        list_games(cursor)
        conn.close()
    v = Toplevel()
    entry = Entry(v)
    entry.bind("<Return>", listar)
    entry.pack()


def list_games(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        s = 'TITLE: ' + row[0]
        lb.insert(END, s)
        lb.insert(END, "------------------------------")
        s = "     COMMENTS_NUM: " + row[1] + ' | CATEGORIES: ' + row[2] + ' | PLAYER_NUM: ' + row[3] + ' | EDITORIAL: ' + row[4]
        lb.insert(END, s)
        lb.insert(END, "\n\n")
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)


def list_games_by_editorial(cursor):
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        s = 'EDITORIAL: ' + str(row[0]) + ' : ' + str(row[1])
        lb.insert(END, s)
        lb.insert(END, "------------------------------")
        lb.insert(END, "\n\n")
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)


def button_action1():
    save_in_db()
    conn = sqlite3.connect('practica2.db')
    conn.text_factory = str
    count = conn.execute("SELECT COUNT(*) FROM GAMES")
    messagebox.showinfo("Base Datos",
                        "Base de datos creada correctamente \nHay " + str(count.fetchone()[0]) + " registros")
    conn.close()


def button_action2():
    top = Toplevel()
    top.title("Listar")
    button4 = Button(top, text="Juegos más comentados", command=juegos_mas_comentados)
    button4.pack(side=LEFT)
    button5 = Button(top, text="Editoriales", command=editoriales)
    button5.pack(side=LEFT)


def button_action3():
    top = Toplevel()
    top.title("Buscar")
    button4 = Button(top, text="Juegos por categoria", command=buscar_por_categoria)
    button4.pack(side=LEFT)
    button5 = Button(top, text="Juegos por jugadores", command=buscar_por_jugadores)
    button5.pack(side=LEFT)


if __name__ == '__main__':
    window = tkinter.Tk()
    frame = Frame(window)
    frame.pack()
    button1 = Button(frame, text="Almacenar", command=button_action1)
    button1.pack(side=LEFT)
    button2 = Button(frame, text="Listar", command=button_action2)
    button2.pack(side=LEFT)
    button3 = Button(frame, text="Buscar", command=button_action3)
    button3.pack(side=LEFT)
    frame.mainloop()
