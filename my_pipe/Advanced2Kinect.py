'''
import sys
Dir = 'C:/Users/Administrator/Documents/DEV/MayaMiscTools/my_pipe'
if Dir not in sys.path:
    sys.path.append(Dir)

import Advanced2Kinect;reload(Advanced2Kinect)

Advanced2Kinect.create()
'''

import pymel.core as pm

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

    def create(self):
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

            # Aim Constraint
            pm.pointConstraint( tag, (kjot+'intermediate') )

            # Aim Constraint
            if not aim is None:
                aimv = (-1,0,0) if pm.getAttr(aim+'.tx') < 0 else aimv
                pm.aimConstraint( aim, (kjot+'intermediate'), aim=aimv,\
                          wut='objectrotation', u=(0,1,0), wu=(0,1,0), wuo=tag )

            pm.setAttr( (kjot+'.jointOrient'), pm.getAttr(kjot+'intermediate.jointOrient') )
            pm.connectAttr( (kjot+'intermediate.r'), (kjot+'.r') )
            pm.connectAttr( (kjot+'intermediate.t'), (kjot+'.t') )

        rootGrp = pm.group( 'SPINEBASE', n='K2Skeleton_Root', w=True, em=True)
        pm.parent( 'SPINEBASE', rootGrp )
        pm.setAttr( 'SPINEBASEintermediate.visibility', False )
        return

    def copySkinWeights(self, fromCluster=None, toCluster=None):
        # Get Skined Geometry
        fromSkin, toSkin = self.getSkins()

        # Get skinCluster
        if not fromCluster:
            fromClusters = pm.listConnections((fromSkin+'.inMesh'), type='skinCluster')
            if len(fromClusters) > 1:
                print "The source skined object have more than one skinCluster:"
                print fromClusters
                pm.error("The 'fromCluster' argument should be given.")
            fromCluster = fromClusters[0]

        if not toCluster:
            toClusters = pm.listConnections((toSkin+'.inMesh'), type='skinCluster')
            if len(toClusters) > 1:
                print "The destination skined object have more than one skinCluster:"
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
            #fromjoints = pm.skinPercent( fromCluster, fromvtx, q=True, t=None )
            #fromweights = pm.skinPercent( fromCluster, fromvtx, q=True, v=True )
            #fromdict = {x: y for x, y in zip(fromjoints, fromweights)}

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
            #break

    def getSkins(self):
        objs = pm.ls(sl=True)
        if len(objs) < 2:
            pm.error("Must one source skined object and one destination object selected.")
        return (objs[0], objs[1])

#------------------------------------------------------------------------------#

def create():
    global a2k
    if a2k is None:
        a2k = Advanced2Kinect()
    a2k.create()

def copySkinWeights():
    global a2k
    if a2k is None:
        a2k = Advanced2Kinect()
    a2k.copySkinWeights()
