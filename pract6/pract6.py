from whoosh.index import create_in
from whoosh.fields import *
from whoosh.query import *
from whoosh.qparser import QueryParser
import os.path

schema = Schema(remitente=TEXT, contenido=TEXT (stored=True))
if not os.path.exists("index"):
    os.mkdir("index")
index = create_in("index", schema)
writer = index.writer()

diccionario = {}
with open("Agenda/agenda.txt", "r") as agenda:
    lineas = agenda.readlines()

keys = lineas[::2]
values = lineas[1::2]

for i in range(len(keys)):
    if values[i][-2:] == "\r\n":
        diccionario[keys[i][:-2]] = values[i][:-2]
    else:
        diccionario[keys[i][:-2]] = values[i]

for i in os.listdir("Correos"):
        if not os.path.isdir(i):
            ruta = "Correos/"+i
            with open(ruta, "r") as doc:
                lines = doc.readlines()
            mail = lines[0]
            if mail[-2:] == "\r\n":
                mail = mail[:-2]
            contenido = lines[3:]
            writer.add_document(remitente=unicode(diccionario[mail]), contenido= unicode("".join(contenido)))
writer.commit()

element = raw_input("Ingrese el nombre del remitente:\r\n ")

searcher = index.searcher()
parser = QueryParser("remitente", index.schema)
query = parser.parse(element)
result = searcher.search(query)
print("Tiene " + str(len(result)) + " mensaje(s). \n")

for i in result:
    print i["contenido"] + "\n"
