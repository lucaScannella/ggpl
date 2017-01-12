from pyplasm import*

DEPTH_PIANO = 0.02
MARRONCINO = Color4f([218/255.,179/255.,122/255.,1.0])
DARKWOOD_ARMADIO = Color4f([128/255.,67/255.,50/255.,1.0])
LIGHTWOOD_ARMADIO = Color4f([203/255.,164/255.,106/255.,1.0])
LIBRERIA =  Color4f([117/255.,119/255.,143/255.,1.0])
SCAFFALI_LIBRERIA = Color4f([170/255.,170/255.,186/255.,1.0])
BLACKBOARD = Color4f([20/255.,30/255.,11/255.,1.0])
GREEN_TABLE = Color4f([158/255.,182/255.,72/255.,1.0])

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
def getCattedra(l,p,h):
    HEIGHT_PIANO_LATERALE = h*0.6
    
    downSide_piano = COLOR(MARRONCINO)(MKPOL([[[0,0,0],[l+DEPTH_PIANO*2,0,0],[0,p+DEPTH_PIANO*2,0],[l+DEPTH_PIANO*2,p+DEPTH_PIANO*2,0]],[[1,2,3,4]],1]))
    upSide_piano = COLOR(WHITE)(MKPOL([[[0,0,DEPTH_PIANO],[l+DEPTH_PIANO*2,0,DEPTH_PIANO],[0,p+DEPTH_PIANO*2,DEPTH_PIANO],[l+DEPTH_PIANO*2,p+DEPTH_PIANO*2,DEPTH_PIANO]],[[1,2,3,4]],1]))
    rightSide_piano = COLOR(MARRONCINO)(MKPOL([[[l+DEPTH_PIANO*2,0,0],[l+DEPTH_PIANO*2,0,DEPTH_PIANO],[l+DEPTH_PIANO*2,p+DEPTH_PIANO*2,0],[l+DEPTH_PIANO*2,p+DEPTH_PIANO*2,DEPTH_PIANO]],[[1,2,3,4]],1]))
    leftSide_piano = COLOR(MARRONCINO)(MKPOL([[[0,0,0],[0,0,DEPTH_PIANO],[0,p+DEPTH_PIANO*2,0],[0,p+DEPTH_PIANO*2,DEPTH_PIANO]],[[1,2,3,4]],1]))
    nearSide_piano = COLOR(MARRONCINO)(MKPOL([[[0,0,0],[0,0,DEPTH_PIANO],[l+DEPTH_PIANO*2,0,0],[l+DEPTH_PIANO*2,0,DEPTH_PIANO]],[[1,2,3,4]],1]))
    farSide_piano = COLOR(MARRONCINO)(MKPOL([[[0,p+DEPTH_PIANO*2,0],[0,p+DEPTH_PIANO*2,DEPTH_PIANO],[l+DEPTH_PIANO*2,p+DEPTH_PIANO*2,0],[l+DEPTH_PIANO*2,p+DEPTH_PIANO*2,DEPTH_PIANO]],[[1,2,3,4]],1]))
    piano = STRUCT([upSide_piano,downSide_piano,rightSide_piano,leftSide_piano,nearSide_piano,farSide_piano])
    
    pianoFerro = OFFSET([DEPTH_PIANO*2,DEPTH_PIANO*2,DEPTH_PIANO*1.5])(SKEL_1(CUBOID([l-DEPTH_PIANO,p-DEPTH_PIANO,0])))
    sezione_gamba = SPHERE(DEPTH_PIANO)([20,2])

    gamba = OFFSET([h,0,0])(sezione_gamba)
    gamba = R([1,3])(PI/2)(gamba)
    
    gambaPianoFerro = COLOR(GRAY)(STRUCT([T([1,2])([DEPTH_PIANO,DEPTH_PIANO])(gamba),T([1,2])([l,DEPTH_PIANO])(gamba),T([1,2])([DEPTH_PIANO,p])(gamba),T([1,2])([l,p])(gamba),T(3)(h)(pianoFerro)]))

    tavolo = STRUCT([T([1,2])([DEPTH_PIANO/2,DEPTH_PIANO/2])(gambaPianoFerro),T(3)(h+0.03)(piano)])
    
    
    piano_laterale = COLOR(MARRONCINO)(CUBOID([DEPTH_PIANO,p,HEIGHT_PIANO_LATERALE]))
    piano_far = COLOR(MARRONCINO)(CUBOID([l+DEPTH_PIANO,DEPTH_PIANO,HEIGHT_PIANO_LATERALE]))
    
    piano_cassetto = R([3,1])(PI/2)(piano_laterale)
    box_cassetti = STRUCT([piano_laterale,T([1,3])([DEPTH_PIANO,DEPTH_PIANO])(piano_cassetto),T([1,3])([DEPTH_PIANO,HEIGHT_PIANO_LATERALE/2])(piano_cassetto),T([1,3])([DEPTH_PIANO,HEIGHT_PIANO_LATERALE-DEPTH_PIANO])(piano_cassetto)])
    
    cassetto = COLOR(MARRONCINO)(CUBOID([HEIGHT_PIANO_LATERALE,DEPTH_PIANO,(HEIGHT_PIANO_LATERALE/2)-DEPTH_PIANO*2]))
    
    cilindro_pomello1 = SPHERE(DEPTH_PIANO)([20,2])
    cilindro_pomello1 = COLOR(DARKWOOD_ARMADIO)(OFFSET([DEPTH_PIANO/2,0,0])(cilindro_pomello1))
    cilindro_pomello2 = SPHERE(DEPTH_PIANO/2)([20,2])
    cilindro_pomello2 = COLOR(DARKWOOD_ARMADIO)(OFFSET([DEPTH_PIANO,0,0])(cilindro_pomello2))
    pomello = STRUCT([cilindro_pomello2,T(1)(DEPTH_PIANO/2)(cilindro_pomello1)])
    pomello = R([1,2])(PI/2)(pomello)
    
    cassetto = STRUCT([cassetto,T([1,2,3])([(HEIGHT_PIANO_LATERALE-DEPTH_PIANO)/2,DEPTH_PIANO,((HEIGHT_PIANO_LATERALE/2)-DEPTH_PIANO)/2])(pomello)])
    cassetto = COLOR(LIGHTWOOD_ARMADIO)(T([1,2])([HEIGHT_PIANO_LATERALE,DEPTH_PIANO])(R([1,2])(PI)(cassetto)))
    
    cassetti = STRUCT([box_cassetti,T([1,3])([DEPTH_PIANO,DEPTH_PIANO])(cassetto),T([1,3])([DEPTH_PIANO,(HEIGHT_PIANO_LATERALE/2)])(cassetto)])
    
    tavolo = STRUCT([T([1,2,3])([DEPTH_PIANO*2.5,DEPTH_PIANO*1.5,h/4])(piano_laterale),tavolo,T([1,2,3])([l-DEPTH_PIANO*1.5,DEPTH_PIANO*1.5,h/4])(piano_laterale),T([2,3])([p+DEPTH_PIANO*1.5,h/4])(piano_far),T([1,2,3])([l-HEIGHT_PIANO_LATERALE-DEPTH_PIANO*2.5,DEPTH_PIANO*1.5,h/4])(cassetti)])

    return tavolo

