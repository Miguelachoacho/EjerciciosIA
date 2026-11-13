# El ejercicio consiste en encontrar una secuencia óptima de acciones para que el robot recolecte todas las muestras [M] 
# y las entregue en la base en el menor tiempo total posible, sin que la batería llegue a 0% en ningún momento.

# Estado inicial: PosRobot, carga (el robot lleva carga? 1 si, 0 no), muestra recolectada, cant bateria.

# Estado objetivo: Todas las regiones [M] muestreadas y entregadas en la base.

# Acciones y costos: Moverse (5 min, -10% bat), Tomar muestra (15 min, -25% bat), Dejar muestras en base (10 min, -5% bat) y Cargar en base (30 min, bat al 100%).
# Restricción crítica: La batería debe ser mayor a 0% tras cada acción, obligando al robot a planificar regresos a la base para recargar cuando sea necesario.

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
muestras = list((0,2),(0,3),(2,0),(3,1))
initial_state= ((0,1),0,(()),100) #PosRobot,bool de muestra, tupla con la muestra que recolectó y por ultimo la bateria en %
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
        elif acc == "Tomar Muestra":
            muestraCargada = posRobot #Seteo la muestra
            muestras.remove(posRobot) ##Saco de pool de muestras la muestrra
            bateria -= 25
            carga = 1
        elif acc == "Dejar Muestra":
            bateria -= 5
            carga = 0
        else: ##Por defecto la unica acción que queda es recargar
            bateria = 100

        return tuple((posRobot),carga,muestraCargada,bateria)

    def cost (self,state,action,state2):
        acc,mov = action

        if acc == "Mover":
            return 5
        elif acc == "Tomar Muestra":
            return 15
        elif acc == "Dejar Muestra":
            return 10
        else:
            return 30
    def is_goal(self, state):
        return muestras.len()==0 and state[0] == base
    
    def heuristic(self, state):

        return super().heuristic(state)

problem = problemaSeguridad(initial_state)  
result = astar(problem,graph_search=True,viewer=WebViewer())
    ##print(result.path())

