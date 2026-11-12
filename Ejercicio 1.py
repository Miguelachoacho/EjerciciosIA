from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    limited_depth_first,
    uniform_cost,
    iterative_limited_depth_first,
    greedy,
    astar
)
from simpleai.search.viewers import BaseViewer, WebViewer
from itertools import combinations
rover_inicio=(1,0)
bateria_inicial=20
zonas_sombra=[(0, 1), (0, 2)]
muestras_igneas=[(1, 1),(1,2)]
muestras_sedimentarias=[]
EstadoInicial =(rover_inicio,bateria_inicial,"termico",0,((1,1),(1,2))) # PosRobot,bateria,taladro equipado, cantidad de carga
class Entrega1 (SearchProblem):

    def actions (self,state):
        acciones = []
        x,y = state[0]
        movimientos = [(-1,0), #arriba
                    (1,0),  #abajo
                    (0,-1), #izquierda
                    (0,1)]  #derecha
        for dx,dy in movimientos:
            acciones.append(("moverse",(dx,dy))) #moviento
        
        movimientosOverride = [(-2,0), #arriba
                    (2,0),  #abajo
                    (0,-2), #izquierda
                    (0,2)]  #derecha
        for dx,dy in movimientosOverride:
            acciones.append(("sobremarcha",(dx,dy))) #moviento doble

        if state[2] == "termico":
            acciones.append(("equipar","percusion"))
        elif state[2] == "percusion":
            acciones.append (("equipar","termico"))
        
        if state[0] in muestras_igneas and state[2] == "termico" and state[3] < 2:
            acciones.append(("recolectar","ignea"))
        elif state[0] in muestras_sedimentarias and state[2] == "percusion" and state[3] < 2:
            acciones.append(("recolectar","sedimentaria"))

        if state[0] not in zonas_sombra and state[1]< 10:
            acciones.append(("desplegar paneles", None))

        if state[3] == 2 or (state[3] == 1 and len(state[4]) == 0):
            acciones.append(("depositar",None))
        return (acciones)
    
    def result(self, state, action):
        posrobot = list(state[0])
        bateria = state[1]
        taladro  = state[2]
        carga = state [3]
        muestrasrestantes = list (state[4])
        accion,obj = action

        if accion == "desplegar paneles":
            if bateria >= 10:
                bateria = 20
            else:
                bateria += 10
        elif accion == "moverse":
           posrobot= ( posrobot[0]+obj[0],posrobot[1]+obj[1])
           bateria -= 1
        elif accion =="sobremarcha":
           posrobot= ( posrobot[0]+obj[0],posrobot[1]+obj[1])
           bateria -= 4
        elif accion == "equipar":
            taladro = obj
            bateria -= 1
        elif accion == "recolectar" and state[3] < 2:
            bateria -= 3
            carga += 1
            muestrasrestantes = [m for m in muestrasrestantes if m != tuple(posrobot)] 

        elif(accion == "depositar" and carga == 2) or (carga == 1 and len(state[4]) == 0) :
            carga = 0 
            bateria -= 1

        return tuple(posrobot),bateria,taladro,carga,tuple(muestrasrestantes)

    
    def cost (self,state,action,state2):
        match action[0]:
            case "moverse":
                return 1
            case "equipar":
                return 3
            case "recolectar":
                return 2
            case "depositar":
                return (state[3] * 1) + 1
            case "desplegar paneles":
                return 4 
            case "sobremarcha":
                return 1
            case _:
                return 0

    def is_goal(self, state):
        return state[3] == 0 and len(state[4]) == 0

    def heuristic(self, state):
        pos = state[0]
        carga = state[3]
        muestras_restantes = list(state[4])
        n_restantes = len(muestras_restantes)

        estimacion = 0

        # Costo mínimo de recolectar cada muestra pendiente
        estimacion += n_restantes * 2

        # Costo mínimo de movimiento: llegar a la muestra más cercana
        # Con sobremarcha (mueve 2, costo 1) => ceil(manhattan / 2)
        if n_restantes > 0:
            min_dist = min(
                abs(pos[0] - m[0]) + abs(pos[1] - m[1])
                for m in muestras_restantes
            )
            estimacion += (min_dist + 1) // 2

        # Costo mínimo de depositar (si hay algo que entregar)
        if carga > 0 or n_restantes > 0:
            estimacion += 1  # subestima (real mínimo = carga_al_depositar + 1)

        return estimacion

problem = Entrega1(EstadoInicial)  
result = astar(problem,graph_search=True,viewer=WebViewer())
path =result.path()
for res in path:
    print(res)