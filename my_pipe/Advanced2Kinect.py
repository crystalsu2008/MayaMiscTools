'''
import sys
Dir = 'C:/Users/Administrator/Documents/DEV/MayaMiscTools/my_pipe'
if Dir not in sys.path:
    sys.path.append(Dir)

import Advanced2Kinect;reload(Advanced2Kinect)

Advanced2Kinect.create()
'''

import pymel.core as pm
import maya.mel as mel

a2k = None

class Advanced2Kinect(object):

    k2map = {'SPINEBASE': ('Root_M', None, 'SPINEMID'),
             'SPINEMID': ('Spine1_M', 'SPINEBASE', 'SPINESHOULDER'),
              'SPINESHOULDER': ('Chest_M', 'SPINEMID', 'NECK'),
               'NECK': ('Neck_M', 'SPINESHOULDER', 'HEAD'),
                'HEAD': ('HeadEnd_M', 'NECK', None),
            'SHOULDERLEFT': ('Shoulder_L', 'SPINESHOULDER', 'ELBOWLEFT'),
             'ELBOWLEFT': ('Elbow_L', 'SHOULDERLEFT', 'WRISTLEFT'),
              'WRISTLEFT': ('Wrist_L', 'ELBOWLEFT', 'HANDLEFT'),
               'HANDLEFT': ('MiddleFinger1_L', 'WRISTLEFT', 'HANDTIPLEFT'),
                'HANDTIPLEFT': ('MiddleFinger4_L', 'HANDLEFT', None),
                 'THUMBLEFT': ('ThumbFinger4_L', 'WRISTLEFT', None),
            'SHOULDERRIGHT': ('Shoulder_R', 'SPINESHOULDER', 'ELBOWRIGHT'),
             'ELBOWRIGHT': ('Elbow_R', 'SHOULDERRIGHT', 'WRISTRIGHT'),
              'WRISTRIGHT': ('Wrist_R', 'ELBOWRIGHT', 'HANDRIGHT'),
               'HANDRIGHT': ('MiddleFinger1_R', 'WRISTRIGHT', 'HANDTIPRIGHT'),
                'HANDTIPRIGHT': ('MiddleFinger4_R', 'HANDRIGHT', None),
                 'THUMBRIGHT': ('ThumbFinger4_R', 'WRISTRIGHT', None),
            'HIPLEFT': ('Hip_L', 'SPINEBASE', 'KNEELEFT'),
             'KNEELEFT': ('Knee_L', 'HIPLEFT', 'ANKLELEFT'),
              'ANKLELEFT': ('Ankle_L', 'KNEELEFT', 'FOOTLEFT'),
               'FOOTLEFT': ('ToesEnd_L', 'ANKLELEFT', None),
            'HIPRIGHT': ('Hip_R', 'SPINEBASE', 'KNEERIGHT'),
             'KNEERIGHT': ('Knee_R', 'HIPRIGHT', 'ANKLERIGHT'),
              'ANKLERIGHT': ('Ankle_R', 'KNEERIGHT', 'FOOTRIGHT'),
               'FOOTRIGHT': ('ToesEnd_R', 'ANKLERIGHT', None)}

    k2wmap= {'SPINEBASE': ['Root_M'],
             'SPINEMID': ['Spine1_M'],
              'SPINESHOULDER': ['Chest_M', 'Scapula_L', 'Scapula_R'],
               'NECK': ['Neck_M', 'Head_M', 'HeadEnd_M',
                        'Eye_R', 'EyeEnd_R', 'Eye_L', 'EyeEnd_L',
                        'Jaw_M', 'JawEnd_M'],
                'HEAD': None,
            'SHOULDERLEFT': ['Shoulder_L'],
             'ELBOWLEFT': ['Elbow_L'],
              'WRISTLEFT': ['Wrist_L', 'Cup_L', 'ThumbFinger1_L'],
               'HANDLEFT': ['MiddleFinger1_L', 'MiddleFinger2_L', 'MiddleFinger3_L', 'MiddleFinger4_L',
                            'IndexFinger1_L', 'IndexFinger2_L', 'IndexFinger3_L', 'IndexFinger4_L',
                            'RingFinger1_L', 'RingFinger2_L', 'RingFinger3_L', 'RingFinger4_L',
                            'PinkyFinger1_L', 'PinkyFinger2_L', 'PinkyFinger3_L', 'PinkyFinger4_L'],
                'HANDTIPLEFT': None,
                 'THUMBLEFT': ['ThumbFinger2_L', 'ThumbFinger3_L', 'ThumbFinger4_L'],
            'SHOULDERRIGHT': ['Shoulder_R'],
             'ELBOWRIGHT': ['Elbow_R'],
              'WRISTRIGHT': ['Wrist_R', 'Cup_R', 'ThumbFinger1_R'],
               'HANDRIGHT': ['MiddleFinger1_R', 'MiddleFinger2_R', 'MiddleFinger3_R', 'MiddleFinger4_R',
                            'IndexFinger1_R', 'IndexFinger2_R', 'IndexFinger3_R', 'IndexFinger4_R',
                            'RingFinger1_R', 'RingFinger2_R', 'RingFinger3_R', 'RingFinger4_R',
                            'PinkyFinger1_R', 'PinkyFinger2_R', 'PinkyFinger3_R', 'PinkyFinger4_R'],
                'HANDTIPRIGHT': None,
                 'THUMBRIGHT': ['ThumbFinger2_R', 'ThumbFinger3_R', 'ThumbFinger4_R'],
            'HIPLEFT': ['Hip_L'],
             'KNEELEFT': ['Knee_L'],
              'ANKLELEFT': ['Ankle_L', 'Toes_L'],
               'FOOTLEFT': None,
            'HIPRIGHT': ['Hip_R'],
             'KNEERIGHT': ['Knee_R'],
              'ANKLERIGHT': ['Ankle_R', 'Toes_R'],
               'FOOTRIGHT': None}

    noneKeepKeywords =  ['Root', 'Spine', 'Chest', 'Neck', 'Head', 'Eye', 'Jaw',
                                 'Scapula', 'Shoulder', 'Elbow', 'Wrist', 'Cup',
      'MiddleFinger', 'ThumbFinger', 'IndexFinger', 'PinkyFinger', 'RingFinger',
                                                 'Hip', 'Knee', 'Ankle', 'Toes']

    asSkins, k2Skins = [None], [None]

    '''
    SmoothBindOptions = {'multipleBindPosesOpt': 1,
                        'bindMethod': 1,
                        'bindTo': 0,
                        'skinMethod': 1,
                        'removeUnusedInfluences': 0,
                        'colorizeSkeleton': 0,
                        'maxInfl': 3,
                        'normalizeWeights': 2,
                        'obeyMaxInfl': 0}
    '''

    def k2create(self):
        #
        # Create Kinect2 Joints
        #
        for kjot in self.k2map:
            tag = self.k2map[kjot][0]
            aimid = self.k2map[kjot][2]
            aim = None if aimid is None else self.k2map[aimid][0]
            aimv = (1,0,0)

            t = pm.xform( tag, q=True, ws=True, t=True )
            pm.select( cl=True )
            interJoint = pm.joint( p=t, n=(kjot+'intermediate') )

            if not aim is None:
                aimv = (-1,0,0) if pm.getAttr(aim+'.tx') < 0 else aimv
                aimer = pm.aimConstraint( aim, interJoint, aim=aimv, wuo=tag,\
                                   wut='objectrotation', u=(0,1,0), wu=(0,1,0) )
                pm.delete( aimer )
            pm.duplicate( interJoint, n=kjot )

        #
        # Make Joints Hierarchy
        #
        for kjot in self.k2map:
            parent = self.k2map[kjot][1]
            aimid = self.k2map[kjot][2]
            if not parent is None:
                pm.parent( (kjot+'intermediate'), (parent+'intermediate') )
                pm.parent( kjot, parent )
                if aimid is None:
                    pm.setAttr( kjot+'intermediate'+'.jointOrient', (0,0,0) )

            # Freeze Transformations
            pm.makeIdentity( (kjot+'intermediate'), a=True, jo=False, t=False,\
                             r=True, s=False, n=0, pn=True )

        #
        # Make Constraint
        #
        for kjot in self.k2map:
            parent = self.k2map[kjot][1]
            tag = self.k2map[kjot][0]
            aimid = self.k2map[kjot][2]
            aim = None if aimid is None else self.k2map[aimid][0]
            aimv = (1,0,0)

            # Point Constraint
            pm.pointConstraint( tag, (kjot+'intermediate') )

            # Aim Constraint
            if not aim is None:
                aimv = (-1,0,0) if pm.getAttr(aim+'.tx') < 0 else aimv
                pm.aimConstraint( aim, (kjot+'intermediate'), aim=aimv,\
                          wut='objectrotation', u=(0,1,0), wu=(0,1,0), wuo=tag )

            pm.setAttr( (kjot+'.jointOrient'), pm.getAttr(kjot+'intermediate.jointOrient') )
            pm.connectAttr( (kjot+'intermediate.r'), (kjot+'.r') )
            pm.connectAttr( (kjot+'intermediate.t'), (kjot+'.t') )

