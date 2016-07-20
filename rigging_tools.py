# This is a collection of few little tools for Rigging and Animation

from pymel.core import *
import maya.cmds as cmds
import maya.mel as mel

class RiggingTools(object):
    'This class include some little function for rigging and animation'
    label='Rigging Tools' #This label is used to embed in MayaMiscTools's Layout.

    def initUI(self, parentLayout=None):
        if parentLayout:
            setParent(parentLayout)
        else:
            self.win=window('RiggingTools',t=self.label,w=400)
        with frameLayout(bv=False,lv=False,label=self.label) as self.frame:
            with formLayout(numberOfDivisions=100) as self.form:
                with columnLayout(cat=('both', 0), rs=0, adj=True) as self.clumn:

                    with frameLayout(bv=True,lv=False,label='Joint Size',cll=True) as self.jointSizeFrame:
                        with columnLayout(cat=('both', 0), rs=0, adj=True) as self.jointSizeClumn:
                            self.jointSizeSlider=floatSliderGrp(cw=[1,60], label='Joint Size', field=True, minValue=0.01, maxValue=10.0, fieldMinValue=0.01, fieldMaxValue=100.0, precision=2, value=1)
                            self.jointSizeSlider.changeCommand(self.setJointSize)
                            self.jointSizeSlider.dragCommand(self.setJointSize)
                            with gridLayout(  cellWidthHeight=(30, 30),columnsResizable=True) as self.sizeButtongrid:
                                button(l='0.01', h=30, command='cmds.jointDisplayScale(0.01)')
                                button(l='0.25', h=30, command='cmds.jointDisplayScale(0.25)')
                                button(l='0.5', h=30, command='cmds.jointDisplayScale(0.5)')
                                button(l='0.75', h=30, command='cmds.jointDisplayScale(0.75)')
                                button(l='1', h=30, command='cmds.jointDisplayScale(1)')
                                for i in range(2,11):
                                    button(l=(i), h=30, command=('cmds.jointDisplayScale('+str(i)+')'))

                    with frameLayout(bv=True,lv=False,label='Joint Info',cll=True) as self.jointInfoFrame:
                        with columnLayout(cat=('both', 0), rs=0, adj=True) as self.jointInfoClumn:
                            with formLayout(numberOfDivisions=100) as self.showJointlabelForm:
                                self.showJointlabelButton=button(l='Show Joint\'s Label', h=30)
                                self.showJointlabelButton.setCommand(self.jointsLabelVisible)
                                SJLB=self.showJointlabelButton
                                self.hideJointlabelButton=button(l='Hide Joint\'s Label', h=30)
                                self.hideJointlabelButton.setCommand(self.jointslabelInvisible)
                                HJLB=self.hideJointlabelButton
                            formLayout(self.showJointlabelForm, e=True, af=[(SJLB,'top',0), (SJLB,'left',0), (HJLB,'right',0), (HJLB,'top',0)], ap=[(SJLB,'right',0,50), (HJLB,'left',0,50)])
                            self.setJointLabelToNameButton=button(l='Set Joint\'s Label to Joint\'s Name', h=30)
                            self.setJointLabelToNameButton.setCommand(self.setJointLabelToName)
                            #SJLN=self.setJointLabelToNameButton
                            with formLayout(numberOfDivisions=100) as self.showJointAxisForm:
                                self.showJointAxisButton=button(l='Show Joint\'s Local Rotation Axes', h=30)
                                self.showJointAxisButton.setCommand(self.jointsAxisVisible)
                                SJAB=self.showJointAxisButton
                                self.hideJointAxisButton=button(l='Hide Joint\'s Local Rotation Axes', h=30)
                                self.hideJointAxisButton.setCommand(self.jointsAxisInvisible)
                                HJAB=self.hideJointAxisButton
                            formLayout(self.showJointAxisForm, e=True, af=[(SJAB,'top',0), (SJAB,'left',0), (HJAB,'right',0), (HJAB,'top',0)], ap=[(SJAB,'right',0,50), (HJAB,'left',0,50)])

                    with frameLayout(bv=True,lv=False,label='Joint Lock and Hide',cll=True) as self.jointLockAndHideFrame:
                        with columnLayout(cat=('both', 0), rs=0, adj=True) as self.jointLockAndHideFrame:
                            self.lockAndHideCheck=checkBoxGrp(cw=[1,60], numberOfCheckBoxes=3, label='Attributes', labelArray3=['Translate', 'Rotate', 'Scale'])
                            with formLayout(numberOfDivisions=100) as self.lockAndHideForm:
                                self.unlockAndShowButton=button(l='Unlick and Show Joint\'s Transform Attributes', h=30)
                                self.unlockAndShowButton.setCommand(self.unlockAndShowJointsAttr)
                                USB=self.unlockAndShowButton
                                self.lockAndHideButton=button(l='Lock and Hide Joint\'s Transform Attributes', h=30)
                                self.lockAndHideButton.setCommand(self.lockAndHideJointsAttr)
                                LHB=self.lockAndHideButton
                            formLayout(self.lockAndHideForm, e=True, af=[(USB,'top',0), (USB,'left',0), (LHB,'right',0), (LHB,'top',0)], ap=[(USB,'right',0,50), (LHB,'left',0,50)])
                    self.selectRootJointsButton=button(l='Select Joints at The Root of Hierarchy', h=30)
                    self.selectRootJointsButton.setCommand(self.selectRootJoints)
                    self.selectEndJointsButton=button(l='Select Joints at The End of Hierarchy', h=30)
                    self.selectEndJointsButton.setCommand(self.selectEndJoints)
                    self.jointOrientZeroButton=button(l='Set Joint Orient to Zero', h=30)
                    self.jointOrientZeroButton.setCommand(self.setJointOrientZero)
                    self.kinect1to2Button=button(l='Convert Kinect1 System to Kinect2', h=30)
                    self.kinect1to2Button.setCommand(self.kinect1to2)

            formLayout(self.form, e=True, af=[(self.clumn,'top',0), (self.clumn,'left',0), (self.clumn,'right',0), (self.clumn,'bottom',0)])
        self.embed=self.frame #This attribute is used to embed in MayaMiscTools's Layout.

    def findRootJoint(self, jo):
        pa=listRelatives(jo, parent=True, typ='joint')
        return self.findRootJoint(jo=pa[0]) if len(pa) else jo

    #Select joints at the root of hierarchy.
    def selectRootJoints(self, val):
        seljoints=ls(sl=True, typ='joint')
        joints=[]
        if(len(seljoints)):
            [joints.append(self.findRootJoint(jo=x)) for x in seljoints if not x in joints]
            select(joints)
        else:
            select( [x for x in ls(typ='joint') if not len(listRelatives(x, parent=True, typ='joint'))] )

    #Select joints at the end of hierarchy.
    def selectEndJoints(self, val):
        select( [x for x in self.getJoints() if not len(listRelatives(x, ad=True, typ='joint'))] )

    #Set joint orient attribute to zero.
    def setJointOrientZero(self, val):
        [setAttr((x+'.jointOrient'), (0,0,0)) for x in self.getJoints(no_selected_return_all=False)]

    #Set joint's Transform Attributes Locked and Invisible.
    def lockAndHideJointsAttr(self, val):
        for x in self.getJoints():
            if self.lockAndHideCheck.getValue1():
                setAttr((x+'.tx'), lock=True, keyable=False)
                setAttr((x+'.ty'), lock=True, keyable=False)
                setAttr((x+'.tz'), lock=True, keyable=False)
            if self.lockAndHideCheck.getValue2():
                setAttr((x+'.rx'), lock=True, keyable=False)
                setAttr((x+'.ry'), lock=True, keyable=False)
                setAttr((x+'.rz'), lock=True, keyable=False)
            if self.lockAndHideCheck.getValue3():
                setAttr((x+'.sx'), lock=True, keyable=False)
                setAttr((x+'.sy'), lock=True, keyable=False)
                setAttr((x+'.sz'), lock=True, keyable=False)

    #Set joint's Transform Attributes Unlocked and Visible.
    def unlockAndShowJointsAttr(self, val):
        for x in self.getJoints():
            if self.lockAndHideCheck.getValue1():
                setAttr((x+'.tx'), lock=False, keyable=True)
                setAttr((x+'.ty'), lock=False, keyable=True)
                setAttr((x+'.tz'), lock=False, keyable=True)
            if self.lockAndHideCheck.getValue2():
                setAttr((x+'.rx'), lock=False, keyable=True)
                setAttr((x+'.ry'), lock=False, keyable=True)
                setAttr((x+'.rz'), lock=False, keyable=True)
            if self.lockAndHideCheck.getValue3():
                setAttr((x+'.sx'), lock=False, keyable=True)
                setAttr((x+'.sy'), lock=False, keyable=True)
                setAttr((x+'.sz'), lock=False, keyable=True)

    #Set joint's Local Rotation Axes visible.
    def jointsAxisInvisible(self, val):
        [setAttr((x+'.displayLocalAxis'), False) for x in self.getJoints()]

    #Set joint's Local Rotation Axes visible.
    def jointsAxisVisible(self, val):
        [setAttr((x+'.displayLocalAxis'), True) for x in self.getJoints()]

    def setJointSize(self, val):
        value=self.jointSizeSlider.getValue()
        jointDisplayScale(value)

    #Set Joint's Label to Joint's Name
    def setJointLabelToName(self, val):
        [setAttr((x+'.otherType'), x.nodeName(), type='string') for x in self.getJoints()]

    #Set joint's label visible.
    def jointsLabelVisible(self, val):
        for x in self.getJoints():
            setAttr((x+'.drawLabel'), True)
            if not getAttr((x+'.type')):
                setAttr((x+'.type'), 18)
                setAttr((x+'.otherType'), x.nodeName(), type='string')

    #Set joint's label invisible.
    def jointslabelInvisible(self, val):
        [setAttr((x+'.drawLabel'), False) for x in self.getJoints()]

    def getJoints(self, no_selected_return_all=True):
        seljoints=ls(sl=True, typ='joint')
        joints=seljoints[:]
        if(len(seljoints)):
            [joints.append(y) for x in seljoints for y in listRelatives(x, ad=True, typ='joint') if not y in joints]
        elif no_selected_return_all:
            joints=ls(typ='joint')
        return joints

    def openUI(self):
        if window('RiggingTools', q=True, ex=True):
            deleteUI('RiggingTools', wnd=True)
        self.initUI()
        showWindow(self.win)

    #Convert Kinect1 Skeleton System to Kinect2
    def kinect1to2(self, val):
        bindPoses=dagPose('HIP_CENTER', q=True, bindPose=True)
        # Rename kinect1 joints name to kinect2
        rename('HIP_CENTER', 'SPINEBASE')
        rename('SPINE', 'SPINEMID')
        rename('SHOULDER_CENTER', 'SPINESHOULDER')
        rename('SHOULDER_LEFT', 'SHOULDERLEFT')
        rename('ELBOW_LEFT', 'ELBOWLEFT')
        rename('WRIST_LEFT', 'WRISTLEFT')
        rename('HAND_LEFT', 'HANDLEFT')
        rename('SHOULDER_RIGHT', 'SHOULDERRIGHT')
        rename('ELBOW_RIGHT', 'ELBOWRIGHT')
        rename('WRIST_RIGHT', 'WRISTRIGHT')
        rename('HAND_RIGHT', 'HANDRIGHT')
        rename('HIP_LEFT', 'HIPLEFT')
        rename('KNEE_LEFT', 'KNEELEFT')
        rename('ANKLE_LEFT', 'ANKLELEFT')
        rename('FOOT_LEFT', 'FOOTLEFT')
        rename('HIP_RIGHT', 'HIPRIGHT')
        rename('KNEE_RIGHT', 'KNEERIGHT')
        rename('ANKLE_RIGHT', 'ANKLERIGHT')
        rename('FOOT_RIGHT', 'FOOTRIGHT')
        # Add NECK
        newJo=insertJoint('SPINESHOULDER')
        newJo=rename(newJo, 'NECK')
        pos=getAttr('HEAD.t')*.25
        joint(newJo, e=True, co=True, r=True, p=pos)
        # Add HANDTIPLEFT
        newJo=insertJoint('HANDLEFT')
        newJo=rename(newJo, 'HANDTIPLEFT')
        pos=getAttr('HANDLEFT.t')*.5
        joint('HANDLEFT', e=True, co=True, r=True, p=pos)
        joint(newJo, e=True, co=True, r=True, p=pos)
        # Add HANDTIPRIGHT
        newJo=insertJoint('HANDRIGHT')
        newJo=rename(newJo, 'HANDTIPRIGHT')
        pos=getAttr('HANDRIGHT.t')*.5
        joint('HANDRIGHT', e=True, co=True, r=True, p=pos)
        joint(newJo, e=True, co=True, r=True, p=pos)
        # Add THUMBLEFT
        newJo=joint('WRISTLEFT')
        newJo=rename(newJo, 'THUMBLEFT')
        pos=getAttr('HANDLEFT.t')
        newpos=mel.eval('rot(<<'+str(pos[0])+','+str(pos[1])+','+str(pos[2])+'>>,<<0,1,1>>,-.25*3.1415927)')
        joint(newJo, e=True, co=True, r=True, p=newpos)
        # Add THUMBRIGHT
        newJo=joint('WRISTRIGHT')
        newJo=rename(newJo, 'THUMBRIGHT')
        pos=getAttr('HANDRIGHT.t')
        newpos=mel.eval('rot(<<'+str(pos[0])+','+str(pos[1])+','+str(pos[2])+'>>,<<0,1,-1>>,.25*3.1415927)')
        joint(newJo, e=True, co=True, r=True, p=newpos)
        # Set bindPose
        dagPose('SPINEBASE', bindPose=True, addToPose=True, name=bindPoses[0])