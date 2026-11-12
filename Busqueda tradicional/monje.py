from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    limited_depth_first,
    uniform_cost,
    iterative_limited_depth_first,
    greedy,
    astar,
)
from simpleai.search.viewers import BaseViewer, WebViewer

EI = (('m', 'm', 'm','c','c','c'),(),0)

GOAL = ((),('m','m','m','c','c','c'), 1)

class MonjesCanibales(SearchProblem):
    def cost(self, state, action, state2):
        return 1
    
    def is_goal(self, state):
        return len(state[1]) == 6
    
    def actions(self, state):
        barco = state[2]  #el barco esta en 4
        
        acciones = [] #todas las acciones posibles

        for m in range(3):
            for c in range(3):
                total_personas_moviendose = m + c
                lado_origen = state[barco]
                if total_personas_moviendose >= 1 and total_personas_moviendose <= 2:
                    if lado_origen.count('m') >= m and lado_origen.count('c') >= c:
                        nueva_accion = ('m' * m + 'c' * c)
                        nuevo_estado = self.result(state, nueva_accion)
                        if self.estado_valido(nuevo_estado):
                            acciones.append(nueva_accion)
        return acciones
    
    def estado_valido(self, state):
        for n in [0, 1]:
            if state[n].count('m') < state[n].count('c') and state[n].count('m') > 0:
                return False
        return True

    def result(self, state, action):
        lado_izq, lado_der, barco = state
        personas_moviendose = list(action) # esto hace que mc se transforme en 'm', 'c'

        # creo una copia del estado actual

        lado_izq_new = list(lado_izq)
        lado_der_new = list(lado_der)

        if barco == 0:
            for persona in personas_moviendose:
                lado_izq_new.remove(persona)
                lado_der_new.append(persona)
            nuevo_estado = (tuple(lado_izq_new), tuple(lado_der_new), 1)
        
        if barco == 1:
            for persona in personas_moviendose:
                lado_izq_new.append(persona)
                lado_der_new.remove(persona)
            nuevo_estado = (tuple(lado_izq_new), tuple(lado_der_new), 0)
        
        return nuevo_estado

    def heuristic(self, state):
        return len(state[0]) / 2
    
#result = breadth_first(MonjesCanibales(EI))
result = astar(MonjesCanibales(EI))

for action, state in result.path():
    print("action:", action)
    print("state:", state)

print("Depth:", len(list(result.path())))




