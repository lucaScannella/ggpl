from pyplasm import*
import pprint

GLASS = Color4f([216/255.,243/255.,249/255.,50/255.])
WINDOW_WOOD = Color4f([154/255.,105/255.,83/255.,1.0])

DOOR_DARK_WOOD = Color4f([170/255.,144/255.,125/255.,1.0])
DOOR_WOOD = Color4f([230/255.,207/255.,168/255.,1.0])
DIRTY_YELLOW = Color4f([200/255.,188/255.,87/255.,1.0])
LIGHT_YELLOW = Color4f([250/255.,250/255.,176/255.,1.0])
GLASS_TEXTURE = ["window_texture.jpg",True,False,1,1,0,1,1]
LIGHT_WOOD_TEXTURE = ["light_wood_texture.jpg",True,False,1,1,0,1,1]
DARK_WOOD_TEXTURE = ["dark_wood_texture.jpg",True,False,1,1,PI/2,0.25,1]
WOOD_WINDOW_TEXTURE = ["wood_window_texture.jpg",True,False,1,1,PI/2,0.25,1]


def getPoints(posVertice,distanze):
    
    sommaDistanze = 0
    for i in distanze[:posVertice+1]:
        sommaDistanze += i
        
    vertBelow = sommaDistanze - distanze[posVertice]
    
    return [vertBelow,sommaDistanze]

def makeObject(distX,distY,distZ,occupancy):
    
    window = STRUCT([QUOTE([0])])
    
    for x in range(len(distX)):
        for y in range(len(distY)):
            for z in range(len(distZ)):
                if occupancy[x][y][z] != 0:
                    cell = MKPOL([getVerts(x,y,z,distX,distY,distZ),[[1,2,3,4,5,6,7,8]],1])
                    if occupancy[x][y][z] == 1:
                        cell = TEXTURE(WOOD_WINDOW_TEXTURE)(cell)
                    elif occupancy[x][y][z] == 2:
                        cell = TEXTURE(GLASS_TEXTURE)(cell)
                    elif occupancy[x][y][z] == 3:
                        cell = TEXTURE(DARK_WOOD_TEXTURE)(cell)
                    elif occupancy[x][y][z] == 4:
                        cell = TEXTURE(LIGHT_WOOD_TEXTURE)(cell)
                    window = STRUCT([window,cell])
    return window
    
def getVerts(x,y,z,distX,distY,distZ):
    xPoints = getPoints(x,distX)
    yPoints = getPoints(y,distY)
    zPoints = getPoints(z,distZ)
    
    verts=[]
    
    for x in xPoints:
        for y in yPoints:
            for z in zPoints:
                vert = [x,y,z]
                verts.append(vert)

    return verts