#------------------------------------------------------------------------------#

        #
        # Create None Kinect2 Joints
        #
        # Get (AdvancedSkeleton: Kinect2) joint dict.
        as_map_k2={}
        for k2jo, asjos in self.k2wmap.iteritems():
            if asjos:
                for asjo in asjos:
                    as_map_k2[asjo]=k2jo
        #for x, y in as_map_k2.iteritems():
        #    print x,y

        # Finding the keepJoints.
        keepJoints = {}
        for joint in pm.listRelatives('DeformationSystem', ad=True, typ='joint'):
            keepJoint=True
            for keyword in self.noneKeepKeywords:
                if keyword in str(joint):
                    keepJoint=False
                    break

            if keepJoint:
                jointParent = pm.listRelatives(joint, p=True, typ='joint')[0]
                keepJoints[joint] = jointParent

        # Create None Kinect2 joints and intermediate joints.
        interJoints={}
        k2keepJoints={}
        for kepJot, kepJotParent in keepJoints.iteritems():
            t = pm.xform( kepJot, q=True, ws=True, t=True )
            pm.select( cl=True )
            intJot = pm.joint( p=t, n=('k2'+kepJot+'intermediate') )
            k2kepJot=pm.duplicate( intJot, n=('k2'+kepJot) )[0]
            # Get the correct parent.
            if as_map_k2.has_key(str(kepJotParent)):
                interJoints[intJot] = (as_map_k2[str(kepJotParent)]+'intermediate', kepJot)
                k2keepJoints[k2kepJot] = (as_map_k2[str(kepJotParent)], intJot)
            else:
                interJoints[intJot] = ('k2'+kepJotParent+'intermediate', kepJot)
                k2keepJoints[k2kepJot] = ('k2'+kepJotParent, intJot)

        #
        # Make Joints Hierarchy
        #
        for intJot, intJotInfo in interJoints.iteritems():
            pm.parent( intJot, intJotInfo[0] )
            pm.parentConstraint( intJotInfo[1], intJot )
        for k2kepJot, k2kepJotInfo in k2keepJoints.iteritems():
            pm.parent( k2kepJot, k2kepJotInfo[0] )
            pm.setAttr( (k2kepJot+'.jointOrient'), pm.getAttr(k2kepJotInfo[1]+'.jointOrient') )
            pm.connectAttr( (k2kepJotInfo[1]+'.r'), (k2kepJot+'.r') )
            pm.connectAttr( (k2kepJotInfo[1]+'.t'), (k2kepJot+'.t') )

