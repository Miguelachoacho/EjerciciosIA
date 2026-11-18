from simpleai.search import (SearchProblem,astar)
from math import ceil
estadoInicial = ((5,2,4,5,8),())
pesoMaxCaja = 10
class mudanzaProblem (SearchProblem):
    def actions(self, state):  
        pendientes,cajas = state
        objeto = pendientes[0]
        acciones = []

        for i, caja in enumerate(cajas):
            if sum (caja) + objeto <= pesoMaxCaja:
                acciones.append(i)
        acciones.append(len(cajas))
        

        return acciones

    def result(self, state, action):
        pendientes, cajas = state
        objeto = pendientes[0]
        cajas = list(cajas)              # las tuplas no se pueden modificar

        if action == len(cajas):         # caja nueva
            cajas.append((objeto,))
        else:                            # caja existente
            cajas[action] = cajas[action] + (objeto,)

        return (pendientes[1:], tuple(cajas))

    def cost(self, state, action, state2):
        cajas = state[1]
        return 1 if action == len(cajas) else 0

    def is_goal(self, state):
        return state[0] == ()

    def heuristic(self, state):
        pendientes, cajas = state
        libre = sum(pesoMaxCaja - sum(c) for c in cajas)
        resto = sum(pendientes) - libre
        return max(0, ceil(resto / pesoMaxCaja)) ## Ceil redondea al entero más ceracano

problem = mudanzaProblem(estadoInicial)
result = astar(problem, graph_search=True)
print(result.state[1])
print("Cajas:", result.cost)