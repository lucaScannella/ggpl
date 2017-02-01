from math import*
from pyplasm import *

def ggpl_my_roof_builder(verts,cells):
    tetto = MKPOL([verts,cells,1])
    
    '''Components of the roof: the skeleton and the skin of the roof'''
    skeleton = COLOR(YELLOW)(skeletizer(tetto))
    skin = COLOR(RED)(skinner(tetto))
    
    '''build the roof'''
    roof = STRUCT([skeleton,T(3)(0.1)(skin)])
    
    return roof

def casa():
    verts = [[0,0,0],[3,0,0],[3,2,0],[0,2,0],[0,0,1.5],[3,0,1.5],[3,2,1.5],[0,2,1.5],[0,1,2.2],[3,1,2.2]]
    cells = [[1,2],[2,3],[3,4],[4,1],[5,6],[6,7],[7,8],[8,5],[1,5],[2,6],[3,7],[4,8],[5,9],[8,9],[6,10],[7,10],[9,10]]
    pols = [[1]]
    house = MKPOL([verts,cells,pols])
    house = OFFSET([0.1,0.2,0.1])(house)
    return STRUCT([SKEL_2(house),T(2)(3)(house)])
	
def skeletizer(obj):
    structure = SKEL_1(obj)
    structure = OFFSET([0.05,0.05,0.1])(structure)
    

    return structure

# ritorna il piano + alto [numero]
def pianoMax(verts):
    mass = -1000
    for v in verts:
       mass = max(mass,v[2])
    return mass
    
# ritorna true se due punti stanno sullo stesso lato [bool]
def stessoLato(v1,v2):
    return v1[0]==v2[0] or v1[1]==v2[1]

def pulisciDoppioni(verts):
    vertici = verts

    for i in verts[:len(verts)-1]:
        for j in verts[verts.index(i)+1:]:
            if i == j:
                vertici.remove(j)
    return verts
    
#costruisce la "pelle" del tetto, ossia il rivestimento esterno    
def skinner(obj):
    components = UKPOL(obj)

    verts = components[0]
    cells = components[1]
    
    #lista di facciate (ossia i punti che devo collegare tra loro per ogni facciata) [lista di liste]
    faces = makeFaces(verts,cells)
    skin = MKPOL([verts,faces,[1]])
    
    return OFFSET([0.05,0.05,0.05])(skin)

#ritorna una mappa di posizione-vertice che stanno sull'ultimo piano    
def lastFloorMap(verts,vertsConvessi):
    maxFloor = pianoMax(vertsConvessi)
    pos2vert = {}
    for i in range(len(vertsConvessi)):
        if vertsConvessi[i][2] == maxFloor:
            pos2vert[verts.index(vertsConvessi[i])+1] = vertsConvessi[i]
    return pos2vert

def mod(n):
    if n<0:
        n*=-1
    return n
    
def distanza2(v1,v2):
    cateto1 = mod(v1[0]-v2[0])
    cateto2 = mod(v1[1]-v2[1])
    distanza = sqrt(cateto1**2 + cateto2**2)
    return distanza

#passati due vertici calcola la loro distanza
def distanza3(v1,v2):
    cateto1 = mod(v1[2]-v2[2])
    v1iniziale = v1[2]
    v2iniziale = v2[2]
    
    #proietto i vertici sul piano d'origine dove Z=0
    v1[2] = 0
    v2[2] = 0
    
    cateto2 = distanza2(v1,v2)
    distanza = sqrt(cateto1**2 + cateto2**2)
    
    v1[2] = v1iniziale
    v2[2] = v2iniziale
    
    return distanza

#resistuisce la posizione del vertice piu vicino a v1, vert2position: mappa vertice-posizione
def nearestVert(v1,pos2vert):
    distanza = 100000
    for pos,v in pos2vert.items():
        distanza2 = min(distanza,distanza3(v1,v))
        if distanza > distanza2:
            posMin = pos
            distanza = distanza2
    return posMin
    
def adiacenti(v1,verts,vertsConvessi):
    adiacents = []
    lastVerts = lastFloorMap(verts,vertsConvessi)
    
    for v in vertsConvessi:
        if  stessoLato(v,v1) and v != v1 and v not in lastVerts.values():
            adiacents.append(v)

    return adiacents

def occorrenzaConvessi(adiacente,verts,cells):
    cont = 0

    for cell in cells:
        for c in cell:
            if adiacente == verts[c-1]:
                cont += 1
    return cont

def BFS(vertsConvessi,verts,lastVerts,facciate):
    color = []
    for i in range(len(vertsConvessi)):
        color.append(0)
    
    coda = [vertsConvessi[0]]
    cells = []
    while coda:
        # operazione di dequeue
        vertice = coda.pop(0)
        if color[vertsConvessi.index(vertice)] == 0:
            adiacents = adiacenti(vertice,verts,vertsConvessi)
            for adiacente in adiacents:
                cell = []
                if color[vertsConvessi.index(adiacente)] == 0:
                    cell.append(verts.index(vertice)+1)
                    supVert = nearestVert(vertice,lastVerts)
                    cell.append(supVert)
                    cell.append(verts.index(adiacente)+1)
                    for posLastV,lastV in lastVerts.items():
                        if posLastV != supVert:
                            if vertice[0] == adiacente[0]:
                                if (lastV[1] > vertice[1] and lastV[1] > adiacente[1]) or (lastV[1] < vertice[1] and lastV[1] < adiacente[1]):
                                    cell.append(posLastV)
                            elif vertice[1] == adiacente[1]:
                                if (lastV[0] > vertice[0] and lastV[0] > adiacente[0]) or (lastV[0] < vertice[0] and lastV[0] < adiacente[0]):
                                    cell.append(posLastV)
                    if occorrenzaConvessi(adiacente,verts,facciate) <= 1:
                        coda.append(adiacente)
                if cell != [] and (occorrenzaConvessi(vertice,verts,facciate)<=1 or occorrenzaConvessi(adiacente,verts,facciate)<=1):
                    cells.append(cell)
            color[vertsConvessi.index(vertice)] = 1
    return cells

def selectVerts(verts,cell):
    vertsConvessi = []
    
    for c in cell:
        vertsConvessi.append(verts[c-1])
        
    return vertsConvessi

def makeFaces(verts,cells):
    faces = []
    for cell in cells:
        vertsConvessi = selectVerts(verts,cell)
        facesConvesse = BFS(vertsConvessi,verts,lastFloorMap(verts,vertsConvessi),cells)
        faces.extend(facesConvesse)
    
    return faces