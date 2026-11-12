from itertools import combinations
from simpleai.search import CspProblem,backtrack,min_conflicts

def build_camp(camp_size,habs,generators,labs,deposits,airlocks,craters):

    row,col = camp_size  #Desgloso el mapa fila, columna
    varHabs = []
    varGen = []
    varLab = []
    varDep = []
    varAir = []
    dominioCompleto =[]
    dominoExclusa = []
    dominioInterior = []
    #Diccionario de dominios
    dominios ={}
    #Restricciones
    constrains = []   
    for hab in range(habs):
        varHabs.append("Hab: "+ str(hab))
    for gen in range(generators):
        varGen.append("Gen: "+ str(gen))   
    for lab in range(labs):
        varLab.append("Lab: "+ str(lab))
    for dep in range(deposits):
        varDep.append("Dep: "+ str(dep))
    for air in range(airlocks):
        varAir.append("Air: "+ str(air)) ##Tiene que estar en el borde  



    for r in range(row):
        for c in range(col):
                if (r == 0 or r == row-1 or c == 0 or c== col -1 )and (r,c) not in craters:  ##Si está en la fila/col primera o ultima y no haya crateres
                    dominoExclusa.append((r,c)) 
#Dominio interior y completo
    for r in range(row):
        for c in range(col):
            if (r,c) not in craters:
                    dominioCompleto.append((r,c))  #Completo las posibles disponibles 
                    if (r,c) not in dominoExclusa:
                        dominioInterior.append((r,c))


    for hab in varHabs:
        dominios[hab] = dominioInterior
    for gen in varGen:
        dominios[gen] = dominioCompleto
    for lab in varLab:
        dominios[lab] = dominioCompleto
    for dep in varDep:
        dominios[dep] = dominioCompleto
    for air in varAir:
        dominios[air] = dominoExclusa

    variables = varHabs + varGen + varLab + varDep +  varAir


    def modulos_Distintos(variables,values):
        return values[0] != values[1]
    
    for var1,var2 in combinations(variables,2):
         constrains.append(((var1,var2),modulos_Distintos))

    def gen_no_adj_hab(variables,values):
        row1,col1 = values[0]
        row2,col2 = values[1]
        return abs(row1-row2) + abs( col1-col2) > 1
    
    for gen1,gen2 in combinations(varGen,2):
         constrains.append(((gen1,gen2),gen_no_adj_hab))

    def lab_adj_dep(variables,values):
        row1,col1 = values[0]
        row2,col2 = values[1]
        return abs(row1-row2) + abs( col1-col2) == 1
    
    for lab1,lab2 in combinations(varLab,2):
         constrains.append(((lab1,lab2),lab_adj_dep))

    def salida_hab(variable,values):
        row,col = values[0]
        valoresPosibles = set(values[1:])
        adyacentes = (row +1 ,col),(row-1 ,col),(row ,col + 1),(row ,col - 1)
        contador = 0
        for valor in valoresPosibles:
             if valor not in adyacentes:
                 contador += 1
        return contador > 1
    
    for hab in varHabs:
        constrains.append(((hab),salida_hab))

    print("Restricciones", len(constrains))
    print("Variables:", variables)
    problem = CspProblem(variables,dominios,constrains)
    solution = backtrack (problem, variable_heuristic='MOST_CONSTRAINED_VARIABLE', value_heuristic='LEAST_CONSTRAINING_VALUE')

    resultado = []
    if not solution:
         return []
    
    for hab in varHabs:
        row,col=solution[hab]
        resultado.append((hab, row, col))

    for lab in varLab:
        row,col=solution[lab]
        resultado.append((lab, row, col))

    for gen in varGen:
        row,col=solution[gen]
        resultado.append((gen, row, col))

    for dep in varDep:
        row,col=solution[dep]
        resultado.append((dep, row, col))

    for air in varAir:
        row,col=solution[air]
        resultado.append((air, row, col))

    return resultado

resultado = build_camp(
camp_size= (5,6),
habs=3,
generators=2,
labs=2,
deposits=2,
airlocks=3,
craters=[(2, 2), (2, 3),(4,4)]
)
