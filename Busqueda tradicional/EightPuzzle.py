from simpleai.search.viewers import WebViewer
from simpleai.search import (SearchProblem,breadth_first,
                             depth_first,limited_depth_first,iterative_limited_depth_first
                             ,astar)

#Definir estado inicial 
# 1 4 2
#   3 5
# 6 7 8
inicialState  = (
    (1,4,2),
    (None,3,5),
    (6,7,8)
)


goalState  = (
    (1,2,3),
    (4,5,6),
    (7,8,None)
)
#Definir estado meta 

#Busca el numero en el array y devulve
def ubicaciónPieza(piece,state):
    for row_index, row in enumerate(state):
        for col_index,current_piece in enumerate(row):
            if current_piece == piece:
                return row_index,col_index
            

class EightPuzzle (SearchProblem):
    
    #Definir metodo actions
    def actions (self,state):
        filaNulo,colNulo = ubicaciónPieza(None,state)
        acciones =[]
        if filaNulo > 0: #Si la fila no es la primera, puedo mover una para abajo
            acciones.append(state[filaNulo -1][colNulo])
        if filaNulo < 2: #Si la fila no es la ultima, puedo mover una para arriba
            acciones.append(state[filaNulo + 1][colNulo])
        if  colNulo > 0: #Si la columna no es la primera, puedo mover una para la izq
            acciones.append(state[filaNulo][colNulo - 1])
        if colNulo < 2: #Si la columna no es la ultima, puedo mover una para la derecha
            acciones.append(state[filaNulo + 1][colNulo + 1])
        return acciones
    

    #Definir costo 
    def cost (self,state1,action,state2):
        return 1 
    
    def is_goal (self,state):
        return state == goalState

    #El result es cuando se aplica las acciones al estado inicial 
    def result (self,state,action):
        filaNulo,colNulo = ubicaciónPieza(None,state) #Ubicación nulo
        filaNum,colNumero = ubicaciónPieza(action,state) #Ubicació pieza a mover
        state_as_list =list(list(row) for row in state) ## Paso la tupla de tupla a una lista de lista
        #Intercambio el vacio el la ubicacion del numero a mover
        state_as_list[filaNulo][colNulo] = action # state[filaNum,colNumero]
        state_as_list[filaNum][colNumero] = None

        newState = tuple(tuple(row) for row in state_as_list) ##Vuelvo a convertir a una tupla tupla
        return newState

problem = EightPuzzle(inicialState)
result = depth_first(problem,graph_search=True)
print(result)

for action,state in result.path():
    print("Action:",action)
    print("State:", state)

    


        