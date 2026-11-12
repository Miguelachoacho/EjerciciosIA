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
from itertools import combinations

state = ({
    10:0,
    30:0,
    60:0,
    80:0,
    120:0,}, (300, 0))

class PuenteProblem(SearchProblem):
    def actions(self,state):
        movimientos = []
        diccionario = state[0]
        linterna = state[1]
        personas_lado_1 = []
        for persona in diccionario:
            if diccionario[persona] == 0:
                personas_lado_1.append(persona)

        combinaciones = list(combinations(personas_lado_1, 2))
        # Combinaciones para el lado 1 antes de pasar al lado dos
        for combs in combinaciones:
            if linterna[1] == 0:
                movimientos.append(combs, "Pasar")

        if linterna[1] == 1:
             for persona in diccionario:
                if diccionario[persona] == 1:
                    movimientos.append(persona, "Volver")

        return movimientos

    def cost(self, state1, state2):
        pass

    def result(state, action):
        linterna = list(state[1])
        personas, act = action
        diccionario = state[0]
        if act == "Pasar":
            linterna[1] = 1
            for persona in personas:
                diccionario[persona] = 1
            linterna[0] -= max(personas)
        else:
            linterna[1] = 0
            linterna[0] -= personas
            diccionario[personas] = 0

        return (diccionario, (linterna))