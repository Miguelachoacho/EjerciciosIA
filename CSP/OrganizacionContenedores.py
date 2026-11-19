from itertools import combinations
from simpleai.search import CspProblem, backtrack, min_conflicts

N = 6
celdas = [(r, c) for r in range(N) for c in range(N)]

muelles = ["muelle " + str(i) for i in range(6)]
gruas = ["grua " + str(i) for i in range(10)]
zonas = ["zona " + str(i) for i in range(15)]
variables_problema = muelles + gruas + zonas + ["admin", "estacionamiento"]

domains = {}
for variable in muelles:
    domains[variable] = [(r, c) for r, c in celdas if r == 0 or c == 0]   # borde norte u oeste
for variable in gruas:
    domains[variable] = list(celdas)
for variable in zonas:
    domains[variable] = [(r, c) for r, c in celdas if 0 < r < N-1 and 0 < c < N-1]  # no en bordes
domains["admin"] = list(celdas)
domains["estacionamiento"] = [(N-1, c) for c in range(N)]                 # borde sur

constraints = []

def adyacentes(a, b):
    return a != b and abs(a[0]-b[0]) <= 1 and abs(a[1]-b[1]) <= 1

def different(variable, values):     # llegan 2 posiciones y deben ser distintas
    pos1, pos2 = values
    return pos1 != pos2

for variable1, variable2 in combinations(variables_problema, 2):
    constraints.append(((variable1, variable2), different))

def muelleConGrua(variable, values):   # values[0] es el muelle, el resto son las grúas
    muelle = values[0]
    return any(adyacentes(muelle, grua) for grua in values[1:])

for muelle in muelles:
    constraints.append(((muelle,) + tuple(gruas), muelleConGrua))

def gruaConMuelle(variable, values):   # values[0] es la grúa, el resto son los muelles
    grua = values[0]
    return any(adyacentes(grua, muelle) for muelle in values[1:])

for grua in gruas:
    constraints.append(((grua,) + tuple(muelles), gruaConMuelle))

def adminLejosDeGrua(variable, values):
    admin, grua = values
    return not adyacentes(admin, grua)

for grua in gruas:
    constraints.append((("admin", grua), adminLejosDeGrua))

problem = CspProblem(variables_problema, domains, constraints)
solution = backtrack(problem, variable_heuristic='MOST_CONSTRAINED_VARIABLE', value_heuristic='LEAST_CONSTRAINING_VALUE')
print("Solution: ")
print(solution)