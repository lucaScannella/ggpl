from pyplasm import*
from workshop_08 import*
from workshop_04 import*
from workshop_09 import*

EXTERNAL_WALL = ["external_wall.jpg",True,True,1,1,0,1,1]
FLOOR = ["floor.jpg",True,True,1,1,0,10,4]
EXTERNAL_WALL = Color4f([255/255.,228/255.,196/255.,1.0])
INTERNAL_WALL = Color4f([247/255.,232/255.,159/255.,1.0])


def ggpl_house():
	n = 1.08
	verts = [[8.571874618530273*n, 4.1875*n, 0.0],[0.9590134620666504*n, 4.1875*n, 0.0], [0.9590135216712952*n, 20.04747200012207*n, 0.0],[7.468815326690674*n, 20.04747200012207*n, 0.0],[7.468815326690674*n, 26.437950134277344*n, 0.0],[15.954095840454102*n, 26.437950134277344*n, 0.0],[15.954096794128418*n, 0.6815853118896484*n, 0.0],[8.571874618530273*n, 0.6815851330757141*n, 0.0]]
	fmi = MKPOL([verts,[[1,2,3,4],[1,4,5,6,7,8]],1])
	first_roof = tetto_terrazzo(PI/2.5,fmi,0.1,0)

	first_floor = make_floor(1)
	first_floor = STRUCT([first_floor,T([1,2,3])([-0.6,-0.8,3.2])(first_roof)])

	second_roof = tetto_terrazzo(PI/2.5,fmi,1,1)
	
	second_floor = make_floor(2)
	second_floor = STRUCT([second_floor,T([1,2,3])([-0.5,-0.8,3.2])(second_roof)])

	casa = STRUCT([first_floor,T(3)(3.1)(second_floor)])

	return casa

def make_floor(floor):
	first_muri_esterni = planimetrier("1_muri_est.lines")
	first_muri_esterni = OFFSET([0.01,0.01,3])(first_muri_esterni)

	first_muri_interni = planimetrier("1_muri_int.lines")
	first_muri_interni = OFFSET([0.02,0.02,3])(first_muri_interni)

	first_portone = object_maker("1_portone.lines",1)
	portone = T(1)(0.2)(first_portone)
	first_portone = T(3)(-0.1)(OFFSET([0.2,0.2,0.1])(first_portone))

	first_porte_interne = object_maker("1_porte_int.lines",1)
	porte = T(3)(0.2)(first_porte_interne)
	first_porte_interne = OFFSET([0.2,0.2,0.2])(first_porte_interne)
	


	first_finestre = object_maker("1_finestre.lines",0)
	finestre = T([1,3])([0.2,1.5])(first_finestre)
	first_finestre = OFFSET([0.2,0.2,0.2])(first_finestre)
	first_finestre = OFFSET([-0.05,-0.05,-0.05])(first_finestre)

	if floor == 1:
		first_esterni = DIFFERENCE([first_muri_esterni,first_portone])
		first_esterni = DIFFERENCE([first_esterni,T(3)(1.3)(first_finestre)])
	else:
		first_esterni = DIFFERENCE([first_muri_esterni,T(3)(1.3)(first_finestre)])

	first_esterni = OFFSET([0.25,0.25,0.25])(first_esterni)
	first_esterni = COLOR(EXTERNAL_WALL)(first_esterni)


	first_interni = DIFFERENCE([first_muri_interni,first_porte_interne])
	first_interni = OFFSET([0.15,0.15,0.15])(first_interni)
	first_interni = COLOR(INTERNAL_WALL)(first_interni)

	floor = makeFloor("1_muri_est.lines")
	floor = TEXTURE(FLOOR)(floor)

	muri = STRUCT([first_interni,first_esterni,floor])

	casa = STRUCT([muri,finestre,porte,portone])

	return casa

def verts(file_name):
    planimetry = None
    linea = []
    with open(file_name,'r') as csvFile:
        rows = csv.reader(csvFile, delimiter=' ', quotechar='|')
        for row in rows:
            l = turnStringOnList(row[0])
            p1 = [l[0],l[1],0]
            p2 = [l[2],l[3],0]
            linea.append(p1)
            linea.append(p2)

    return linea
    
def turnStringOnList(stringa):
    lista = stringa.split(",")
    listaAppoggio = []
    for el in lista:
        listaAppoggio.append(float(el)/20.)
    return listaAppoggio


VIEW(ggpl_house())