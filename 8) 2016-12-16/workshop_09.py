from pyplasm import *
import csv
import math

ANGOLO = PI/3
COSTANTE_DI_TAGLIO = 0.6
TERRACE_TEXTURE = ["terrace_texture.jpg",True,False,1,1,0,10,10]

def tetto_terrazzo(angolo,perimetro):
    perimetro = UKPOL(perimetro)
    vertici = perimetro[0]
    celle = perimetro[1]
    vertici = cleanVerts(vertici)
    roof = make_roof(vertici,celle,angolo,COSTANTE_DI_TAGLIO,1)
    
    return roof
    
def getVertsInCell(verts,cell):
    vertici = []
    for c in cell:
        vertici.append(verts[c-1])
    return vertici

def getListeCoordinate(vertici):
    listaX = []
    listaY = []
    
    for v in vertici:
        listaX.append(v[0])
        listaY.append(v[1])

    return [listaX,listaY]
    
def getVertsSuperiori(vertici,angolo,cost,celle,allVertici):
    verticiSuperiori = []
    tan = math.sin(angolo)/math.cos(angolo)
    listaX = getListeCoordinate(vertici)[0]
    listaY = getListeCoordinate(vertici)[1]
    baricentro = centroid(listaX,listaY)

    for v in vertici:
        vSup = []
        #riempio la x
        valore = math.fabs(baricentro[0]-v[0])*cost
        if baricentro[0]-v[0] >= 0:
            vSup.append(v[0]+valore)
        else:
            vSup.append(v[0]-valore)
    
        #riempio la y
        valore = math.fabs(baricentro[1]-v[1])*cost
        if baricentro[1]-v[1] >= 0:
            vSup.append(v[1]+valore)
        else:
            vSup.append(v[1]-valore)
        
        #riempio la z
        vSup.append(tan*cost)
        verticiSuperiori.append(vSup)

    for v in vertici:
        if getNumCelle(v,allVertici,celle) > 1:
            verticiStessaCella = getVertSameCell(v,vertici,celle,allVertici)
            for vsc in verticiStessaCella:
                retta1 = [v,vsc]
                print "Retta 1:",retta1
                vSuperiore = verticiSuperiori[vertici.index(v)]
                if vertici.index(v) < vertici.index(vsc):
                    print "v sta PRIMA di vsc"
                    vPrev = getVerticeAdiacente(v,vsc,vertici,0)
                    print "vertice precedente:",vPrev
                    vPrevSup = verticiSuperiori[vertici.index(vPrev)]
                    retta2 = [vSuperiore,vPrevSup]
                    print "Retta 2:",retta2
                else:
                    print "v sta DOPO di vsc"
                    vNext = getVerticeAdiacente(v,vsc,vertici,1)
                    print "vertice successivo:",vNext
                    vNextSup = verticiSuperiori[vertici.index(vNext)]
                    retta2 = [vSuperiore,vNextSup]
                    print "Retta 2:",retta2

                verticiSuperiori[vertici.index(v)] = intersezione(retta1,retta2)
                print "intersezione:",verticiSuperiori[vertici.index(v)],"\n"
                
                verticiSuperiori[vertici.index(v)][2] = tan*cost

    return verticiSuperiori  

def cleanVerts(vertici):
    verticiN = []
    for v in vertici:
        vert = []
        check  = False
        if v[1] - int(v[1]) > 0:
            vn = [math.ceil(v[0]),math.ceil(v[1]),math.ceil(v[2])]
            print vn
            for v2 in vertici:
                if v2 == vn:
                    check = True
                    print check
                    break
        if check:
            verticiN.append(vn)
        else:
            verticiN.append(v)
    return verticiN

def getVerticeAdiacente(v,vsc,vertici,adiacente):
    if adiacente == 0:                          #vertice precedente
        if vertici.index(v) == 0:
            if vertici[len(vertici)-1] == vsc:
                return vertici[vertici.index(v)+1]
            else:
                return vertici[len(vertici)-1]
        else:
            return vertici[vertici.index(v)-1]
    elif adiacente == 1:                        #vertice successivo
        if vertici.index(v) == len(vertici)-1:
            if vertici[0] == vsc:
                return vertici[vertici.index(v)-1]
            else:
                return vertici[0]
        else:
            return vertici[vertici.index(v)+1]
    else:
        return None

