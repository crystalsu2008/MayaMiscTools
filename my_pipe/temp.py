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
