from itertools import combinations
from simpleai.search import CspProblem,backtrack

#Definimos valores, dominos y constrains
variables = ["mastil","interno1","interno2","frente"]
dominio={}
for var in variables:

    dominio[var] = [
        ("Taladro muestras",15),
        ("Cámara panorámica",3),
        ("Bateria Nuclear",10),
        ("Laser",5),
        ("Microscopio",3),
        ("Sistema Navegacion",8),
        ("Antena",7),
        ("Espacio Muestra",5)
    ]
print (variables)
restricciones = []

def pesoMaximo (variables,values):
    mastil,interno1,interno2,frente = values
    pesoTotal = mastil[1]+interno1[1]+interno2[1]+frente[1]
    return pesoTotal <= 25

restricciones.append((variables,pesoMaximo))

def unicaMejora(variable,values):
    mejora1,mejora2 = values
    return mejora1 != mejora2   #Revisar 

for variable1,variable2 in combinations(variables,2):
    restricciones.append(((variable1,variable2),unicaMejora))

def telescopioConTaladro(variable, values):
    nombres = [v[0] for v in values]
    return not ("Taladro muestras" in nombres and "Microscopio" in nombres)

restricciones.append((variables,telescopioConTaladro))

def antenaSinBateria(variable, values):
    n = [v[0] for v in values]
    return not ("Antena" in n and "Bateria Nuclear" in n)

def laserConBateria(variable, values):
    n = [v[0] for v in values]
    return "Laser" not in n or "Bateria Nuclear" in n

CIENCIA = {"Microscopio", "Laser", "Taladro muestras", "Espacio Muestra"}
def alMenosUnaCiencia(variable, values):
    return any(v[0] in CIENCIA for v in values)

restricciones += [
    (variables, antenaSinBateria),
    (variables, laserConBateria),
    (variables, alMenosUnaCiencia),
]

SLOTS_PERMITIDOS = {
    "Taladro muestras":   {"mastil", "frente"},
    "Cámara panorámica":  {"mastil"},
    "Bateria Nuclear":    {"interno1", "interno2"},
    "Laser":              {"mastil", "frente"},
    "Microscopio":        {"mastil", "frente"},
    "Sistema Navegacion": {"interno1", "interno2"},
    "Espacio Muestra":    {"interno1", "interno2", "frente"},
    "Antena":             {"interno1", "interno2", "mastil"},
}

def slotValido(variable, values):
    slot, = variable
    mejora, = values
    return slot in SLOTS_PERMITIDOS[mejora[0]]

for slot in variables:
    restricciones.append(((slot,), slotValido))

problema = CspProblem(variables, dominio, restricciones)
print(backtrack(problema))