def getVertSameCell(v,vertici,celle,allVertici):
    listaVertici = []
    for vert in vertici:
        if vert != v:
            if sameCells(v,vert,allVertici,celle):
                listaVertici.append(vert)
    return listaVertici

def make_roof(vertici,celle,angolo,cost,showTerrace):
    facciate = QUOTE([0])
    terrace = QUOTE([0])
    for c in celle:
        verts = getVertsInCell(vertici,c)
        vertsSuperiori = getVertsSuperiori(verts,angolo,cost,celle,vertici)
        terrace = STRUCT([terrace,make_terrace(vertsSuperiori,celle.index(c))])
        facciate = STRUCT([facciate,make_facciate(verts,vertsSuperiori,vertici,celle)])
    
    terrace = TEXTURE(TERRACE_TEXTURE)(terrace)
    
    if showTerrace == 1:
        roof = STRUCT([terrace,facciate])
    else:
        roof = facciate
    
    return roof
    
def make_facciate(verts,vertsSuperiori,vertici,celle):

    if sameCells(verts[0],verts[len(verts)-1],vertici,celle) == False:
        facciate = MKPOL([[verts[0],verts[len(verts)-1],vertsSuperiori[0],vertsSuperiori[len(verts)-1]],[[1,2,3,4]],1])
        facciate = TEXTURE(["roof_texture.jpg",True,False,1,1,coefficienteAngolare(verts[0],verts[len(verts)-1]),distanza(verts[0],verts[len(verts)-1]),distanza(vertsSuperiori[0],verts[0])])(facciate)
    else:
        facciate = QUOTE([0])
   
    for i in range(len(verts)-1):
        if sameCells(verts[i],verts[i+1],vertici,celle) == False:
            facciata = MKPOL([[verts[i],vertsSuperiori[i],vertsSuperiori[i+1],verts[i+1]],[[1,2,3,4]],1])
            facciata = TEXTURE(["roof_texture.jpg",True,False,1,1,coefficienteAngolare(verts[i],verts[i+1]),distanza(verts[i],verts[i+1]),distanza(vertsSuperiori[i],verts[i])])(facciata)
            facciate = STRUCT([facciate,facciata])

    return facciate

def coefficienteAngolare(v1,v2):
    if v2[0] != v1[0]:
        return (v2[1] - v1[1])/(v2[0] - v1[0])
    else:
        return 0
    
def make_terrace(verts,n):
    terrace = MKPOL([verts,[[i+1 for i in  range(len(verts))]],1])
    
    if n%2 != 0:
        terrace = S([1,2,3])([-1,-1,-1])(terrace)
        terrace = R([2,1])(PI)(terrace)
        terrace = T(3)(verts[0][2]*2)(terrace)
    
    return terrace

def getCelle(v,vertici,celle):
    listaCelle = []
    
    for c in celle:
        for i in c:
            if vertici[i-1]==v:
                listaCelle.append(celle.index(c)+1)
                break

    return listaCelle
    
def getNumCelle(v,vertici,celle):
    numCelle = 0
    for c in celle:
        for i in c:
            if vertici[i-1]==v:
                numCelle += 1
                break

    return numCelle

def sameCells(v1,v2,vertici,celle):
    listaV1 = getCelle(v1,vertici,celle)
    listaV2 = getCelle(v2,vertici,celle)
    
    c=0
    
    for i in listaV1:
        for j in listaV2:
            if i==j:
                c+=1

    if c > 1:
        return True
    else:
        return False
    
def distanza(v1,v2):

    return math.sqrt(math.fabs(v1[0]-v2[0])**2+math.fabs(v1[1]-v2[1])**2)
    
