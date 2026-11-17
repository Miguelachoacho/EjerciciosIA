from itertools import combinations
from simpleai.search import CspProblem,backtrack,min_conflicts

# No puede haber dos robots en la misma habitación, generarían demasiadas molestias para los científicos.
# No puede haber dos robots en habitaciones adyacentes, impedirían demasiado la circulación.
# Las habitaciones restringidas siguen sin poder contener robots.
# Las dos habitaciones que poseen puertas al exterior deben contener un robot.



#Definir variables y valores 

variables = ["robot1","robot2","robot3","robot4","robot5","robot6"]
zonasRestrigidas = ((0,2),(1,3),(2,1))
puertas = ((0,3),(3,2))
#Mapa de 5X4, zonas restringidas son (0,2|1,3|2,1)
celdas_validas = [
    (x, y)
    for x in range(5)
    for y in range(4)
    if (x, y) not in zonasRestrigidas
]

dominios = {v: list(celdas_validas) for v in variables}

restricciones = [] #Acá definimos las restricciones

def differente(variable,values):
    robot1,robot2 = values
    return robot1 != robot2

for robot1,robot2 in combinations(variables,2):
    restricciones.append(((robot1,robot2),differente))

## TTip para valores adyacentes la distancia de manhattan da 1 
def adyacente (variables,values):
    robot1,robot2 = values
    posXrobot1 = robot1[0]
    posYrobot1 = robot1[1]
    posXrobot2 = robot2[0]
    posYrobot2 = robot2[1]
    return abs(posXrobot1-posXrobot2) + abs(posYrobot1-posYrobot2) != 1

for robot1,robot2 in combinations(variables,2):
    restricciones.append(((robot1,robot2),adyacente))
    
def robotPuerta(puerta):
    def restriccion(vars, values):
        return puerta in values
    return restriccion

for robotInPuerta in puertas:
    restricciones.append((tuple(variables), robotPuerta(robotInPuerta)))