def getSedia(l,p,h):
    HEIGHT_SCHIENALE = h/3
    HEIGHT_LEG = h/1.77
    HEIGHT_PILLAR = h/2.30
    
    sedilePieno = SPHERE(DEPTH_PIANO)([10,10])
    sedilePieno = OFFSET([0,p,l])(sedilePieno)
    c = CUBOID([p/10,1.5*p,1.5*l])
    
    sedile = INTERSECTION([c,T([1,2,3])([p/10,DEPTH_PIANO,DEPTH_PIANO])(sedilePieno)])
    sedile = R([3,1])(PI/2)(sedile)
    sedile = COLOR(MARRONCINO)(T(3)(DEPTH_PIANO*3)(sedile))
    
    
    ''' SKELETON '''
    tube = SPHERE(DEPTH_PIANO/2)([20,20])
    
    sedile_tube_l = OFFSET([l,0,0])(tube)
    sedile_tube_p = OFFSET([p,0,0])(tube)
    sedile_tube_p = R([1,2])(PI/2)(sedile_tube_p)
    
    sedile_skel = STRUCT([sedile_tube_p,sedile_tube_l,T(1)(l)(sedile_tube_p),T(2)(p)(sedile_tube_l)])
    
    leg_tube = SPHERE(DEPTH_PIANO/2)([20,2])
    leg = OFFSET([HEIGHT_LEG,0,0])(leg_tube)
    leg = R([1,3])(PI/2)(leg)
    legs = STRUCT([leg,T(1)(l)(leg),T(2)(p)(leg),T([1,2])([l,p])(leg)])
    
    sedile_legs = STRUCT([legs,T(3)(HEIGHT_LEG)(sedile_skel)])
    
    pillar = OFFSET([HEIGHT_PILLAR,0,0])(tube)
    pillar = R([1,3])(PI/2)(pillar)
    
    skeleton = COLOR(GRAY)(STRUCT([sedile_legs,T(3)(HEIGHT_LEG+(1.5*DEPTH_PIANO))(pillar),T([1,3])([l,HEIGHT_LEG+(1.5*DEPTH_PIANO)])(pillar)]))
    
    ''' SCHIENALE '''
    schienale = SPHERE(DEPTH_PIANO/3)([20,20])
    schienale = OFFSET([0,l+DEPTH_PIANO,HEIGHT_SCHIENALE])(schienale)
    schienale = COLOR(MARRONCINO)(schienale)
    schienale = T([2,3])([0.77*DEPTH_PIANO,h-(HEIGHT_SCHIENALE/3)])(R([2,1])(PI/2)(schienale))
    
    sedia_schienale = STRUCT([T(1)(DEPTH_PIANO/2)(skeleton),schienale])
    sedia_schienale = STRUCT([T(2)(DEPTH_PIANO/2)(sedia_schienale)])
    
    sedia = STRUCT([T([1,2])([DEPTH_PIANO/2,DEPTH_PIANO/2])(sedia_schienale),T(3)(HEIGHT_LEG+DEPTH_PIANO/3)(sedile)])
    
    return sedia

