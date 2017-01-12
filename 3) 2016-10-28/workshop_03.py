from pyplasm import*
from math import*

def ggpl_myStair(x,y,z):
    soglia = 0.15/0.3
    if float(z)/float(y) >= soglia+1.6:
        z = input("l'altezza e troppo grande reinseriscila")
    if float(z)/float(y) <= soglia-0.4:
        y = input("la profondita e troppo grande reinseriscila")
    nScalini = int(z/0.15)
    profScalino = float(y)/nScalini
    altezzaScalino = float(z)/nScalini
    
    scalino = MKPOL([[[0,0,0],[0,0,altezzaScalino],[0,profScalino,0],[0,profScalino*2,altezzaScalino],[x,0,0],[x,0,altezzaScalino],[x,profScalino,0],[x,profScalino*2,altezzaScalino]],[[1,2,3,4,5,6,7,8]],1])
    
    c = profScalino-(1/2)*altezzaScalino
    scalino2 = CUBOID([x,profScalino,altezzaScalino/2])
    nearScalino = MKPOL([[[0,0,0],[0,0,1.5*altezzaScalino],[0,c,1.5*altezzaScalino],[0,0.5*altezzaScalino,0],[0,0.5*altezzaScalino,altezzaScalino],[0,c,altezzaScalino],[0.05,0,0],[0.05,0,1.5*altezzaScalino],[0.05,c,1.5*altezzaScalino],[0.05,0.5*altezzaScalino,0],[0.05,0.5*altezzaScalino,altezzaScalino],[0.05,c,altezzaScalino]],[[1,2,4,5,7,8,10,11],[2,3,5,6,8,9,11,12]],1])
    stair = QUOTE([0])
    nearScalini = QUOTE([0])
    distY=0
    distZ=0
    for i in range(nScalini):
        nearScalini = STRUCT([nearScalini,T([2,3])([distY,distZ])(nearScalino)])
        #stair = STRUCT([stair,T([2,3])([distY,distZ])(scalino)])
        stair = STRUCT([stair,T([2,3])([distY,distZ])(scalino2)])
        distY = distY + profScalino
        distZ = distZ + altezzaScalino
    ''' endScalino=CUBOID([x,profScalino,altezzaScalino])
    stair = STRUCT([stair,T([2,3])([distY,distZ])(endScalino)])'''
    
    stair = COLOR(YELLOW)(stair)
    stair = STRUCT([nearScalini,T([1,3])([0.005,altezzaScalino])(stair),T(1)(x+0.005)(nearScalini)])
    
    wall = CUBOID([0.2,y,z+altezzaScalino/2])
    wall = COLOR(BROWN)(wall)
    stair = STRUCT([wall,T(1)(0.2)(stair)])
    return stair

VIEW(ggpl_myStair(2,3,2))