from simpleai.search.viewers import WebViewer
from simpleai.search import SearchProblem,astar,breadth_first

class problemJarro(SearchProblem):
    #Definir estado inicial 
    def __init__(self, cantJarros):
       self.n = cantJarros
       estadoInicial = tuple([0] * (self.n - 1) + [self.n])
       super(problemJarro, self).__init__(estadoInicial)

    def capacidad(self, jarroSeleccionado, litrosActuales):
        return jarroSeleccionado +1 - litrosActuales

    def is_goal(self, state):
        return all(x == 1 for x in state)

    def actions(self, state):
        acciones = []
        for jarroOrigen, litrosOrigen in enumerate(state):
            for jarroDestino,litrosDestino in enumerate(state):
                if jarroOrigen != jarroDestino and litrosOrigen > 0:
                    acciones.append((jarroOrigen, jarroDestino))
        return acciones

    def result(self, state, action):
        jarraOrigen, jarroDestino = action
        litrosOrigen, litrosDestino = state[jarraOrigen], state[jarroDestino]

        transversar = min(litrosOrigen,self.capacidad(jarroDestino,litrosDestino))

        lista = list(state)
        lista[jarraOrigen] -= transversar
        lista[jarroDestino] += transversar
        return tuple(lista)


    def cost(self, state1, action,state2):
        # Siempre va sumando 1 al total 
        return action[0] + 1

    def heuristic(self, state):
        return len([x for x in state if x == 0])
    
result = astar(problemJarro(4), graph_search=True,viewer=WebViewer())
print(result.path())