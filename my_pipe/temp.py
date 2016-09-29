import pymel.core as pm

class ASSimplifyFit( object ):

    def doSimplify( self, parentNode ):
        for node in parentNode:
            childenNode = pm.listRelatives( node, c=True, typ='joint' )
            if len( childenNode ):
                self.doSimplify( childenNode )
            print node
            print pm.hasAttr( node, 'inbetweenJoints')
            print pm.hasAttr( node, 'inbetweenJoints')
            #pm.setAttr( (node+'.inbetweenJoints'), 0 )
        return

assf = ASSimplifyFit()
assf.doSimplify( pm.ls('FitSkeleton') )

#==============================================================================#
#------------------------------------------------------------------------------#

import pymel.core as pm
class Advance2Kinect2( object ):

    K2Joints=['SPINEBASE', 'SPINEMID', 'SPINESHOULDER', 'NECK', 'HEAD',\
              'SHOULDERLEFT', 'ELBOWLEFT', 'WRISTLEFT', 'HANDLEFT', 'HANDTIPLEFT',\
              'THUMBLEFT', 'SHOULDERRIGHT', 'ELBOWRIGHT', 'WRISTRIGHT', 'HANDRIGHT',\
              'HANDTIPRIGHT', 'THUMBRIGHT', 'HIPLEFT', 'KNEELEFT', 'ANKLELEFT',\
              'FOOTLEFT', 'HIPRIGHT', 'KNEERIGHT', 'ANKLERIGHT', 'FOOTRIGHT']

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
        aimer = []
        for kjot in self.k2map:
            tag = self.k2map[kjot][0]
            aimid = self.k2map[kjot][2]
            aim = None if aimid is None else self.k2map[aimid][0]
            aimv = (1,0,0)

            t = pm.xform( tag, q=True, ws=True, t=True )
            pm.select( cl=True )
            pm.joint( p=t, n=kjot )

            if not aim is None:
                aimv = (-1,0,0) if pm.getAttr(aim+'.tx') < 0 else aimv
                aimer.append(pm.aimConstraint( aim, kjot, aim=aimv, wut='objectrotation', u=(0,1,0), wu=(0,1,0), wuo=tag ))
        pm.delete( aimer )

        #
        # Make Joints Hierarchy
        #
        for kjot in self.k2map:
            parent = self.k2map[kjot][1]
            aimid = self.k2map[kjot][2]
            if not parent is None:
                pm.parent( kjot, self.k2map[kjot][1] )
                if aimid is None:
                    pm.setAttr( kjot+'.jointOrient', (0,0,0) )

            # Freeze Transformations
            pm.makeIdentity( kjot, a=True, jo=False, t=False, r=True, s=False, n=0, pn=True )

        #
        # Make Constraint
        #
        for kjot in self.k2map:
            tag = self.k2map[kjot][0]
            aimid = self.k2map[kjot][2]
            aim = None if aimid is None else self.k2map[aimid][0]
            aimv = (1,0,0)

            # Aim Constraint
            pm.pointConstraint( tag, kjot )

            # Aim Constraint
            if not aim is None:
                aimv = (-1,0,0) if pm.getAttr(aim+'.tx') < 0 else aimv
                pm.aimConstraint( aim, kjot, aim=aimv, wut='objectrotation', u=(0,1,0), wu=(0,1,0), wuo=tag )

        return

a2k = Advance2Kinect2()
a2k.create()