def getSediaBraccioli(l,p,h):
    WIDHT_BRACCIOLO = l/5
    DEPTH_BRACCIOLO = 0.9*p
    
    ''' BRACCIOLO '''
    sezione_bracciolo = SPHERE(WIDHT_BRACCIOLO/4)([20,0])
    bracciolo = OFFSET([DEPTH_BRACCIOLO,WIDHT_BRACCIOLO/4,0])(sezione_bracciolo)
    
    sedia = getSedia(l,p,h)
    sediaBraccioli = STRUCT([T(1)(WIDHT_BRACCIOLO/2-DEPTH_PIANO/2)(sedia),T([2,3])([p-DEPTH_BRACCIOLO+2*DEPTH_PIANO,0.77*h])(bracciolo),T([1,2,3])([l-DEPTH_PIANO,p-DEPTH_BRACCIOLO+2*DEPTH_PIANO,0.77*h])(bracciolo)])
    
    return bracciolo
    
def getArmadio(l,p,h):
    WIDTH_ANTA = (l/2)-DEPTH_PIANO
    
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
    
    piani = COLOR(DARKWOOD_ARMADIO)(piani)
    
    ''' ANTA '''
    anta_board = CUBOID([WIDTH_ANTA,DEPTH_PIANO,h])
    pomello = SPHERE(0.01*h)([50,50])
    pomello = COLOR(DARKWOOD_ARMADIO)(pomello)
    anta_dx = COLOR(LIGHTWOOD_ARMADIO)(STRUCT([anta_board,T([1,2,3])([0.1*WIDTH_ANTA,-0.007*h,0.4*h])(pomello)]))
    anta_sx = COLOR(LIGHTWOOD_ARMADIO)(STRUCT([anta_board,T([1,2,3])([0.9*WIDTH_ANTA,-0.007*h,0.4*h])(pomello)]))
    
    
    ''' BOX '''
    box = STRUCT([shortRect,T(3)(h+DEPTH_PIANO)(shortRect),T(3)(DEPTH_PIANO)(longRect),T([1,3])([l-DEPTH_PIANO,DEPTH_PIANO])(longRect),T(2)(p)(farestRect)])
    
    box = COLOR(LIGHTWOOD_ARMADIO)(box)
    
    armadio_senza_ante = STRUCT([box,T([1,2])([DEPTH_PIANO,DEPTH_PIANO])(piani)])
    anta_sx = T([1,3])([DEPTH_PIANO,DEPTH_PIANO])(anta_sx)
    anta_dx = R([1,2])(PI/4)(anta_dx)
    armadio = STRUCT([armadio_senza_ante,anta_sx,T([1,2,3])([1.35*WIDTH_ANTA,DEPTH_PIANO-p,DEPTH_PIANO])(anta_dx)])
    
    return armadio
    
