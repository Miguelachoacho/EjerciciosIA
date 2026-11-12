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
base = (0,1)
muestras = ((0,2),(0,3),(2,0),(3,1))
initial_state= ((0,1),0,(),100) #PosRobot,bool de muestra, tupla con la muestra que recolectó y por ultimo la bateria en %
class problemaSeguridad(SearchProblem):
    
    def actions(self,state):
        posx,posy = state[0]
        movimientosDisponibles = []  #Las acciones que puede realizar el robot
        movimientos = [
            (0,1), # Derecha
            (0,-1), #Izq
            (1,0), #Abajo
            (-1,0) # Arriba
        ]

        for x,y in movimientos:
            if 0 <= posx + x <= 3 and 0 <= posy + y <= 3 and state[3] > 10:
                movimientosDisponibles.append(("Mover",(x,y))) #MOVimientos ortodiagonales dentro del mapade 4 X 4

        if state[0] in muestras and state[3]> 25:
            movimientosDisponibles.append("Tomar Muestra",(state[0]))   ##Tomo la muestra y considero que la pos del robot es donde está la muestra 
        if state[0] == base and state[1] == 1 and state[3] > 5: ##Si estoy en la base y tengo muestra la dejo
            movimientosDisponibles.append("Dejar Muestra")
        if state[0] == base:
            movimientosDisponibles.append("Recargar Bateria")

        return movimientosDisponibles
        
    def result(self, state, action):

        acc,mov = action
        posRobot  = list(state[0])
        carga = state[1]
        muestraCargada = state[2]
        bateria = state[3]

        if acc == "Mover":
            posRobot = (posRobot[0] + mov[0],posRobot[1] + mov[1])
            bateria -= 10
        elif acc == ():

        return  acc

    
        

        return
    