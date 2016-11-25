from pyplasm import*

DEPTH_PIANO = 0.02
MARRONCINO = Color4f([218/255.,179/255.,122/255.,1.0])

def ggpl_my_forniture(listaX,listaY,listaZ):
    
    listaCoordinate = [listaX,listaY,listaZ]
    
   
    '''associo per ogni oggetto nel dizionario un indice opportuno, per ogni nuovo oggetto basta aggiungerlo alla lista "stringheOggetti" e ricordarsi la posizione in cui viene inserito'''
    stringheOggetti = ["tavolo","sedia","armadio","cattedra","libreria"]
    oggetto2indice = associaOggetti(stringheOggetti)
    
    #costruisco gli oggetti
    tavolo = makeObject("tavolo",oggetto2indice,listaCoordinate)
    sedia = makeObject("sedia",oggetto2indice,listaCoordinate)
    armadio = makeObject("armadio",oggetto2indice,listaCoordinate)
    cattedra = makeObject("cattedra",oggetto2indice,listaCoordinate)
    libreria = makeObject("libreria",oggetto2indice,listaCoordinate)
    
    

    
    '''-----------------------------------------------------------------------------------------------'''

def associaOggetti(stringheOggetti):
    oggetto2indice = {}
    
    for i in range(len(stringheOggetti)):
        oggetto2indice[stringheOggetti[i]] = i
    
    return oggetto2indice
    
def getCoordinate(indice,listaCoordinate):
    coordinate = []
    
    for c in listaCoordinate:
        coordinate.append(c[indice])
    
    return coordinate

def getMethodoObject(stringa,coordinate):
    if stringa == "tavolo" or "table":
        return getTavolo(coordinate[0],coordinate[1],coordinate[2])
    elif stringa == "sedia" or "chair":
        return getSedia(coordinate[0],coordinate[1],coordinate[2])
    elif stringa == "armadio" or "closet":
        return getArmadio(coordinate[0],coordinate[1],coordinate[2])
    elif stringa == "cattedra" or "desk":
        return getCattedra(coordinate[0],coordinate[1],coordinate[2])
    elif stringa == "libreria" or "library":
        return getLibreria(coordinate[0],coordinate[1],coordinate[2])
    elif stringa == "sedia braccioli" or "sedia a braccioli" or "arm chair":
        return getSediaBraccioli(coordinate[0],coordinate[1],coordinate[2])
    elif stringa == "lavagna" or "blackboard":
        return getLavagna(coordinate[0],coordinate[1],coordinate[2])
    else:
        return None

def makeObject(stringa,indice2oggetti,listaCoordinate):
    
    indice = indice2oggetti[stringa.lower()]
    coordinate = getCoordinate(indice,listaCoordinate)
    oggetto = getMethodoObject(stringa.lower(),coordinate)
    return oggetto

'''qui sotto sono elencati i metodi di ogni oggetto, dove l sta per larghezza, p profondita e h altezza'''
def getTavolo(l,p,h):
    
    piano = COLOR(WHITE)(CUBOID([l,p,0.025]))
    pianoFerro = OFFSET([0.03,0.03,0.03])(SKEL_1(CUBOID([l-0.06,p-0.06,0])))
    gamba = CUBOID([0.03,0.03,h])

    gambaPianoFerro = COLOR(GRAY)(STRUCT([gamba,T(1)(l-0.06)(gamba),T(2)(p-0.06)(gamba),T([1,2])([l-0.06,p-0.06])(gamba),T(3)(h)(pianoFerro)]))

    tavolo = STRUCT([T([1,2])([0.015,0.015])(gambaPianoFerro),T(3)(h+0.03)(piano)])

    return tavolo

def getSedia(l,p,h,r):
    
    ''' PARTE SMUSSATA '''
    circle = R([1,2])(PI/2)(OFFSET([DEPTH_PIANO,0,0])(SPHERE(r)([50,2])))
    quadUP = CUBOID([l-(2*r),DEPTH_PIANO,r])
    blunt_side = T(1)(r)(STRUCT([circle,T(1)(l-(2*r))(circle),quadUP]))
    
    ''' SCHIENALE '''
    HEIGHT_SCHIENALE = h/3
    quad_schienale = CUBOID([l,DEPTH_PIANO,HEIGHT_SCHIENALE-r])
    schienale = STRUCT([quad_schienale,T(3)(HEIGHT_SCHIENALE-r)(blunt_side)])
    schienale = COLOR(MARRONCINO)(schienale)
    
    ''' SEDILE '''
    quad_sedile = CUBOID([l,p-r,DEPTH_PIANO])
    sedile = STRUCT([T(2)(r)(quad_sedile),T(2)(r)(R([2,3])(PI/2)(blunt_side))])
    sedile = COLOR(MARRONCINO)(sedile)
    
    ''' SKELETON '''
    HEIGHT_LEG = h/1.77
    HEIGHT_PILLAR = h/2.30
    leg = CUBOID([DEPTH_PIANO,DEPTH_PIANO,HEIGHT_LEG])
    pillar = CUBOID([DEPTH_PIANO,DEPTH_PIANO,HEIGHT_PILLAR])
    quad_skeleton = OFFSET([DEPTH_PIANO,DEPTH_PIANO,DEPTH_PIANO])(SKEL_1(CUBOID([l-DEPTH_PIANO,p-r,0])))
    quad_skeleton_legs = STRUCT([leg,T(1)(l-DEPTH_PIANO)(leg),T(2)(p-r)(leg),T([1,2])([l-DEPTH_PIANO,p-r])(leg),T(3)(HEIGHT_LEG)(quad_skeleton)])
    skeleton = STRUCT([quad_skeleton_legs,T([2,3])([p-r,HEIGHT_LEG+DEPTH_PIANO])(pillar),T([1,2,3])([l-DEPTH_PIANO,p-r,HEIGHT_LEG+DEPTH_PIANO])(pillar)])
    skeleton = COLOR(GRAY)(skeleton)
    
    ''' SEDIA '''
    sedia = STRUCT([T(2)(r)(skeleton),T([2,3])([DEPTH_PIANO,HEIGHT_LEG+DEPTH_PIANO])(sedile),T([2,3])([p-DEPTH_PIANO,h-r])(schienale)])
    
    return sedia