def fillOccFinestra(x,y,z):
    occFinestra = [[[0 for k in xrange(z)] for j in xrange(y)] for i in xrange(x)]
    
    occFinestra[0][0][0] = 1
    occFinestra[0][0][1] = 1
    occFinestra[0][0][2] = 1
    occFinestra[0][0][3] = 1
    occFinestra[0][0][4] = 1
    occFinestra[0][0][5] = 1
    occFinestra[0][0][6] = 1
    occFinestra[0][0][7] = 1
    occFinestra[0][1][0] = 1
    occFinestra[0][1][1] = 1
    occFinestra[0][1][2] = 1
    occFinestra[0][1][3] = 1
    occFinestra[0][1][4] = 1
    occFinestra[0][1][5] = 1
    occFinestra[0][1][6] = 1
    occFinestra[0][1][7] = 1
    occFinestra[0][2][0] = 1
    occFinestra[0][2][1] = 1
    occFinestra[0][2][2] = 1
    occFinestra[0][2][3] = 1
    occFinestra[0][2][4] = 1
    occFinestra[0][2][5] = 1
    occFinestra[0][2][6] = 1
    occFinestra[0][2][7] = 1
    
    occFinestra[1][0][0] = 1
    occFinestra[1][0][1] = 0
    occFinestra[1][0][2] = 0
    occFinestra[1][0][3] = 0
    occFinestra[1][0][4] = 1
    occFinestra[1][0][5] = 0
    occFinestra[1][0][6] = 1
    occFinestra[1][0][7] = 0
    occFinestra[1][1][0] = 1
    occFinestra[1][1][1] = 2
    occFinestra[1][1][2] = 2
    occFinestra[1][1][3] = 2
    occFinestra[1][1][4] = 2
    occFinestra[1][1][5] = 2
    occFinestra[1][1][6] = 2
    occFinestra[1][1][7] = 2
    occFinestra[1][2][0] = 1
    occFinestra[1][2][1] = 0
    occFinestra[1][2][2] = 0
    occFinestra[1][2][3] = 0
    occFinestra[1][2][4] = 1
    occFinestra[1][2][5] = 0
    occFinestra[1][2][6] = 1
    occFinestra[1][2][7] = 0
    
    occFinestra[2][0][0] = 1
    occFinestra[2][0][1] = 0
    occFinestra[2][0][2] = 1
    occFinestra[2][0][3] = 1
    occFinestra[2][0][4] = 1
    occFinestra[2][0][5] = 1
    occFinestra[2][0][6] = 1
    occFinestra[2][0][7] = 1
    occFinestra[2][1][0] = 1
    occFinestra[2][1][1] = 2
    occFinestra[2][1][2] = 2
    occFinestra[2][1][3] = 2
    occFinestra[2][1][4] = 2
    occFinestra[2][1][5] = 2
    occFinestra[2][1][6] = 2
    occFinestra[2][1][7] = 2
    occFinestra[2][2][0] = 1
    occFinestra[2][2][1] = 0
    occFinestra[2][2][2] = 1
    occFinestra[2][2][3] = 1
    occFinestra[2][2][4] = 1
    occFinestra[2][2][5] = 1
    occFinestra[2][2][6] = 1
    occFinestra[2][2][7] = 1
    
    occFinestra[3][0][0] = 1
    occFinestra[3][0][1] = 0
    occFinestra[3][0][2] = 1
    occFinestra[3][0][3] = 0
    occFinestra[3][0][4] = 1
    occFinestra[3][0][5] = 0
    occFinestra[3][0][6] = 1
    occFinestra[3][0][7] = 0
    occFinestra[3][1][0] = 1
    occFinestra[3][1][1] = 2
    occFinestra[3][1][2] = 2
    occFinestra[3][1][3] = 2
    occFinestra[3][1][4] = 2
    occFinestra[3][1][5] = 2
    occFinestra[3][1][6] = 2
    occFinestra[3][1][7] = 2
    occFinestra[3][2][0] = 1
    occFinestra[3][2][1] = 0
    occFinestra[3][2][2] = 1
    occFinestra[3][2][3] = 0
    occFinestra[3][2][4] = 1
    occFinestra[3][2][5] = 0
    occFinestra[3][2][6] = 1
    occFinestra[3][2][7] = 0
    
    occFinestra[4][0][0] = 1
    occFinestra[4][0][1] = 1
    occFinestra[4][0][2] = 1
    occFinestra[4][0][3] = 1
    occFinestra[4][0][4] = 1
    occFinestra[4][0][5] = 0
    occFinestra[4][0][6] = 1
    occFinestra[4][0][7] = 0
    occFinestra[4][1][0] = 1
    occFinestra[4][1][1] = 2
    occFinestra[4][1][2] = 2
    occFinestra[4][1][3] = 2
    occFinestra[4][1][4] = 2
    occFinestra[4][1][5] = 2
    occFinestra[4][1][6] = 2
    occFinestra[4][1][7] = 2
    occFinestra[4][2][0] = 1
    occFinestra[4][2][1] = 1
    occFinestra[4][2][2] = 1
    occFinestra[4][2][3] = 1
    occFinestra[4][2][4] = 1
    occFinestra[4][2][5] = 0
    occFinestra[4][2][6] = 1
    occFinestra[4][2][7] = 0
    
    occFinestra[5][0][0] = 1 
    occFinestra[5][0][1] = 0
    occFinestra[5][0][2] = 1
    occFinestra[5][0][3] = 0
    occFinestra[5][0][4] = 0
    occFinestra[5][0][5] = 0
    occFinestra[5][0][6] = 1
    occFinestra[5][0][7] = 0
    occFinestra[5][1][0] = 1
    occFinestra[5][1][1] = 2
    occFinestra[5][1][2] = 2
    occFinestra[5][1][3] = 2
    occFinestra[5][1][4] = 2
    occFinestra[5][1][5] = 2
    occFinestra[5][1][6] = 2
    occFinestra[5][1][7] = 2
    occFinestra[5][2][0] = 1
    occFinestra[5][2][1] = 0
    occFinestra[5][2][2] = 1
    occFinestra[5][2][3] = 0
    occFinestra[5][2][4] = 0
    occFinestra[5][2][5] = 0
    occFinestra[5][2][6] = 1
    occFinestra[5][2][7] = 0
    
    return occFinestra