def getLibreria(l,p,h):
    
    rectOrizzontale = CUBOID([l,p,DEPTH_PIANO])
    rectVerticale = CUBOID([DEPTH_PIANO,p,h])
    farestRect = CUBOID([l,DEPTH_PIANO,h+2*DEPTH_PIANO])
    
    ''' SCAFFALI '''
    numero_scaffali = 4
    dist = h/(numero_scaffali+1.0)
    divisore = CUBOID([DEPTH_PIANO,p,dist])
    piano = CUBOID([l-2*DEPTH_PIANO,p-DEPTH_PIANO,DEPTH_PIANO])
    piano = STRUCT([piano,T([1,3])([0.6*l,DEPTH_PIANO])(divisore)])
    piani = STRUCT([T([1,3])([0.6*l,DEPTH_PIANO])(divisore)])
    
    for i in range(numero_scaffali):
        piani = STRUCT([piani,T(3)(dist)(piano),])
        dist += h/(numero_scaffali+1.0)
    
    piani = COLOR(SCAFFALI_LIBRERIA)(piani)
    
    
    ''' BOX '''
    box = STRUCT([rectOrizzontale,T(3)(h+DEPTH_PIANO)(rectOrizzontale),T(3)(DEPTH_PIANO)(rectVerticale),T([1,3])([l-DEPTH_PIANO,DEPTH_PIANO])(rectVerticale),T(2)(p)(farestRect)])
    box = COLOR(LIBRERIA)(box)
    
    libreria = STRUCT([box,T([1,2])([DEPTH_PIANO,DEPTH_PIANO])(piani)])
    
    

    return libreria
    
def getLavagna(l,p,h):
    rectVerticale = CUBOID([p/2,p,h-(p/2)])
    rectOrizzontale = CUBOID([l-(p/2),p,p/2])
    rectFarest = CUBOID([l,p/3,h])
    rectBoard = COLOR(BLACKBOARD)(CUBOID([l-(p/2),p/3,h-p]))
    
    cornice = STRUCT([rectVerticale,T([1,3])([l-(p/2),p/2])(rectVerticale),T(1)(p/2)(rectOrizzontale),T(3)(h-(p/2))(rectOrizzontale)])
    box = COLOR(MARRONCINO)(STRUCT([T(2)(p)(rectFarest),cornice]))
    
    lavagna = STRUCT([box,T([1,2,3])([p/2,p/3,p/2])(rectBoard)])
    
    chalk = SPHERE(0.1*p)([13,13])
    chalk = OFFSET([0,p,p])(chalk)
    c = CUBOID([p/10,1.5*p,1.5*p])
    
    return COLOR(MARRONCINO)(INTERSECTION([c,T([1,2,3])([p/10,0.1*p,0.1*p])(chalk)]))
    
def getLibro(l,p,h,nPagine):
    behind_side = SPHERE(0.1)([20,2])
    behind_side = OFFSET([h,0,0.2])(behind_side)
    
    return behind_side

