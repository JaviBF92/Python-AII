# encoding: latin1
import urllib, re

def extraer_noticias():
    try:
        urllib.urlretrieve("http://www.us.es/rss/feed/portada", "noticias")
        noticias = open("noticias", "r")
        strnoticias = noticias.read()
        lista = re.findall(r'<item>\s*<title>(.*)</title>\s*<link>(.*)</link>\s*<description>(.*)</description>\s*<author>(.*)</author>\s*(<category>.*</category>)?\s*<guid.*</guid>\s*<pubDate>(.*)</pubDate>\s*</item>', strnoticias)
        noticias.close()
        return lista
    except:
        print("Ha habido un error")

def formatear_fecha(s):
    meses={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    fecha = re.match(r'.*(\d\d) (.{3}) (\d{4}).*', s)
    l = list(fecha.groups())
    l[1] = meses[l[1]]
    return tuple(l)

def buscar_fecha(noticias):
    f = raw_input("Introduzca la fecha (dd-mm-aaaa):")
    fecha=re.match(r'(\d\d)-(\d\d)-(\d\d\d\d)', f)
    if not fecha:
        print "Formato de fecha incorrecto"
        return
    enc = False
    for i in noticias:
        if fecha.groups() == formatear_fecha(i[5]):
            print "Título:", i[0]
            print "Link:", i[1]
            print "Fecha: %2s/%2s/%4s\n" % formatear_fecha(i[5])
            enc = True
        if not enc:
            print "No hay noticias para esa fecha"

def imprimir_noticias(noticias):
    for i in noticias:
        print "Titulo: " + i[0]
        print "Link:", i[1]
        print "Fecha: %2s/%2s/%4s\n" % formatear_fecha(i[5])

opcion = raw_input("""Introduzca opcion:
    1.- Mostrar lista
    2.- Buscar
    """)
if opcion == "1":
    imprimir_noticias(extraer_noticias())
elif opcion == "2":
    buscar_fecha(extraer_noticias())
else:
    print "Opcion incorrecta, por favor, introduzca 1 o 2"
