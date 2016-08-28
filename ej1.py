# encoding: latin1

from Tkinter import *
import sqlite3, re, urllib, tkMessageBox

def db_access():
    con = sqlite3.connect('noticias.db')
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS noticias(titulo text, link text, date text)")
    con.commit()
    return con


def almacenar():
    urllib.urlretrieve("http://www.us.es/rss/feed/portada", "noticias")
    noticias = open("noticias", "r")
    strnoticias = noticias.read()
    lista = re.findall(r'<item>\s*<title>(.*)</title>\s*<link>(.*)</link>\s*<description>(.*)</description>\s*<author>(.*)</author>\s*(<category>.*</category>)?\s*<guid.*</guid>\s*<pubDate>(.*)</pubDate>\s*</item>', strnoticias)
    noticias.close()

    con = db_access()
    cursor = con.cursor()

    formatted_list = [[i[val].decode('unicode-escape') for val in [0, 1, 5]] for i in lista]

    for i in formatted_list:
        cursor.execute("INSERT INTO noticias VALUES (?, ?, ?)", i)

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
            text.insert(INSERT, j+"\n")
        text.insert(INSERT, "\n")
    text.pack()
    sb.config(command = text.yview)

def listar():

    con = db_access()
    cursor = con.cursor()

    lista = cursor.execute("SELECT * FROM noticias")
    mostrar(lista)

    con.close()

def buscar():
    def evento_busqueda(event):
        con = db_access()
        cursor = con.cursor()
        string = "%"+entry.get()+"%"
        lista = cursor.execute("SELECT * FROM noticias WHERE date LIKE ?", (string,))
        mostrar(lista)
        con.close()


    window = Toplevel()
    label = Label(window, text = "Introduzca el mes(Xxx):")
    entry = Entry(window)
    label.pack(side = LEFT)
    entry.bind("<Return>", evento_busqueda)
    entry.pack(side = RIGHT)


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
