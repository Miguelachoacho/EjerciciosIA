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

rover_inicio=(0, 0)
bateria_inicial= 20
zonas_sombra=[(0, 1), (0, 2)]
muestras_igneas=[(1, 1), (1, 2)]
muestras_sedimentarias=[(2, 3)]


EstadoInicial = (rover_inicio, bateria_inicial, "percusion", 0,  tuple(muestras_igneas), tuple(muestras_sedimentarias))  # PosRobot,bateria,taladro equipado, cantidad de carga #Muestras pendientes

class ProblemaRover(SearchProblem):
    def actions(self, state):
        acciones = []
        x, y = state[0]
        muestrasIgneas = state[4]
        muestrasSedimentarias = state[5]
        movimientos = [(-1, 0),  # arriba
                        (1, 0),  # abajo
                        (0, -1),  # izquierda
                        (0, 1)]  # derecha
        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 6 and 0 <= ny < 6:
                acciones.append(("moverse", (dx, dy)))

        movimientosOverride = [(-2, 0),  # arriba 2 pos
                                (2, 0),  # abajo 2 pos 
                                (0, -2),  # izquierda 2 pos 
                                (0, 2)]  # derecha 2 pos
        for dx, dy in movimientosOverride:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 6 and 0 <= ny < 6:
                acciones.append(("sobremarcha", (dx, dy)))

        if state[2] == "termico":
            acciones.append(("equipar", "percusion"))
        elif state[2] == "percusion":
            acciones.append(("equipar", "termico"))

        if state[0] in muestras_igneas and state[2] == "termico" and 0 <= state[3] <= 2:  #Si tengo equipado el taladro correcto y tengo lugar
            acciones.append(("recolectar", "ignea"))
        elif state[0] in muestras_sedimentarias and state[2] == "percusion" and 0 <= state[3] <= 2:  #Si tengo equipado el taladro correcto y tengo lugar
            acciones.append(("recolectar", "sedimentaria"))

        if state[0] not in zonas_sombra:
            acciones.append(("recargar", None))
        
        if state[3] == 2 or (len(state[4]) == 0 and len(state[5])==0 and state[3]>0): #Comparo que tenga dos muestras o si no hay ninguna en el mapa y tiene carga
            acciones.append(("depositar",None))

        return acciones

    def result(self, state, action):
        acc,obj = action
        posRobot = list(state[0]) # Paso a lista para poder manipular como se mueve el robot
        taladroEquipado = state[2]
        carga = state[3]
        bateria = state[1]
        muestrasIg = list (state[4])
        muestrasSed = list (state[5])

        if acc == "moverse": 
            posRobot = posRobot[0]+obj[0],posRobot[1]+obj[1]
            bateria -= 1
        if acc == "sobremarcha":
            posRobot = posRobot[0]+obj[0],posRobot[1]+obj[1]
            bateria -= 4
        if acc == "equipar":
            taladroEquipado = obj
            bateria -= 1
        if acc == "recolectar":
            carga += 1
            bateria -= 3
            if obj == "ignea":
                muestrasIg.remove(state[0])
            if obj == "sedimentaria":
                muestrasSed.remove(state[0])
        
        if acc == "recargar": # Como el tope es 20, si tiene más de 10, solo cargo hasta 20
            bateria = min(20, bateria + 10)
        if acc == "depositar": 
            carga = 0
            bateria -= 1
        return tuple(posRobot),bateria,taladroEquipado,carga,tuple(muestrasIg),tuple(muestrasSed)

    def is_goal(self, state):
        return state[3] == 0 and len(state[4]) == 0 and len(state[5]) == 0

    def heuristic(self, state):
        carga = state[3]
        muestrasRestantes = len(state[4]) + len(state[5])
        heristica = muestrasRestantes + int((carga + muestrasRestantes) / 2)
        return heristica

    def cost(self, state, action, state2):
        acc, obj = action
        muestras = state[3]
        if acc == "moverse" or acc == "sobremarcha":
            return 1 
        if acc == "equipar":
            return 3
        if acc == "recolectar":
            return 2 
        if acc == "depositar":
            return muestras
        else:
            return 4

problema = ProblemaRover(EstadoInicial)
result = astar(problema, graph_search=True,viewer=WebViewer())



