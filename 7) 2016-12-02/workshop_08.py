from pyplasm import *
from workshop_07 import makeObject
import csv

def planimetrier(file_name):
    planimetry = QUOTE([0])
    with open(file_name,'r') as csvFile:
        rows = csv.reader(csvFile, delimiter=' ', quotechar='|')
        for row in rows:
            l = turnStringOnList(row[0])
            linea = MKPOL([[[l[0],l[1],0],[l[2],l[3],0]],[[1,2]],1])
            planimetry = STRUCT([planimetry,linea])
            
    return planimetry
    
def turnStringOnList(stringa):
    lista = stringa.split(",")
    listaAppoggio = []
    for el in lista:
        listaAppoggio.append(float(el)/20.)
    return listaAppoggio
    
def door_maker(file_name):
    porte = QUOTE([0])
    with open(file_name,'r') as csvFile:
        rows = csv.reader(csvFile, delimiter=' ', quotechar='|')
        for row in rows:
            l = turnStringOnList(row[0])
            x1 = l[0]
            x2 = l[2]
            y1 = l[1]
            y2 = l[3]
            portaZ = [2]
            if y2-y1 == 0:
                portaX = [x1,x2-x1]
                portaY = [y1,0.4]
                occPorta = fillPorta(len(portaX),len(portaY),len(portaZ))
            else:
                portaX = [x1,0.4]
                portaY = [y1,y2-y1]
                occPorta = fillPorta(len(portaX),len(portaY),len(portaZ))
            porta = makeObject(portaX,portaY,portaZ,occPorta)
            porte = STRUCT([porte,porta])
            
    return porte
    
    
def fillPorta(x,y,z):
    occPorta = [[[0 for k in xrange(z)] for j in xrange(y)] for i in xrange(x)]
    
    occPorta[0][0][0] = 0
    occPorta[1][1][0] = 1
    occPorta[0][1][0] = 0
    occPorta[1][0][0] = 0

    return occPorta
    
def ggpl_planimetria():
    muri_esterni = planimetrier("muri_esterni.lines")
    muri_esterni = OFFSET([0.4,0.4,5])(muri_esterni)
    muri_esterni = DIFFERENCE([muri_esterni,CUBOID([0.4,0.4,5])])

    muri_interni = planimetrier("muri_interni.lines")
    muri_interni = OFFSET([0.2,0.2,5])(muri_interni)
    muri_interni = DIFFERENCE([muri_interni,CUBOID([0.4,0.4,5])])
    
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
    
    doors = door_maker("finestre.lines")
    return doors

VIEW(ggpl_planimetria())