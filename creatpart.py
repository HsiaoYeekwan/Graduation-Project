from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

Mdb()
#the model paramerters
d = 17.0
D = 26.0
B = 5.0
DAmin = 19.0
DAmax = 19.0

W = (DAmin - d ) / 2
R = ((D - d) / 2 - 2 * W)/2
H1 = H2 = W + 1

def CreateBearingShell():
    #create a new sketch class
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=1000.0)
    g, v, c = s.geometry, s.vertices, s.constraints
    #necessary
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -500.0), point2=(0.0, 500.0))
    s.FixedConstraint(entity=g[2])
    
    s.Line(point1=(d/2.0, 0.0), point2=(d/2.0, B/2.0))
    s.VerticalConstraint(entity=g[3], addUndoState=False)
    
    s.Line(point1=(d/2, B/2), point2=(d/2+H1, B/2))
    s.HorizontalConstraint(entity=g[4], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    
    s.Line(point1=(d/2+H1, B/2), point2=(d/2+H1, 0.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
    
    s.Line(point1=(D/2-H2, 0.0), point2=(D/2-H2, B/2))
    s.VerticalConstraint(entity=g[6], addUndoState=False)
    
    s.Line(point1=(D/2-H2, B/2), point2=(D/2, B/2))
    s.HorizontalConstraint(entity=g[7], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[6], entity2=g[7], addUndoState=False)
    
    s.Line(point1=(D/2, B/2), point2=(D/2, 0.0))
    s.VerticalConstraint(entity=g[8], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[7], entity2=g[8], addUndoState=False)
    
    s.Arc3Points(point1=(d/2+W, 0.0), point2=(D/2-W, 0.0), point3=((D+d)/4, R))
    
    s.autoTrimCurve(curve1=g[5], point1=(d/2+H1, 0.0))
    s.autoTrimCurve(curve1=g[6], point1=(D/2-H2, 0.0))
    s.autoTrimCurve(curve1=g[9], point1=(d/2+W+R, R))
    
    s.Line(point1=(d/2+W, 0.0), point2=(D/2-W, 0.0))
    s.HorizontalConstraint(entity=g[14], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[12], entity2=g[14], addUndoState=False)
    s.copyMirror(mirrorLine=g[14], objectList=(g[3], g[4], g[7], g[8], g[10], 
    g[11], g[12], g[13]))
    s.autoTrimCurve(curve1=g[14], point1=(15.5, 0.0))
    
    p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Part-1']
    p.BaseSolidRevolve(sketch=s, angle=360.0, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Part-1']
    del mdb.models['Model-1'].sketches['__profile__']
def CreateBearingBall():
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
    sheetSize=1000.0)
    g, v, c = s1.geometry, s1.vertices, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.ConstructionLine(point1=(0.0, -500.0), point2=(0.0, 500.0))
    s1.FixedConstraint(entity=g[2])
    s1.Arc3Points(point1=(0.0, R), point2=(0.0, -R), point3=(R, 0.0))
    s1.Line(point1=(0.0, R), point2=(0.0, -R))
    s1.VerticalConstraint(entity=g[4], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    p = mdb.models['Model-1'].Part(name='Part-2', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Part-2']
    p.BaseSolidRevolve(sketch=s1, angle=360.0, flipRevolveDirection=OFF)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Part-2']
    del mdb.models['Model-1'].sketches['__profile__']
    #cut the ball
    p = mdb.models['Model-1'].parts['Part-2']
    p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=0.0)
    p.DatumPlaneByPrincipalPlane(principalPlane=XZPLANE, offset=0.0)
    p.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=0.0)

    p = mdb.models['Model-1'].parts['Part-2']
    datums = p.datums
    c = p.cells
    p.PartitionCellByDatumPlane(datumPlane=datums[4], cells=c)
    c = p.cells
    p.PartitionCellByDatumPlane(datumPlane=datums[2], cells=c)
    c = p.cells
    p.PartitionCellByDatumPlane(datumPlane=datums[3], cells=c)

def CreateSupport():
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=1000.0)
    g = s.geometry
    s.setPrimaryObject(option=STANDALONE)
    s.Line(point1=(0.0, 0.0), point2=(D/2+40, 0.0))
    s.HorizontalConstraint(entity=g[2], addUndoState=False)
    
    s.Line(point1=(D/2+40, 0.0), point2=(D/2+40, 14.0))
    s.VerticalConstraint(entity=g[3], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
    
    s.Line(point1=(D/2+40, 14.0), point2=(D/2+20, 14.0))
    s.HorizontalConstraint(entity=g[4], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    
    s.Line(point1=(D/2+20, 14.0), point2=(D/2+20, 100+D+20))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
    
    s.Line(point1=(D/2+20, 100+D+20), point2=(0.0, 100+D+20))
    s.HorizontalConstraint(entity=g[6], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[5], entity2=g[6], addUndoState=False)
    
    s.Line(point1=(0.0, 100+D+20), point2=(0.0, 0.0))
    s.VerticalConstraint(entity=g[7], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[6], entity2=g[7], addUndoState=False)
    
    s.copyMirror(mirrorLine=g[7], objectList=(g[2], g[3], g[4], g[5], g[6]))
    s.autoTrimCurve(curve1=g[7], point1=(0.0,D))
   
    s.CircleByCenterPerimeter(center=(0.0, 100+D/2), point1=(0.0, 100+D))
    p = mdb.models['Model-1'].Part(name='Part-3', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Part-3']
    p.BaseSolidExtrude(sketch=s, depth=B*2)
    s.unsetPrimaryObject()
    del mdb.models['Model-1'].sketches['__profile__']
    
def Assembly(number_of_balls):
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['Part-1']
    a.Instance(name='Part-1-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['Part-2']
    a.Instance(name='Part-2-1', part=p, dependent=ON)
    a.translate(instanceList=('Part-2-1', ), vector=(d/2+W+R, 0.0, 0.0))
    a.RadialInstancePattern(instanceList=('Part-2-1', ), point=(0.0, 0.0, 0.0), 
        axis=(0.0, 1.0, 0.0), number=number_of_balls, totalAngle=360.0)
    p = mdb.models['Model-1'].parts['Part-3']
    a.Instance(name='Part-3-1', part=p, dependent=ON)
    a.translate(instanceList=('Part-3-1', ), vector=(0.0, -(100+D/2), 0.0))
    a.rotate(instanceList=('Part-3-1', ), axisPoint=(0.0, 0.0, 0.0), 
        axisDirection=(1.0, 0.0, 0.0), angle=90.0)
    a.translate(instanceList=('Part-3-1', ), vector=(0.0, B, 0.0))
    
    
if __name__ == '__main__':
    CreateBearingShell()
    CreateBearingBall()
    CreateSupport()
    Assembly(9)
    