#------------------------------------------------------------------------------#

        # Create 'Kinect2' joint root curve handle.
        xpos = pm.xform('HANDTIPLEFT', q=True, t=True, ws=True)
        ypos = pm.xform('HEAD', q=True, t=True, ws=True)
        zpos = pm.xform('SPINEBASE', q=True, t=True, ws=True)
        textCurveGrp = pm.textCurves( f='Courier', t='Kinect2', ch=False)
        bbox = pm.exactWorldBoundingBox(textCurveGrp)
        pm.xform(textCurveGrp, t=(xpos[0], ypos[1], zpos[2]), ro=(0,0,-90),\
                      s=(ypos[1]/3/bbox[3],ypos[1]/3/bbox[3],ypos[1]/3/bbox[3]))
        rootCurvesShape = pm.listRelatives(textCurveGrp, ad=True, s=True)
        rootCurves = pm.parent(rootCurvesShape, w=True)
        pm.makeIdentity(rootCurves, apply=True, t=1, r=1, s=1, n=0, pn=1)

        # Create 'Kinect2' joint root.
        rootGrp = pm.group( 'SPINEBASE', n='K2_Skeleton', w=True, em=True)
        pm.parent( rootCurvesShape, rootGrp, s=True, add=True)
        pm.delete( textCurveGrp, rootCurves )
        pm.parent( 'SPINEBASE', rootGrp )

        # Move intermediate joint to Advanced Skeleton Group.
        asGroup = pm.listRelatives(pm.listRelatives(pm.ls('MainShape', typ='nurbsCurve'), p=True), p=True)
        pm.parent( 'SPINEBASEintermediate', asGroup)
        pm.setAttr( 'SPINEBASEintermediate.visibility', False )
        return

    def copySkinWeights(self):
        if not self.asSkins[0] or not self.k2Skins[0]:
            pm.error("At least given a source skinned object and a destination object.")
        else:
            for fromSkin, toSkin in zip(self.asSkins, self.k2Skins):
                pm.select(fromSkin, toSkin, replace=True)
                pm.copySkinWeights(nm=True, sa='closestPoint', ia='closestJoint', nr=True)
                #pm.copySkinWeights(ss=fromSkin, ds=toSkin, nm=True, sa='closestPoint', ia='closestJoint', nr=True)

    def duplicateSkinObjects(self):
        fromClusters=[]
        for joint in pm.listRelatives('DeformationSystem', ad=True, typ='joint'):
            clusters = pm.listConnections(joint+'.worldMatrix', type='skinCluster')
            for cluster in clusters:
                if not cluster in fromClusters:
                    fromClusters.append(cluster)
        formSkins=[]
        for cluster in fromClusters:
            skinobjs = pm.listConnections(cluster+'.outputGeometry', type='mesh')
            formSkins.extend(skinobjs)
        toSkins=[]
        for obj in formSkins:
            toSkins.extend(pm.duplicate( obj, n='k2'+obj, rr=True ))
            self.removeInvalidIntermediate(obj)
            # Bind kinect2 skins
            pm.skinCluster('SPINEBASE', toSkins[-1], nw=1, mi=3, dr=4.0)

        geogrp = pm.group( n='K2_Geometry', em=True, w=True )
        pm.parent(toSkins, geogrp)

        # Bind kinect2 skins
        #
        # Set SmoothBind Options
        '''
        for option, var in self.SmoothBindOptions.iteritems():
            pm.optionVar[option]=var
        pm.select('SPINEBASE', toSkins, replace=True)
        # Smooth bind skins.
        pm.runtime.SmoothBindSkin()
        '''


        self.asSkins=formSkins
        self.k2Skins=toSkins

    def removeInvalidIntermediate(self, objs):
        allShapes=pm.listRelatives(objs, c=True, s=True)
        notIntermediateShapes=pm.listRelatives(objs,c=True, s=True, ni=True)
        intermediateShapes=list(set(allShapes)-set(notIntermediateShapes))
        for x in intermediateShapes:
            if not len(pm.listConnections(x)):
                pm.delete(x)

