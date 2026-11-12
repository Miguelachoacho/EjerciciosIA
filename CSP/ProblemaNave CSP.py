from itertools import combinations
from simpleai.search import CspProblem,backtrack,min_conflicts

variables_problema = {"mejora 1", "mejora 2", "mejora 3"}
domains = {}
for variable in variables_problema:
    domains[variable]= [
        ("Baterias",12.5,300),
        ("Brazo",60,50),
        ("ventana",100,550),
        ("Antena",100,550),
        ("laboratorio_Plantas",80,250),
        ("Laboratorio_Exp",75,300),
        ("Computadoras",50,20),
        ("Reciclador",30,10)
    ]
    
print (variable)
constraints =[]

def different(variable,values): # llegan 2 mejoras y deben ser distintas
    mejora1,mejora2 = values
    return mejora1 != mejora2

for variable1,variable2 in combinations(variables_problema,2):
    constraints.append(((variable1,variable2),different))

def platadisponible(variable,values):
    mejora1,mejora2,mejora3 = values
    TotalGastado =mejora1[1] + mejora2[1] + mejora3[1] # Se suman el precio de cada mejora y se limita que no sea mayor a 150 millones
    return TotalGastado <= 150
constraints.append((variables_problema,platadisponible))
def pesoMaximo(variable,values):
    mejora1,mejora2,mejora3 = values
    TotalPeso =mejora1[2] + mejora2[2] + mejora3[2] # Se suman el peso de cada mejora y se limita que no sea mayor a 1 tonelada
    return TotalPeso <= 1000
constraints.append((variables_problema,pesoMaximo))

def compusIncluidas (variables,values):
    mejora1,mejora2,mejora3 = values
    listasmejora = [mejora1[0],mejora2[0],mejora3[0] ]
    if "Computadoras" and "Baterias" in listasmejora:
        return True
    else:
        return False
constraints.append((variables_problema,compusIncluidas))

def laboratorioDispo (variables,values):
    mejora1,mejora2,mejora3 = values
    listasmejora = [mejora1[0],mejora2[0],mejora3[0] ]
    if "laboratorio_Plantas" and "Laboratorio_Exp" in listasmejora:
        return False
    else:
        return True

problem = CspProblem(variables_problema,domains,constraints)
solution = backtrack(problem,variable_heuristic='MOST_CONSTRAINED_VARIABLE',value_heuristic='LEAST_CONSTRAINING_VALUE')
print("Solution: ")
print(solution)
    