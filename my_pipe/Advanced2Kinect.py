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

class Advanced2Kinect( object ):

    k2map= {'SPINEBASE': ('Root_M', None, 'SPINEMID'),
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

    def create( self ):
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

    def copySkinWeights( self ):
        pass

#------------------------------------------------------------------------------#

def create():
    global a2k
    if a2k is None:
        a2k = Advanced2Kinect()
    a2k.create()
