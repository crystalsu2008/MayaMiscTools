'''
import sys
Dir = 'C:/Users/Administrator/Documents/DEV/MayaMiscTools/my_pipe'
if Dir not in sys.path:
    sys.path.append(Dir)

import fixAnimCurve180flip; reload(fixAnimCurve180flip)

fixAnimCurve180flip.fix()
'''

import pymel.core as pm
import maya.mel as mel

fixflip = None

class fixAnimCurve180flip(object):

    tol = 5
    minStep = 1

    def getSelectedChannels(self):
        mainChannelBox = mel.eval('global string $gChannelBoxName;\
                                   $temp=$gChannelBoxName;')
        attrs = pm.channelBox(mainChannelBox, q=True, sma=True)
        if not attrs:
            return None
        return attrs

    def fix(self):
        attrs = fixflip.getSelectedChannels()
        objs = pm.ls(sl=True)

        if not objs:
            pm.error("No Objects selected.")

        if not attrs:
            pm.error("No Attributes selected in the Channel Box.")

        for obj in objs:
            for attr in attrs:
                keyCount = pm.keyframe(obj, at=attr, q=True, keyframeCount=True)

                for idx in range(keyCount-1):
                    time = pm.keyframe(obj, at=attr, index=(idx), q=True)[0]
                    nextTime = pm.keyframe(obj, at=attr, index=(idx+1), q=True)[0]

                    if nextTime-time <= self.minStep:
                        value = pm.keyframe(obj ,at=attr, index=(idx), q=True, eval=True)[0]
                        nextValue = pm.keyframe(obj ,at=attr, index=(idx+1), q=True, eval=True)[0]

                        diff = nextValue-value
                        if 180-self.tol < abs(diff) < 180+self.tol:
                            move = 180 if diff < 0 else -180
                            pm.keyframe(obj, at=attr, r=True, e=True, index=(nextTime, keyCount-1), vc=move)

#------------------------------------------------------------------------------#

def fix():
    global fixflip
    if fixflip is None:
        fixflip = fixAnimCurve180flip()
    fixflip.fix()