def centroid(listaX,listaY):
    sumX = sum(listaX)
    sumY = sum(listaY)
    
    return [sumX/len(listaX),sumY/len(listaY),0]
    
def nextVert(v,vertici):
    minimo = 10000000
    
    if len(vertici) == 1:
        return v
    else:
        for vert in vertici:
            if vert != v:
                if minimo > distanza(v,vert):
                    minimo = distanza(v,vert)
                    nextVert = vert
        return nextVert

def intersezione(retta1,retta2):
    #coordinate retta 1
    x1_r1 = float(retta1[0][0])
    y1_r1 = float(retta1[0][1])
    x2_r1 = float(retta1[1][0])
    y2_r1 = float(retta1[1][1])
    
    #coordinate retta 2
    x1_r2 = float(retta2[0][0])
    y1_r2 = float(retta2[0][1])
    x2_r2 = float(retta2[1][0])
    y2_r2 = float(retta2[1][1])
    
    #caso in cui le rette sono due asintoti verticali e quindi parallele
    if x2_r1 == x1_r1 and x2_r2 == x1_r2:
        print "asintoti verticali"
        return None
    
    #caso in cui una retta e' un asintoto verticale e l'altra un asintoto orizzontale 
    if x2_r1 == x1_r1 and y1_r2 == y2_r2:
        return [x1_r1,y1_r2,0]
    if x2_r2 == x1_r2 and y1_r1 == y2_r1:
        return [x1_r2,y1_r1,0]
    
    #coefficienti angolari
    if x2_r1 != x1_r1:
        m1 = (y2_r1 - y1_r1)/(x2_r1 - x1_r1)
    else:
        m1 = float(10**10)
    if x2_r2 != x1_r2:
        m2 = (y2_r2 - y1_r2)/(x2_r2 - x1_r2)
    else:
        m2 = float(10**10)
 
    #termini noti
    q1 = -m1*x1_r1 + y1_r1
    q2 = -m2*x1_r2 + y1_r2
    
    #caso in cui una delle rette e' un asintoto verticale
    if x2_r1 == x1_r1:
        return [x1_r1,m2*x1_r1+q2,0]
    if x2_r2 == x1_r2:
        return [x1_r2,m1*x1_r2+q1,0]

    #caso in cui una delle due rette e' un asintoto orizzontale
    if y2_r1 == y1_r1:
        return [(y1_r1-q2)/m2,y1_r1,0]
    if y2_r2 == y1_r2:
        return [(y1_r2-q1)/m1,y1_r2,0]

    if m1 != m2:
        y = (m1*q2 - m2*q1)/(m1 - m2)
        return [(y-q2)/m2,y,0]
    else:
        print "rette parallele"
        return None #caso in cui le rette sono parallele o asintoti orizzontali
    
perimetro1 = MKPOL([[[0,0,0],[4,0,0],[4,2,0],[2,2,0],[2,4,0],[0,4,0]],[[1,2,3,4],[1,4,5,6]],1])
tetto1 = tetto_terrazzo(ANGOLO,perimetro1)

perimetro2 = MKPOL([[[0,0,0],[2,0,0],[4,4,0],[3,6,0],[0,4,0],[6,6,0],[6,4,0]],[[1,2,3,4,5],[3,4,6,7]],1])
tetto2 = tetto_terrazzo(ANGOLO,perimetro2)

perimetro3 = MKPOL([[[2,0,0],[4,2,0],[4,8.5,0],[0,5,0],[0,2,0],[6,0,0],[8,2,0],[8,5,0]],[[1,2,3,4,5],[2,3,6,7,8]],1])
tetto3 = tetto_terrazzo(ANGOLO,perimetro3)

retta1 = [[1,2,0],[5,2,0]]
retta2 = [[1,1,0],[4,2,0]]
r1 = MKPOL([retta1,[[1,2]],1])
r2 = MKPOL([retta2,[[1,2]],1])
i = intersezione(retta1,retta2)
inter = MKPOL([[i,[i[0],i[1]+1,0]],[[1,2]],1])
n = STRUCT([r1,r2,inter])


VIEW(tetto2)
