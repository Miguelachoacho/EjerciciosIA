from simpleai.search import SearchProblem, astar

ORDEN = ("M", "AC", "P")
ESTADO_INICIAL = (
    (("X2", "X3"), ("AC", "X1", "M"), ("P",)),
    ()
)


class ProblemaCarguero(SearchProblem):

    def actions(self, state):
        pilas, barco = state
        acciones = []

        for origen, pila in enumerate(pilas):
            if not pila:
                continue

            carga = pila[0]

            if len(barco) < len(ORDEN) and carga == ORDEN[len(barco)]:
                acciones.append(("cargar", origen))

            for destino, pila_destino in enumerate(pilas):
                if origen == destino or len(pila_destino) >= 3:
                    continue

                if pila_destino and (
                    carga == "M" or pila_destino[0] == "AC"
                ):
                    continue

                acciones.append(("mover", origen, destino))

        return acciones

    def result(self, state, action):
        pilas, barco = state
        pilas = list(pilas)

        tipo, origen = action[:2]
        carga = pilas[origen][0]
        pilas[origen] = pilas[origen][1:]

        if tipo == "cargar":
            barco += (carga,)
        else:
            destino = action[2]
            pilas[destino] = (carga,) + pilas[destino]

        return tuple(pilas), barco

    def is_goal(self, state):
        return state[1] == ORDEN

    def cost(self, state, action, state2):
        return 1

    def heuristic(self, state):
        pilas, barco = state
        estimacion = 0

        for carga in ORDEN[len(barco):]:
            estimacion += 1
            for pila in pilas:
                if carga in pila:
                    estimacion += pila.index(carga)

        return estimacion


problema = ProblemaCarguero(ESTADO_INICIAL)
resultado = astar(problema)

for accion, estado in resultado.path():
    print(accion, estado)