def getTavolo(l,p,h):
    LARGHEZZA_PIANO = l+DEPTH_PIANO*6
    PROFONDITA_PIANO = p+DEPTH_PIANO*3
    
    downSide_piano = COLOR(MARRONCINO)(MKPOL([[[0,0,0],[LARGHEZZA_PIANO,0,0],[0,PROFONDITA_PIANO,0],[LARGHEZZA_PIANO,PROFONDITA_PIANO,0]],[[1,2,3,4]],1]))
    upSide_piano = COLOR(GREEN_TABLE)(MKPOL([[[0,0,DEPTH_PIANO],[LARGHEZZA_PIANO,0,DEPTH_PIANO],[0,PROFONDITA_PIANO,DEPTH_PIANO],[LARGHEZZA_PIANO,PROFONDITA_PIANO,DEPTH_PIANO]],[[1,2,3,4]],1]))
    rightSide_piano = COLOR(MARRONCINO)(MKPOL([[[LARGHEZZA_PIANO,0,0],[LARGHEZZA_PIANO,0,DEPTH_PIANO],[LARGHEZZA_PIANO,PROFONDITA_PIANO,0],[LARGHEZZA_PIANO,PROFONDITA_PIANO,DEPTH_PIANO]],[[1,2,3,4]],1]))
    leftSide_piano = COLOR(MARRONCINO)(MKPOL([[[0,0,0],[0,0,DEPTH_PIANO],[0,PROFONDITA_PIANO,0],[0,PROFONDITA_PIANO,DEPTH_PIANO]],[[1,2,3,4]],1]))
    nearSide_piano = COLOR(MARRONCINO)(MKPOL([[[0,0,0],[0,0,DEPTH_PIANO],[LARGHEZZA_PIANO,0,0],[LARGHEZZA_PIANO,0,DEPTH_PIANO]],[[1,2,3,4]],1]))
    farSide_piano = COLOR(MARRONCINO)(MKPOL([[[0,PROFONDITA_PIANO,0],[0,PROFONDITA_PIANO,DEPTH_PIANO],[LARGHEZZA_PIANO,PROFONDITA_PIANO,0],[LARGHEZZA_PIANO,PROFONDITA_PIANO,DEPTH_PIANO]],[[1,2,3,4]],1]))
    piano = STRUCT([upSide_piano,downSide_piano,rightSide_piano,leftSide_piano,nearSide_piano,farSide_piano])
    
    '''sezione_tubo_piccolo = SPHERE(DEPTH_PIANO)([19,2])
    sezione_tubo_grande = SPHERE(DEPTH_PIANO*2)([19,2])
    cerchio_grande = OFFSET([DEPTH_PIANO,0,0])(sezione_tubo_grande)
    cerchio_piccolo = OFFSET([DEPTH_PIANO,0,0])(sezione_tubo_piccolo)
    anello = DIFFERENCE([cerchio_grande,cerchio_piccolo])
    anello = R([1,2])(PI/2)(anello)
    anello = T([1,3])([DEPTH_PIANO*2,DEPTH_PIANO*2])(anello)
   
    c = CUBOID([DEPTH_PIANO*4,DEPTH_PIANO,DEPTH_PIANO*4])
    c = T([1,3])([DEPTH_PIANO*2,DEPTH_PIANO*2])(c)
    
    
    anello_quarti = INTERSECTION([anello,c])
    anello_quarti = T([1,3])([-DEPTH_PIANO*2,-DEPTH_PIANO*2])(anello_quarti)'''
    
    ring = TORUS([DEPTH_PIANO*2,DEPTH_PIANO])([20,20])
    ring = T([1,3])([DEPTH_PIANO*2,DEPTH_PIANO/2])(ring)
    ring = OFFSET([0.001,0.001,0.001])(ring)                    #faccio l'OFFSET perch altrimenti non mi fa vedere l'oggetto
    c = CUBOID([DEPTH_PIANO*4,DEPTH_PIANO*4,DEPTH_PIANO*1.2])
    c = T(1)(DEPTH_PIANO*2)(c)
    
    anello_quarti = R([2,3])(PI/2)(INTERSECTION([ring,c]))
    
    tubo = R([3,1])(PI/2)(TUBE([DEPTH_PIANO/35,DEPTH_PIANO/2,l])(20))
    leg =TUBE([DEPTH_PIANO/35,DEPTH_PIANO/2,h])(20)
    
    tubo_dx = STRUCT([T([1,2])([DEPTH_PIANO*2,DEPTH_PIANO/2])(leg),T([1,2,3])([-DEPTH_PIANO*1.49,DEPTH_PIANO,h])(anello_quarti)])
    tubo_sx = T([3,1])([DEPTH_PIANO*2,DEPTH_PIANO])(R([1,2])(PI)(tubo_dx))
    
    stecca = STRUCT([tubo_sx,T([1,3])([DEPTH_PIANO*2,h+DEPTH_PIANO])(tubo),T(1)(l+DEPTH_PIANO*2)(tubo_dx)])
    tubo_laterale = R([3,2])(PI/2)(TUBE([DEPTH_PIANO/35,DEPTH_PIANO/2,p])(20))
    
    
    skeleton = COLOR(GRAY)(STRUCT([stecca,T([2,3])([DEPTH_PIANO,h-DEPTH_PIANO*8])(tubo_laterale),T(2)(p)(stecca),T([1,2,3])([l+DEPTH_PIANO*3,DEPTH_PIANO,h-DEPTH_PIANO*8])(tubo_laterale)]))
    
    ripiano = CUBOID([l+DEPTH_PIANO*4,p-DEPTH_PIANO,DEPTH_PIANO])
    ripiano_lontano = CUBOID([l+DEPTH_PIANO*4,DEPTH_PIANO,DEPTH_PIANO*6])
    ripiano = COLOR(MARRONCINO)(STRUCT([T(2)(DEPTH_PIANO)(ripiano),T([2,3])([p-DEPTH_PIANO,DEPTH_PIANO])(ripiano_lontano)]))
    
    skeleton_ripiano = STRUCT([skeleton,T(3)(h-DEPTH_PIANO*7)(ripiano)])
    
    tavolo = STRUCT([T([1,2])([DEPTH_PIANO,DEPTH_PIANO])(skeleton_ripiano),T(3)(h+DEPTH_PIANO*2)(piano)])
    
    return tavolo

VIEW(getTavolo(1.6,0.8,0.72))