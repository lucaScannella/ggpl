from pyplasm import *
from workshop_07 import makeObject
import csv

#EXTERNAL_WALL = ["external_wall.jpg",True,True,1,1,0,10,2]

def planimetrier(file_name):
    planimetry = None
    with open(file_name,'r') as csvFile:
        rows = csv.reader(csvFile, delimiter=' ', quotechar='|')
        for row in rows:
            l = turnStringOnList(row[0])
            #linea = MKPOL([[[l[0],l[1],0],[l[2],l[3],0],[l[0],l[1],3],[l[2],l[3],3]],[[1,2,3,4]],1])
            linea = MKPOL([[[l[0],l[1],0],[l[2],l[3],0]],[[1,2]],1])
            '''if l[2]-l[0] == 0:
                linea = TEXTURE(["brick.jpeg",True,True,1,1,0,math.fabs(l[3]-l[1])/3,1])(linea)
            elif l[3]-l[1] == 0:
                linea = TEXTURE(["brick.jpeg",True,True,1,1,0,math.fabs(l[2]-l[0])/3,1])(linea)
            else:
                linea = TEXTURE(["brick.jpeg",True,True,1,1,0,10,3])(linea)'''

            if planimetry == None:
                planimetry = linea
            else:
                planimetry = STRUCT([planimetry,linea])

            
    return planimetry
    
def turnStringOnList(stringa):
    lista = stringa.split(",")
    listaAppoggio = []
    for el in lista:
        listaAppoggio.append(float(el)/20.)
    return listaAppoggio
    
def door_maker(file_name):
    porte = None
    with open(file_name,'r') as csvFile:
        rows = csv.reader(csvFile, delimiter=' ', quotechar='|')
        for row in rows:
            l = turnStringOnList(row[0])
            x1 = l[0]
            x2 = l[2]
            y1 = l[1]
            y2 = l[3]
            portaZ = [4]
            if y2-y1 == 0:
                portaX = [x1,x2-x1+0.4]
                portaY = [y1,0.2]
                occPorta = fillPorta(len(portaX),len(portaY),len(portaZ))
            else:
                portaX = [x1-0.08,0.33]
                portaY = [y1,y2-y1+0.4]
                occPorta = fillPorta(len(portaX),len(portaY),len(portaZ))
            porta = makeObject(portaX,portaY,portaZ,occPorta)
            if porte == None:
                porte = porta
            else:
                porte = STRUCT([porte,porta])
            
    return porte

def window_maker(file_name):
    windows = None
    with open(file_name,'r') as csvFile:
        rows = csv.reader(csvFile, delimiter=' ', quotechar='|')
        for row in rows:
            l = turnStringOnList(row[0])
            x1 = l[0]
            x2 = l[2]
            y1 = l[1]
            y2 = l[3]
            windowZ = [2.5]
            if y2-y1 == 0:
                windowX = [x1-0.2,x2-x1+0.6]
                windowY = [y1+0.1,0.2]
                occWindow = fillWindow(len(windowX),len(windowY),len(windowZ))
            else:
                windowX = [x1+0.1,0.2]
                windowY = [y1,y2-y1+0.4]
                occWindow = fillWindow(len(windowX),len(windowY),len(windowZ))
            window = makeObject(windowX,windowY,windowZ,occWindow)
            if windows == None:
                windows = window
            else:
                windows = STRUCT([window,windows])
            
    return windows

def object_maker(file_name,n):
    objs = None
    with open(file_name,'r') as csvFile:
        rows = csv.reader(csvFile, delimiter=' ', quotechar='|')
        for row in rows:
            l = turnStringOnList(row[0])
            x1 = l[0]
            x2 = l[2]
            y1 = l[1]
            y2 = l[3]

            if n==0:
                objZ = [1]
            elif n==1:
                objZ = [2.5]

            if y2-y1 == 0:
                objX = [x1,x2-x1]
                objY = [y1,0.2]
            else:
                objX = [x1,0.2]
                objY = [y1,y2-y1]

            if n==0:
                occObj = fillWindow(len(objX),len(objY),len(objZ))
            elif n==1:
                occObj = fillPorta(len(objX),len(objY),len(objZ))

            obj = makeObject(objX,objY,objZ,occObj)

            if objs == None:
                objs = obj
            else:
                objs = STRUCT([obj,objs])
            
    return objs

def makeFloor(file_name):
    floor = None
    with open(file_name,'r') as csvFile:
        rows = csv.reader(csvFile, delimiter=' ', quotechar='|')
        for row in rows:
            l = turnStringOnList(row[0])
            p1 = [l[0],l[1]]
            p2 = [l[2],l[3]]
            c = STRUCT( AA(POLYLINE)([[p1,p2]]))
            if floor == None:
                floor = c
            else:
                floor = STRUCT([floor,c])
    
    floor = SOLIDIFY(floor)
    return floor

    
def fillPorta(x,y,z):
    occPorta = [[[0 for k in xrange(z)] for j in xrange(y)] for i in xrange(x)]
    
    occPorta[0][0][0] = 0
    occPorta[1][1][0] = 1
    occPorta[0][1][0] = 0
    occPorta[1][0][0] = 0

    return occPorta
    
def fillWindow(x,y,z):
    occWindow = [[[0 for k in xrange(z)] for j in xrange(y)] for i in xrange(x)]
    
    occWindow[0][0][0] = 0
    occWindow[1][1][0] = 2
    occWindow[0][1][0] = 0
    occWindow[1][0][0] = 0

    return occWindow

#def ggpl_planimetria():
    muri_esterni = planimetrier("muri_esterni.lines")
    muri_esterni = OFFSET([0.4,0.4,5])(muri_esterni)
    #muri_esterni = DIFFERENCE([muri_esterni,CUBOID([0.4,0.4,5])])

    muri_interni = planimetrier("muri_interni.lines")
    muri_interni = OFFSET([0.2,0.2,5])(muri_interni)
    #muri_interni = DIFFERENCE([muri_interni,CUBOID([0.4,0.4,5])])
    
    finestre = planimetrier("finestre.lines")
    finestre = OFFSET([0.405,0.4,2.5])(finestre)
    finestre = OFFSET([-0.205,0,0])(finestre)

    
    
    porte = planimetrier("porte.lines")
    porte = OFFSET([0.4,0.41,4])(porte)
    porte = OFFSET([-0.205,0,0])(porte)
    
    pareti = STRUCT([T(2)(0.2)(muri_interni),muri_esterni])

    pareti_porte = DIFFERENCE([muri_interni,T(1)(0.2)(porte)])
    pareti_finestre = DIFFERENCE([muri_esterni,T(3)(1.25)(finestre)])
    pareti_finestre_porta = DIFFERENCE([pareti_finestre,T(1)(0.2)(porte)])
    
    house = STRUCT([pareti_porte,pareti_finestre_porta])
    
    doors = door_maker("porte.lines")
    windows = window_maker("finestre.lines")
    return STRUCT([house,doors,T(3)(1.25)(windows)])

#VIEW(ggpl_planimetria())