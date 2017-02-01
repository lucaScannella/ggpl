from pyplasm import*

def drawgraph (f):
	domain = INTERVALS(PI)(64)
	return MAP([ S1, COMP([f,S1]) ])(domain)

out = STRUCT(AA(POLYLINE)([[[0,0],[4,2],[2.5,3],[4,5],[2,5],[0,3],[-3,3],[0,0]],[[0,3],[0,1],[2,2],[2,4],[0,3]],[[2,2],[1,3],[1,2],[2,2]]]))

c = PROD([ SOLIDIFY(out), Q(1) ])

c2 = [T(1)(6),c]

'''ambient =[0.4,g*0.4,b*0.4,alpha]
diffuse =[r*0.6,g*0.6,b*0.6,alpha]
specular=[0,0,0,alpha]
emission=[0,0,0,alpha]'''
#VIEW(MAP(BEZIER(S1)([[-0,0],[1,4],[1,1],[2,1],[3,1]]))(INTERVALS(1)(32)))

c = CUBOID([1,1,1])
c =  MATERIAL([GREEN, 0.4])(c)

#c = TEXTURE(['ciocco.png',True,True,0,0,0,1,1,0,0])(c)

VIEW(c)
#VIEW(PROD([OFFSET([.1,.1])(MAP(BEZIER(S1)([[0,0],[8,0],[5,5],[2,-3],[0,8],[0,0]]))(INTERVALS(1)(64))),Q(.1)]))


#VIEW(SOLIDIFY(out))
#VIEW(SKELETON(1)(muro))