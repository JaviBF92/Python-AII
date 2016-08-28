# -*- coding: cp437 -*-

from Tkinter import *
import sqlite3, re, urllib, tkMessageBox

def db_access():
    con = sqlite3.connect('games.db')
    con.text_factory = str
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS games(name text, gr text, link text, date text, rating text, category text)")
    con.commit()
    return con


def almacenar():
    urllib.urlretrieve("http://www.lego.com/es-es/games", "games")
    games = open("games", "r")
    strgames = games.read()
    lista = re.findall(r'<li>\s*<a href=\"([^"]+)\">\s*.*\s*<strong>(.*)</strong>\s*<em>(.*)</em>\s*.*\s*.*\s*<p.*>(.*)T.*\s*.*\s*<p.*>(.*)</p>\s*<p.*>(.*)</p>', strgames)
    games.close()

    con = db_access()
    cursor = con.cursor()

    li = [list(i) for i in lista]
    formatted_list = [[formatear_fecha(i[val]) if val == 3 else i[val].decode('utf-8') for val in [2, 0, 1, 3, 4, 5]] for i in li]

    for i in formatted_list:
        print i
        cursor.execute("INSERT INTO games VALUES (?, ?, ?, ?, ?, ?)", i)

    con.commit()
    con.close()

    tkMessageBox.showinfo("","BD creada correctamente")

def formatear_fecha(s):
    fecha = re.match(r'(\d{4})(\d{2})(\d{2})', s)
    return "-".join(list(fecha.groups())[::-1])

def mostrar(lista):
    window = Toplevel()
    sb = Scrollbar(window)
    sb.pack(side = RIGHT, fill = Y)
    text = Text(window, yscrollcommand = sb.set)

    for i in lista:
        for j in i:
            text.insert(INSERT, j+"\n")
        text.insert(INSERT, "\n")

    text.pack()
    sb.config(command = text.yview)

def listar():
    con = db_access()
    cursor = con.cursor()

    lista = cursor.execute("SELECT * FROM games")
    mostrar(lista)

    con.close()

def buscar():
    def evento_busqueda(event):
        if var.get() == 0:
            evento_busqueda_nombre(event)
        else:
            evento_busqueda_grupo(event)

    def evento_busqueda_nombre(event):
        con = db_access()
        cursor = con.cursor()
        string = "%"+entry.get()+"%"
        lista = cursor.execute("SELECT * FROM games WHERE name LIKE ?", (string,))
        mostrar(lista)
        con.close()

    def evento_busqueda_grupo(event):
        con = db_access()
        cursor = con.cursor()
        string = "%"+entry.get()+"%"
        lista = cursor.execute("SELECT * FROM games WHERE gr LIKE ?", (string,))
        mostrar(lista)
        con.close()

    window = Toplevel()
    top = Frame(window)
    top.pack()
    bottom = Frame(window)
    bottom.pack(side=BOTTOM)
    label = Label(top, text = "Introduzca el parámetro:")
    entry = Entry(top)
    var = IntVar()
    r1 = Radiobutton(bottom, text = "Nombre", variable=var, value = 0)
    r2 = Radiobutton(bottom, text = "Grupo", variable=var, value = 1)
    label.pack(side = LEFT)
    entry.bind("<Return>", evento_busqueda)
    entry.pack(side = RIGHT)
    r1.pack(anchor=W)
    r2.pack(anchor=W)

top = Tk()

fr = Frame(top)
fr.pack()

almacenar = Button(fr, text = "Almacenar", command = almacenar)
almacenar.pack(side = LEFT)

listar = Button(fr, text = "Listar", command = listar)
listar.pack(side = LEFT)

buscar = Button(fr, text = "Buscar", command = buscar)
buscar.pack(side = LEFT)

top.mainloop()
