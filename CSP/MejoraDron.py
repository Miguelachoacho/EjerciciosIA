from itertools import combinations
from simpleai.search import CspProblem,backtrack,min_conflicts

variables = {"Bahia Trasera", "Bahia Delantera","Motores"}
dominio = {}
restricciones = []

for var in variables:
    dominio[var]=[
        ("Bateria adc",3),
        ("Motor P",1),
        ("Motor E",0.5),
        ("Motor Du",1.2),
        ("Camara HD",1.5),
        ("Camara T",1),
        ("Antena pot",0.5),
        ("Sistema Fumigacion Del",2),
        ("Sistema Fumigacion Tra",2)
    ]


LugaresPermitidosPorMejora = {
    "Bateria"
        "Bateria adc" :{"Bahia Trasera", "Bahia Delantera"},
        "Motor P":{"Motores"},
        "Motor E":{"Motores"},
        "Motor Du":{"Motores"},
        "Camara HD":{"Bahia Delantera"},
        "Camara T":{"Bahia Trasera"},
        "Antena pot":{"Bahia Trasera", "Bahia Delantera"},
        "Sistema Fumigacion Del":{"Bahia Trasera", "Bahia Delantera"},
        "Sistema Fumigacion Tra":{"Bahia Trasera", "Bahia Delantera"}
}

def slotValido(variable, values):
    slot = variable
    mejora = values
    return slot in LugaresPermitidosPorMejora[mejora[0]]

def diferentes (variables,values):
    mejora1,mejora2,mejora3 = variables
    return mejora1 != mejora2 != mejora3

for variable1,variable2,variable3 in combinations(variables,3):
    restricciones.append(((variable1,variable2,variable3),diferentes))




def pesoPermitido(variables,values):
    Bahia_Trasera, Bahia_Delantera,Motores = values
    return Bahia_Trasera[1] +  Bahia_Delantera[1] + Motores[1] <= 5

restricciones.append((variables,pesoPermitido))

def motorPesadoBat(variables, values):
    mejora = {mejora[0] for mejora in values} #Revisa la mejora equipada , values trae todas las mejoras
    motor_potente = "Motor P" in mejora
    bateria = "Bateria adc" in mejora

    return not motor_potente or bateria #Si viene motor y no tiene bateria retorna falso

restricciones.append((tuple(variables), motorPesadoBat))

def camarasHd (variables,values):
    mejora = {mejora[0] for mejora in values}
    camara = "Camara HD" in mejora
    motorPotente = "Motor P" not in mejora

    return not(camara and motorPotente) ##No puede estar camara y motor juntos

restricciones.append((tuple(variables), camarasHd))

def instalacionSistFumi(variables,values):
    mejora = {mejora[0] for mejora in values}
    sistema1 = "Sistema Fumigacion Tra" in mejora
    sistema2 = "Sistema Fumigacion Del" in mejora

    return sistema1 and sistema2

restricciones.append((tuple(variables),instalacionSistFumi))

problema = CspProblem(variables, dominio, restricciones)
print(backtrack(problema))



