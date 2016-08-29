# -*- coding: cp437 -*-

from Tkinter import *
from bs4 import BeautifulSoup
import sqlite3, urllib, tkMessageBox


def db_access():
    con = sqlite3.connect('entradas.db')
    con.text_factory = str
    return con


def almacenar():
    urllib.urlretrieve("http://www.sevillaguia.com/sevillaguia/agendacultural/agendacultural.asp", "entradas")
    entradas = open("entradas", "r")
    bs = BeautifulSoup(entradas)
    lista = bs.find_all(class_=["LinkIndice", "TituloIndice"])
    entradas.close()

    con = db_access()
    cursor = con.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS entradas(title text, link text, category text)")

    for i in lista:
        if i.get("class")[0] == "TituloIndice":
            cat = i.string
        else:
            cursor.execute("INSERT INTO entradas VALUES (?, ?, ?)", (i.string, i.get("href"), cat))

    con.commit()
    con.close()

    tkMessageBox.showinfo("","BD creada correctamente")


def mostrar(lista):
    window = Toplevel()
    sb = Scrollbar(window)
    sb.pack(side = RIGHT, fill = Y)
    text = Text(window, yscrollcommand = sb.set)

    for i in lista:
        for j in i:
            text.insert(INSERT, str(j)+"\n")
        text.insert(INSERT, "\n")
    text.pack()
    sb.config(command = text.yview)

def buscar_categoria():
    def categoria_busqueda(event):
        con = db_access()
        cursor = con.cursor()
        string = "%"+entry.get()+"%"
        lista = cursor.execute("SELECT * FROM entradas WHERE category LIKE ?", (string,))
        mostrar(lista)
        con.close()


    window = Toplevel()
    label = Label(window, text = "Introduzca la categoría:")
    entry = Entry(window)
    label.pack(side = LEFT)
    entry.bind("<Return>", categoria_busqueda)
    entry.pack(side = RIGHT)


def buscar_evento():
    def evento_busqueda(event):
        con = db_access()
        cursor = con.cursor()
        string = entry.get()
        lista = cursor.execute("SELECT * FROM entradas").fetchall()

        lista = [i for i in lista if string in i[0]]
        mostrar(lista)
        con.close()


    window = Toplevel()
    label = Label(window, text = "Introduzca una palabra clave:")
    entry = Entry(window)
    label.pack(side = LEFT)
    entry.bind("<Return>", evento_busqueda)
    entry.pack(side = RIGHT)


top = Tk()

fr = Frame(top)
fr.pack()

almacenar = Button(fr, text = "Almacenar", command = almacenar)
almacenar.pack(side = LEFT)

listar = Button(fr, text = "Buscar Categoria", command = buscar_categoria)
listar.pack(side = LEFT)

buscar = Button(fr, text = "Buscar Evento", command = buscar_evento)
buscar.pack(side = LEFT)

top.mainloop()
