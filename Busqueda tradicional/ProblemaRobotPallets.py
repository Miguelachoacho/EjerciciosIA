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

initialState = ((0,0),(("A",(0,2)),("B",(2,1))), None) #Pos robot , tuple -> palet y ubicacion , lleva carga
zonaA = (0,3)
zonaB = (3,3)

class problemaRobot(SearchProblem):
    def actions(self,state):
        posx,posy = state[0]
        movimientosDisponibles = []
        movimientos = [
            (0,1), # Derecha
            (0,-1), #Izq
            (1,0), #Abajo
            (-1,0) # Arriba
        ]

        for x,y in movimientos:
            if 0 <= posx + x <= 3 and 0 <= posy + y <= 3:
                movimientosDisponibles.append(("Mover",(x,y))) #MOVEMOS 
        
        for pallet in state[1]:
            nombre,posPallet = pallet
            if posPallet == state[0] and state[2] is None:
                movimientosDisponibles.append((nombre,posPallet)) #Juntamos el pallet
        if state[2] is not None:
            if  state[2][0] == "A" and state[0] == zonaA:
                movimientosDisponibles.append(("Dejar Pallet",zonaA))
            if  state[2][0] == "B" and state[0] == zonaB:
                movimientosDisponibles.append(("Dejar Pallet",zonaB))
    
        return movimientosDisponibles
    
    def result(self, state, action):
            posRobot = list(state[0])
            listaPallet = list(state[1])
            palletCargado = state[2]
            act,pos = action

            if act == "Mover":
                posRobot = (posRobot[0]+ pos[0],posRobot[1]+ pos[1])
            elif act == "Dejar Pallet": 
                palletCargado = None
            else:
                palletCargado = action  # Asigna la tupla completa, ej. ("A", (0,2))
                listaPallet = [p for p in listaPallet if p != action]  # Elimina sin usar pop (evita errores de índice)

            return tuple(posRobot),tuple(listaPallet),(palletCargado)
    
    def is_goal(self, state):
        return len(state[1]) == 0 and state[2] is None
    
    def heuristic(self, state):
        count = 0
        cantidadPallet = len (state[1])
        count += cantidadPallet * 3  # Cantidad de pallet por la energia que consume levantarlos
        count += cantidadPallet * 2  # Cantidad de pallet por la energia que consume dejarlos 
        return count
    
    def cost(self, state, action, state2):
        if action[0] == "Mover":
            return 1
        elif action[0] == "Dejar Pallet":
            return 2
        else:
            return 3
        
problem = problemaRobot(initialState)  
result = astar(problem,graph_search=True,viewer=WebViewer())
##print(result.path())