#-----------------------------------Invalid------------------------------------#

    def Invalid_getSkins_MyTry(self):
        'MyTry, Useless'
        objs = pm.ls(sl=True)
        if len(objs) < 2:
            pm.error("Must one source skinned object and one destination object selected.")
        return (objs[0], objs[1])

    def Invalid_copyK2SkinWeights(self, fromSkin=None, fromCluster=None, toSkin=None, toCluster=None):
        'MyTry, Useless'
        # Get skinned Geometry
        if not fromSkin or not toSkin:
            fromSkin, toSkin = self.getSkins()

        # Get skinCluster
        if not fromCluster:
            fromClusters = pm.listConnections((fromSkin+'.inMesh'), type='skinCluster')
            if len(fromClusters) > 1:
                print "The source skinned object have more than one skinCluster:"
                print fromClusters
                pm.error("The 'fromCluster' argument should be given.")
            fromCluster = fromClusters[0]

        if not toCluster:
            toClusters = pm.listConnections((toSkin+'.inMesh'), type='skinCluster')
            if len(toClusters) > 1:
                print "The destination skinned object have more than one skinCluster:"
                print fromClusters
                pm.error("The 'toCluster' argument should be given.")
            toCluster = toClusters[0]

        # Get Source and Destination geometry's Vertexs
        fromvtxs = pm.ls(pm.polyListComponentConversion( fromSkin, tv=True, internal=True ), fl=True)
        tovtxs = pm.ls(pm.polyListComponentConversion( toSkin, tv=True, internal=True ), fl=True)

        # Copy Weights
        #
        # Looping all Vertexs
        for fromvtx, tovtx in zip(fromvtxs, tovtxs):
            # Get current Vertexs Kinect2 joint's weight list.
            k2weightsList = []
            for k2jo, asjos in self.k2wmap.iteritems():
                if not asjos:
                    # If there is no corresponding joints, continue.
                    continue
                else:
                    # Sum all corresponding AdvancedSkeleton joint's weights as Kinect2 joint's weight.
                    k2weight = 0.0
                    for asjo in asjos:
                        try:
                            asweight = pm.skinPercent(fromCluster, fromvtx, t=asjo, q=True)
                        except:
                            asweight = 0
                        k2weight += asweight
                    if not k2weight==0:
                        # Append Kinect2 joint and weight to list.
                        k2weight = 1 if k2weight > 1 else k2weight
                        k2weightsList.append((k2jo, k2weight))

            pm.skinPercent( toCluster, tovtx, tv=k2weightsList )
            print fromvtx, tovtx

#------------------------------------------------------------------------------#

def create():
    global a2k
    if a2k is None:
        a2k = Advanced2Kinect()
    a2k.k2create()
    a2k.duplicateSkinObjects()
    a2k.copySkinWeights()

def copySkinWeights():
    global a2k
    if a2k is None:
        a2k = Advanced2Kinect()
    a2k.copyK2SkinWeights()
