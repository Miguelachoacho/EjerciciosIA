from simpleai.search.viewers import WebViewer
from simpleai.search import (SearchProblem,breadth_first,
                             depth_first,limited_depth_first,iterative_limited_depth_first
                             ,astar)

obstaculos = ((1, 2), (2, 2), (3, 3), (0, 4))
posRobot= (4,0)
GOAL= (2,4)

class robotLaberinto(SearchProblem):

    def actions(self,state):
        x,y = state
        acciones = []
        movimientos = [(-1,0), #arriba
                     (1,0),  #abajo
                     (0,-1), #izquierda
                     (0,1)]  #derecha

        for dx,dy in movimientos:
            movRobotX,movRobotY = x + dx, y + dy
            if 0<= movRobotX < 5 and 0 <= movRobotY < 5 and  (movRobotX,movRobotY) not in obstaculos:  #Si no hay paredes y el movimiento no hay obstaculos se mueve
                acciones.append(( dx,dy))
        
        return acciones
    
    def result(self,state,actions):
        posx,posy = state
        nuevaPosx,nuevaPosy = actions
        Nuevostate = posx + nuevaPosx, nuevaPosy + posy
        return Nuevostate
    
    def is_goal(self, state):
        return state == GOAL
    def heuristic(self, state):
        x1,x2 = state
        g1,g2 = GOAL
        distancia = abs((x1 - g1) + (x2-g2))
        return distancia
    
    def cost (self,state,state2,actions):  ##El costo de moverse es 1
        return 1
problem = robotLaberinto(posRobot)  
result = astar(problem,graph_search=True,viewer=WebViewer())
print(result.path())