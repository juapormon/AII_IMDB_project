import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox


def juegos_mas_comentados():
    conn = sqlite3.connect('practica2.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT * FROM GAMES LIMIT 3")
    conn.close
    list_games(cursor)


def editoriales():
    conn = sqlite3.connect('practica2.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT EDITORIAL e, (SELECT COUNT(TITLE) FROM GAMES WHERE EDITORIAL LIKE e) FROM GAMES")
    conn.close
    list_games(cursor)


def buscar_por_categoria():
    top4= TopLevel()
    def listar(Event):
        conn = sqlite3.connect('practica2.db')
        conn.text_factory = str
        cursor = conn.execute("SELECT * FROM GAMES WHERE CATEGORIES LIKE '%" + str(entry.get())+"%'")
        conn.close
        list_games(cursor)
    conn = sqlite3.connect('practica2.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT CATEGORIES FROM GAMES")
    categories=set()
    for i in cursor:
        categories_games = i[0].split(", ")
        for category in categories_games:
            categories.add(category.strip())
    entry = Spinbox(v, values=list(categories))
    entry.bind("<Return>", listar)
    entry.pack()
    conn.close()


def buscar_por_jugadores():
    def listar(Event):
        conn = sqlite3.connect('practica2.db')
        conn.text_factory = str
        cursor = conn.execute("SELECT * FROM GAMES WHERE NUM_PLAYERS LIKE '%" + str(entry.get())+"%'")
        conn.close
        list_games(cursor)
    v = tkinter.TopLevel()
    entry = Entry(v)
    entry.bind("<Return>", listar)
    entry.pack()


def list_games(cursor):
    v = TopLevel()
    sc = Scrollbar(v)
    sc.pack(sudo=RIGHT, fill=Y)
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


def button_action1():
    almacenar_db()
    conn = sqlite3.connect('practica2.db')
    conn.text_factory = str
    count = conn.execute("SELECT COUNT(*) FROM GAMES")
    messagebox.showinfo("Base Datos",
                        "Base de datos creada correctamente \nHay " + str(count.fetchone()[0]) + " registros")


def button_action2():
    top = Toplevel()
    top.title("Listar")
    button4 = Button(top, text="Juegos más comentados", command=juegos_mas_comentados)
    button4.pack(side=LEFT)
    button5 = Button(top, text="Editoriales", command=editoriales)
    button5.pack(side=LEFT)


def button_action3():
    top2 = Toplevel()
    top2.title("Buscar")
    button4 = Button(top2, text="Juegos por categoria", command=buscar_por_categoria)
    button4.pack(side=LEFT)
    button5 = Button(top2, text="Juegos por jugadores", command=buscar_por_jugadores)
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