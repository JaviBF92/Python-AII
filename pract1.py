#Cadenas ej1

def inserta(str, ch):
    return ch.join(s for s in str)

def reemplaza_espacio(str, ch):
    return str.replace(" ",ch)

def reemplaza_num(str, ch):
    return "".join(["X" if i.isdigit() else i for i in str])


def inserta_cada_tres(str, ch):
    return ch.join([str[i:i+3] for i in range(0, len(str), 3)])

#Cadenas ej2

def subcadena(str1, str2):
    return (str2 in str1)

def orden_alfabetico(str1, str2):
    if str1[0] < str2[0]:
        return str1
    return str2

print inserta("hola", ",")
print reemplaza_espacio("Hola Mundo", "_")
print reemplaza_num("2as34", "X")
print inserta_cada_tres("lskjdlfk", "?")
print subcadena("Acceso Inteligente a la Informacion", "gente")

print orden_alfabetico("alfabeto","betaalfo")

#Tuplas ej1

def campania1(tupla):
    for i in tupla:
        if i[1] == "H":
            print "Estimado " + i[0] + ", vote por mi."
        elif i[1] == "M":
            print "Estimada " + i[0] + ", vote por mi."

def campania2(tupla, org, cant):
    if org > len(tupla) -1 or org + cant > len(tupla):
        print "Tamano de la tupla excedido"
    else:
        filt = tupla[org:org + cant]
        campania1(filt)

#Tuplas ej2

def listado(lista):
    return [i[1] + " " + i[2] + ". " + i[0] for i in lista]

campania1((("Jose", "H"), ("Alvaro", "H"), ("Manu", "H"), ("Ana", "M")))
campania2((("Jose", "H"), ("Alvaro", "H"), ("Manu", "H"), ("Ana", "M")), 2, 2)
print listado([("Boza", "Francisco", "J"), ("Rodriguez", "Laura", "R")])

#Busqueda

def busqueda(cad, lst):
    return [i for i in lst if cad in i[0]]

print busqueda("Romero", [("Maria Romero", "654111227"), ("Jesus Romero", "613550784"), ("Manuel Garcia", "621304877")])

#Diccionarios

def ingresa_nombres():
    agenda = {}
    while True:
        entrada = raw_input("Introduce un nombre: \n")
        if entrada == "*":
            print ("Gracias")
            break
        elif entrada not in agenda:
            tlf = raw_input("Introduce un telefono: \n")
            if tlf == "*":
                print ("Gracias")
                break
            agenda[entrada] = tlf
    return agenda

print ingresa_nombres()

#Objetos

class Corcho:
    def __init__(self, bodega):
        self.bodega = bodega

class Botella:
    def __init__(self, corcho = None):
        self.corcho = corcho

class Sacacorchos:
    def __init__(self):
        self.corcho = None
    def destapar(self, botella):
        self.corcho = botella.corcho
        botella.corcho = None
    def limpiar(self):
        self.corcho = None

corcho = Corcho("La Bodega")
botella = Botella(corcho)
sacacorchos = Sacacorchos()
sacacorchos.destapar(botella)
sacacorchos.limpiar()

#Herencia y polimorfismo

class Personaje:
    def __init__(self, vida, posicion, velocidad):
        self.vida = vida
        self.posicion = posicion
        self.velocidad = velocidad
    def recibir_ataque(self, cantidad):
        self.vida = self.vida - cantidad
        if self.vida <= 0:
            print "El personaje ha muerto"
    def mover(self, direccion, velocidad):
        if direccion == "izquierda":
            self.posicion = self.posicion - velocidad
        elif direccion == "derecha":
            self.posicion = self.posicion + velocidad

class Soldado(Personaje):
    def __init__(self, vida, posicion, velocidad, ataque):
        self.vida = vida
        self.posicion = posicion
        self.velocidad = velocidad
        self.ataque = ataque
    def atacar(self, personaje):
        personaje.vida = personaje.vida - self.ataque

class Campesino(Personaje):
    def __init__(self, vida, posicion, velocidad, cosecha):
        self.vida = vida
        self.posicion = posicion
        self.velocidad = velocidad
        self.cosecha = cosecha
    def cosechar(self):
        return self.cosecha