def fillOccPorta(x,y,z):
    occPorta = [[[0 for k in xrange(z)] for j in xrange(y)] for i in xrange(x)]
    
    occPorta[0][0][0] = 4
    occPorta[0][0][1] = 4
    occPorta[0][0][2] = 4
    occPorta[0][0][3] = 4
    occPorta[0][0][4] = 4
    occPorta[0][1][0] = 4
    occPorta[0][1][1] = 4
    occPorta[0][1][2] = 4
    occPorta[0][1][3] = 4
    occPorta[0][1][4] = 4
    occPorta[0][2][0] = 4
    occPorta[0][2][1] = 4
    occPorta[0][2][2] = 4
    occPorta[0][2][3] = 4
    occPorta[0][2][4] = 4
    
    occPorta[1][0][0] = 4
    occPorta[1][0][1] = 0
    occPorta[1][0][2] = 4
    occPorta[1][0][3] = 0
    occPorta[1][0][4] = 4
    occPorta[1][1][0] = 4
    occPorta[1][1][1] = 3
    occPorta[1][1][2] = 4
    occPorta[1][1][3] = 2
    occPorta[1][1][4] = 4
    occPorta[1][2][0] = 4
    occPorta[1][2][1] = 0
    occPorta[1][2][2] = 4
    occPorta[1][2][3] = 0
    occPorta[1][2][4] = 4
    
    occPorta[2][0][0] = 4
    occPorta[2][0][1] = 4
    occPorta[2][0][2] = 4
    occPorta[2][0][3] = 4
    occPorta[2][0][4] = 4
    occPorta[2][1][0] = 4
    occPorta[2][1][1] = 4
    occPorta[2][1][2] = 4
    occPorta[2][1][3] = 4
    occPorta[2][1][4] = 4
    occPorta[2][2][0] = 4
    occPorta[2][2][1] = 4
    occPorta[2][2][2] = 4
    occPorta[2][2][3] = 4
    occPorta[2][2][4] = 4
    
    return occPorta

def makeWindowDoor():
    
    '''__________________________________________________________PORTA FINESTRA_________________________________________________________'''
    portaX = [0.1,0.4,0.1]
    portaY = [0.03,0.03,0.03]
    portaZ = [0.1,0.5,0.1,1.0,0.1]
    
    occPorta = fillOccPorta(len(portaX),len(portaY),len(portaZ))
    anta = makeObject(portaX,portaY,portaZ,occPorta)
    base_maniglia = CUBOID([0.03,0.01,0.03])
    base_maniglia = COLOR(DIRTY_YELLOW)(base_maniglia)
    maniglia = MKPOL([[[0,0,0],[0.01,0,0],[0,0,0.04],[0.01,0,0.04],[0,0,0.03],[0.08,0,0.03],[0.08,0,0.04]],[[1,2,3,4],[4,5,6,7]],1])
    maniglia = OFFSET([0,0.01,0])(maniglia)
    maniglia = COLOR(LIGHT_YELLOW)(maniglia)
    maniglia = STRUCT([base_maniglia,T([1,3])([0.01,0.01])(R([2,3])(PI/2)(maniglia))])
    anta_maniglia = STRUCT([anta,T([1,2,3])([portaX[0]/4,-0.01,sum(portaZ)/2])(maniglia)])
    porta = STRUCT([anta,T(1)(sum(portaX))(anta_maniglia)])
    
    
    
    '''____________________________________________________________FINESTRA_____________________________________________________________'''
    finestraX = [0.1,0.03,0.03,0.03,0.03,0.15]
    finestraY = [0.03,0.03,0.03]
    finestraZ = [0.1,0.03,0.03,0.03,0.03,0.6,0.03,0.07]
    
    occFinestraQuarti = fillOccFinestra(len(finestraX),len(finestraY),len(finestraZ))
    finestraQuarti = makeObject(finestraX,finestraY,finestraZ,occFinestraQuarti)
    finestraQuarti = STRUCT([finestraQuarti,T([1,2])([sum(finestraX)*2,sum(finestraY)])(R([1,2])(PI)(finestraQuarti))])
    finestra = STRUCT([finestraQuarti,T([2,3])([sum(finestraY),sum(finestraZ)*2])(R([2,3])(PI)(finestraQuarti))])
    
    return STRUCT([porta,T(1)(sum(portaX)+1)(finestra)])


VIEW(makeWindowDoor())

    