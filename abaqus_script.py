from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

Mdb()
#the model paramerters
d = 20.0
D = 42.0
B = 12.0
DAmin = 24.5
DAmax = 25.5

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
    
def AssignSections():
    #create materials 
    mdb.models['Model-1'].Material(name='Material-bearing')
    mdb.models['Model-1'].materials['Material-bearing'].Elastic(table=((203000.0, 
        0.29), ))
    mdb.models['Model-1'].materials['Material-bearing'].Density(table=((7.85e-09, 
        ), ))
    mdb.models['Model-1'].Material(name='Material-support')
    mdb.models['Model-1'].materials['Material-support'].Elastic(table=((195000.0, 
        0.26), ))
    mdb.models['Model-1'].materials['Material-support'].Density(table=((7.3e-09, ), 
        ))
    #create section
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-bearing', 
    material='Material-bearing', thickness=None)
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-support', 
    material='Material-support', thickness=None)
    #to Assignment the sections
    p = mdb.models['Model-1'].parts['Part-1']
    c = p.cells
    region = p.Set(cells=c, name='Set-1')
    p = mdb.models['Model-1'].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Section-bearing', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)

    p = mdb.models['Model-1'].parts['Part-2']
    c = p.cells
    region = p.Set(cells=c, name='Set-1')
    p.SectionAssignment(region=region, sectionName='Section-bearing', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
        
    p = mdb.models['Model-1'].parts['Part-3']
    c = p.cells
    region = p.Set(cells=c, name='Set-1')
    p.SectionAssignment(region=region, sectionName='Section-support', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
def GetMash(Shell_Size , Ball_Size , Support_Size):
    #to generate the mash
    p = mdb.models['Model-1'].parts['Part-1']
    p.seedPart(size=Shell_Size, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()

    p = mdb.models['Model-1'].parts['Part-2']
    p.seedPart(size=Ball_Size, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()

    p = mdb.models['Model-1'].parts['Part-3']
    p.seedPart(size=Support_Size, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    
def StepSetting(TimePeriod , numIntervals , Speed):
    #create step 
    mdb.models['Model-1'].ExplicitDynamicsStep(name='Step-1', previous='Initial', 
        timePeriod=TimePeriod)
    
    #create contact property
    mdb.models['Model-1'].ContactProperty('IntProp-1')
    mdb.models['Model-1'].interactionProperties['IntProp-1'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, table=((
        0.025, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)
    mdb.models['Model-1'].interactionProperties['IntProp-1'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, 
        constraintEnforcementMethod=DEFAULT)
    #create contact
    mdb.models['Model-1'].ContactExp(name='Int-1', createStepName='Initial')
    mdb.models['Model-1'].interactions['Int-1'].includedPairs.setValuesInStep(
        stepName='Initial', useAllstar=ON)
    mdb.models['Model-1'].interactions['Int-1'].contactPropertyAssignments.appendInStep(
        stepName='Initial', assignments=((GLOBAL, SELF, 'IntProp-1'), ))
    #add reference point
    a = mdb.models['Model-1'].rootAssembly
    a.ReferencePoint(point=(0.0, 0.0, 0.0))
    #yueshu binding and couping
    s1 = a.instances['Part-3-1'].faces
    side1Faces1 = s1.findAt(((0.0,0.0,D/2),))
    region1=a.Surface(side1Faces=side1Faces1, name='m_Surf-1')
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['Part-1-1'].faces
    side1Faces1 = s1.findAt(((0.0,0.0,D/2),))
    region2=a.Surface(side1Faces=side1Faces1, name='s_Surf-1')
    mdb.models['Model-1'].Tie(name='Constraint-1', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)
        
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    refPoints1 = r1.findAt((0.0,0.0,0.0))
    refPoints1 = (refPoints1,)
    region1=a.Set(referencePoints=refPoints1, name='m_Set-1')
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['Part-1-1'].faces
    side1Faces1 = s1.findAt(((0.0,0.0,d/2),))
    region2=a.Surface(side1Faces=side1Faces1, name='s_Surf-3')
    mdb.models['Model-1'].Coupling(name='Constraint-2', controlPoint=region1, 
        surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
    #create boundary conditions
    a = mdb.models['Model-1'].rootAssembly
    faces = a.instances['Part-3-1'].faces
    face = faces.findAt((( 0,0,-(100 + D/2) ),))
    
    region = a.Set(faces=face, name='Set-8')
    mdb.models['Model-1'].DisplacementBC(name='BC-3', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=SET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
    
    
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    refPoints1 = r1.findAt((0.0,0.0,0.0))
    refPoints1 = (refPoints1,)
    region = a.Set(referencePoints=refPoints1, name='Set-3')
    mdb.models['Model-1'].VelocityBC(name='BC-2', createStepName='Initial', 
        region=region, v1=0.0, v2=0.0, v3=0.0, vr1=0.0, vr2=UNSET, vr3=0.0, 
        amplitude=UNSET, localCsys=None, distributionType=UNIFORM, fieldName='')

    mdb.models['Model-1'].SmoothStepAmplitude(name='Amp-1', timeSpan=STEP, data=((
        0.0, 0.0), (0.005, 1.0), (0.01, 1.0)))
    mdb.models['Model-1'].boundaryConditions['BC-2'].setValuesInStep(
        stepName='Step-1', vr2=Speed, amplitude='Amp-1')
        
    #yu ding yi chang
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    refPoints1 = r1.findAt((0.0,0.0,0.0))
    refPoints1 = (refPoints1,)
    region = a.Set(referencePoints=refPoints1, name='Set-4')
    mdb.models['Model-1'].Velocity(name='Predefined Field-1', region=region, 
        field='', distributionType=MAGNITUDE, velocity1=0.0, velocity2=0.0, 
        velocity3=0.0, omega=Speed, axisBegin=(0.0, 0.0, 0.0), axisEnd=(0.0, 1.0, 
        0.0))
    #add load
    a = mdb.models['Model-1'].rootAssembly
    r = a.referencePoints
    refPoints1 = r.findAt((0.0,0.0,0.0))
    refPoints1 = (refPoints1,)
    
    region = a.Set(referencePoints=refPoints1, name='Set-6')
    mdb.models['Model-1'].ConcentratedForce(name='Load-2', createStepName='Step-1', 
        region=region, cf3=-10000.0, amplitude='Amp-1', distributionType=UNIFORM, 
        field='', localCsys=None)
        
    #output setting
    a.ReferencePoint(point=(0.0,0.0,D/2))
    r = a.referencePoints
   
    rp2 = r.findAt((0.0,0.0,D/2))
    rp2 = (rp2,)
    
    region2=a.Set(referencePoints=rp2, name='m_Set-2')
    
    s1 = a.instances['Part-3-1'].faces
    side1Faces1 = s1.findAt(((0.0,0.0,-D/2),))
    outer_surface=a.Surface(side1Faces=side1Faces1, name='outer_surface')
    
    mdb.models['Model-1'].Coupling(name='Constraint-3', controlPoint=region2, 
        surface=outer_surface, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        localCsys=None,u1=OFF, u2=OFF, u3=OFF, ur1=OFF, ur2=OFF, ur3=OFF)
        
    mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
        'U', 'V', 'A'), region=MODEL, exteriorOnly=OFF, sectionPoints=DEFAULT, 
        rebar=EXCLUDE,numIntervals=numIntervals)
    regionDef=mdb.models['Model-1'].rootAssembly.sets['m_Set-2']
    mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(variables=(
        'U1', 'U2', 'U3', 'UR1', 'UR2', 'UR3', 'UT', 'UR', 'UCOM1', 'UCOM2', 
        'UCOM3', 'V1', 'V2', 'V3', 'VR1', 'VR2', 'VR3', 'VT', 'VR', 'VCOM1', 
        'VCOM2', 'VCOM3', 'A1', 'A2', 'A3', 'AR1', 'AR2', 'AR3', 'AT', 'AR', 
        'ACOM1', 'ACOM2', 'ACOM3', 'RBANG', 'RBROT'), region=regionDef, 
        sectionPoints=DEFAULT, rebar=EXCLUDE,numIntervals=numIntervals)
def Run(JobName,number_of_cpus):
    mdb.Job(name=JobName, model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, explicitPrecision=SINGLE, 
        nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
        contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
        resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, numDomains=number_of_cpus, 
        activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=number_of_cpus)
    mdb.jobs[JobName].submit(consistencyChecking=OFF)
if __name__ == '__main__':
    CreateBearingShell()
    CreateBearingBall()
    CreateSupport()
    AssignSections()
    GetMash(1.5,0.5,3.0)
    Assembly(9)
    StepSetting(0.01 , 200 , 314)
    Run('job-testscript',4)
    
