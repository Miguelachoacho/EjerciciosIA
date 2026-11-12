from simpleai.search import SearchProblem,astar
from simpleai.search.viewers import BaseViewer, WebViewer

posObstaculos = ((0,1),(1,3),(2,2))
posRobot = (2,2)
ZonaA = (1,2)
ZonaB = (3,1)

estadoinicial = (posRobot,(("A",(0,2)),("A",(0,2)),("A",(1,2)),("B",(1,2)),("B",(3,1)),("B",(3,1))),(),((),())) # Pos robot, lista pallets

class problemaFinal(SearchProblem):
    def actions(self, state):
        acciones= []
        posx,posy = state[0]
        PalletAgarrado = state[2]
        movimentos = [
            (-1,0), #Arriba
            (1,0),  #Abajo
            (0,-1), #Izq
            (0,1)   #Derecha
        ]
        for dx,dy in movimentos:
            if 0<= posx + dx <= 3 and 0<= posy + dy <= 3:
                acciones.append(("Moverse",(dx,dy)))
        
        for caja in state[1]:
            tipo,pos = caja        
            if state[0] == pos and state[2] == ():
                acciones.append(("Agarrar Pallet", caja))
        if state[2] != ():
            cajaCargada = state[2]  #Caja cargada 
            if cajaCargada[0] == "A" and state[0] == ZonaA and PalletAgarrado != ():
                acciones.append(("Soltar Pallet",()))
            elif cajaCargada[0] == "B" and state[0] == ZonaB and PalletAgarrado !=():
                acciones.append(("Soltar Pallet",()))

        return acciones
    
    def result (self,state,actions):
        posRobot = list(state[0])
        listPallets = list(state[1])
        palletCargado = list(state[2])
        acc,obj = actions
        if acc == "Moverse":
            posRobot = posRobot[0] + obj[0],posRobot[1] + obj[1]
        elif acc == "Agarrar Pallet":
            palletCargado.append(obj)
            listPallets.remove(obj)
    
        elif acc == "Soltar Pallet":
            tipoCaja,posCargado = state[2]
            if tipoCaja == "A":
                palletCargado = ()
                state[4] = posCargado
            else:
                palletCargado = ()
                state[5] = posCargado



        return tuple(posRobot),tuple(listPallets),tuple(palletCargado),state[3]
    
    def is_goal(self, state):
        
        return state[2] == () and state[3] == ()
    
    def cost (self,state,action,state2):
        if action[0] == "Moverse":
            return 1
        elif action[0] == "Agarrar Pallet":
            return 3
        else:
            return 2  
    
    def heuristic(self, state):
        contador = 0
        contador += len(state[1]) * 3 + len(state[1]) * 2
        return contador

problem = problemaFinal(estadoinicial)  
result = astar(problem, graph_search=True,viewer=WebViewer())