def getSediaBraccioli(l,p,h,r):
    WIDHT_BRACCIOLO = l/5
    DEPTH_BRACCIOLO = 0.9*p
    
    ''' BRACCIOLO '''
    circle = R([2,3])(PI/2)(R([1,2])(PI/2)(OFFSET([DEPTH_PIANO,0,0])(SPHERE(WIDHT_BRACCIOLO/2)([50,2]))))
    pillar = CUBOID([WIDHT_BRACCIOLO,DEPTH_BRACCIOLO-r,DEPTH_PIANO])
    bracciolo_wood = STRUCT([T([1,2])([WIDHT_BRACCIOLO/2,WIDHT_BRACCIOLO/2])(circle),T(2)(WIDHT_BRACCIOLO/2)(pillar)])
    bracciolo_wood = COLOR(MARRONCINO)(bracciolo_wood)
    bracciolo_pillar = COLOR(GRAY)(CUBOID([DEPTH_PIANO,DEPTH_BRACCIOLO-r,DEPTH_PIANO]))
    bracciolo = STRUCT([T(3)(DEPTH_PIANO/2)(bracciolo_wood),T([1,2])([(WIDHT_BRACCIOLO/2)-DEPTH_PIANO/2,WIDHT_BRACCIOLO/2])(bracciolo_pillar)])
    
    sedia = getSedia(l,p,h,r)
    sediaBraccioli = STRUCT([T(1)(WIDHT_BRACCIOLO/2-DEPTH_PIANO/2)(sedia),T([2,3])([p-DEPTH_BRACCIOLO+2*DEPTH_PIANO,0.77*h])(bracciolo),T([1,2,3])([l-DEPTH_PIANO,p-DEPTH_BRACCIOLO+2*DEPTH_PIANO,0.77*h])(bracciolo)])
    
    return sediaBraccioli
    
def getArmadio(l,p,h):
    shortRect = CUBOID([l,p,DEPTH_PIANO])
    longRect = CUBOID([DEPTH_PIANO,p,h])
    farestRect = CUBOID([l,DEPTH_PIANO,h+2*DEPTH_PIANO])
    
    ''' SCAFFALI '''
    dist = h/5.0
    piano = CUBOID([l-2*DEPTH_PIANO,p-DEPTH_PIANO,DEPTH_PIANO])
    piani = STRUCT([QUOTE([0])])
    
    for i in range(4):
        piani = STRUCT([piani,T(3)(dist)(piano)])
        dist += h/5.0

    ''' ANTA '''
    anta_board = CUBOID([(l/2)-DEPTH_PIANO,DEPTH_PIANO,h-DEPTH_PIANO])
    pomello = SPHERE(0.01*h)([50,50])
    anta = STRUCT([anta_board,T([1,2,3])([0.01*h,-0.007*h,h/3])(pomello)])
    
    ''' BOX '''
    box = STRUCT([shortRect,T(3)(h+DEPTH_PIANO)(shortRect),T(3)(DEPTH_PIANO)(longRect),T([1,3])([l-DEPTH_PIANO,DEPTH_PIANO])(longRect),T(2)(p)(farestRect)])
    
    armadio = STRUCT([box,T([1,2])([DEPTH_PIANO,DEPTH_PIANO])(piani),T(1)(DEPTH_PIANO)(anta)])
    
    return armadio
    
def getLibreria(l,p,h):
    return
    
def getLavagna(l,p,h):
    return

#VIEW(STRUCT([sfera,T(1)(-0.4)(sfera),T(1)(-0.5)(quad),T([1,2])([-0.4,-0.1])(quadUP)]))

'''def getArmadio(l,p,h):

def getCattedra(l,p,h):

def getLibreria(l,p,h):'''


#VIEW(getArmadio(1.74,0.44,2.1))