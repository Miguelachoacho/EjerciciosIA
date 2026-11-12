from simpleai.search import SearchProblem,astar
from simpleai.search.viewers import WebViewer
class search_RobotPallets(SearchProblem):
    paredes = ((0,0),(0,2),(2,1))
    puntoEntrega = (2,0)
    filas = 3
    columnas = 3
    def __init__(self):
        
        palletsRecolectar =((0,1),(1,2),(1,1))
        robot = (0,1)
        llevaPallets = None

        estadoInicial = (robot,llevaPallets,palletsRecolectar)
        super().__init__(estadoInicial)


    def actions(self, state):
        movientos = [(-1,0), #arriba
                     (1,0),  #abajo
                     (0,-1), #izquierda
                     (0,1)]  #derecha
        
        robot, llevaPallets,palletsRecolectar = state
        acciones = []
        for dx,dy in movientos:
            nuevaPosicion = (robot[0] + dx, robot[1] + dy)
            if nuevaPosicion not in self.paredes:
                            # límites
                if not (0 <= nuevaPosicion[0] < self.filas and 0 <= nuevaPosicion[1] < self.columnas):
                    continue
            
            acciones.append((dx,dy))
        
    
        if (llevaPallets == None and robot in palletsRecolectar):
            acciones.append("Agarrar Pallet")


        if (llevaPallets == True and robot == self.puntoEntrega):
            acciones.append("Soltar Pallet")           
        return acciones

    def result(self, state, action):
        # Define how the state changes based on the action taken
        robot, llevaPallets,palletsRecolectar = state
        if action == 'Agarrar Pallet':
            listaPallets = list(palletsRecolectar)
            listaPallets.remove(robot)
            listaActualizada = tuple(listaPallets)
            return (robot,True,listaActualizada)
        elif action == 'Soltar Pallet':
            return (robot, None, palletsRecolectar)
        else:
            dx, dy = action
            nuevaPosicion = (robot[0] + dx, robot[1] + dy)
            return (nuevaPosicion, llevaPallets, palletsRecolectar)

    def is_goal(self, state):
        robot, llevaPallets, palletsRecolectar = state
        return(len(palletsRecolectar) == 0 and llevaPallets == None)

    def cost(self, state1, action, state2):
        'El costo de la acción es siempre 1'
        return 1
    
    def heuristic(self, state):
        robot, llevaPallets, palletsRecolectar = state
        return len(palletsRecolectar)


result = astar(search_RobotPallets(), graph_search=True,viewer=WebViewer())
print(result)