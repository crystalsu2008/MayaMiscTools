# This is a collection of few little tools for Rigging and Animation

from pymel.core import *
import maya.cmds as cmds
import maya.mel as mel
import random

class RiggingTools(object):
    'This class include some little function for rigging and animation'
    label='Rigging Tools' #This label is used to embed in MayaMiscTools's Layout.

    list_poses=[]
    list_skins=[]
    list_geometries=[]

    def initUI(self, parentLayout=None):
        if parentLayout:
            setParent(parentLayout)
        else:
            self.win=window('RiggingTools',t=self.label,w=400)
        with frameLayout(bv=False,lv=False,label=self.label) as self.frame:
            with formLayout(numberOfDivisions=100) as self.form:
                with columnLayout(cat=('both', 0), rs=0, adj=True) as self.clumn:

                    with frameLayout(bv=True,lv=True,label='Joint Size & Color',cll=False, bgc=[0.0,0.35,0.0], fn='smallObliqueLabelFont') as self.jointSizeFrame:
                        with columnLayout(cat=('both', 0), rs=0, adj=True) as self.jointSizeClumn:
                            self.jointSizeSlider=floatSliderGrp(cw=[1,60], label='Joint Size', field=True, minValue=0.01, maxValue=10.0, fieldMinValue=0.01, fieldMaxValue=100.0, precision=2, value=1)
                            self.jointSizeSlider.changeCommand(self.setJointSize)
                            self.jointSizeSlider.dragCommand(self.setJointSize)
                            with gridLayout(cellWidthHeight=(30, 30), columnsResizable=True) as self.sizeButtongrid:
                                button(l='0.01', h=30, command='cmds.jointDisplayScale(0.01)')
                                button(l='0.25', h=30, command='cmds.jointDisplayScale(0.25)')
                                button(l='0.5', h=30, command='cmds.jointDisplayScale(0.5)')
                                button(l='0.75', h=30, command='cmds.jointDisplayScale(0.75)')
                                button(l='1', h=30, command='cmds.jointDisplayScale(1)')
                                for i in range(2,11):
                                    button(l=(i), h=30, command=('cmds.jointDisplayScale('+str(i)+')'))
                        with columnLayout(cat=('both', 0), rs=0, adj=True) as self.jointsColorClumn:
                            with formLayout(numberOfDivisions=100) as self.jointsColorForm:
                                self.jointsColorSlider=colorSliderGrp( label='Joint Color', rgb=(0.188, 0.404, 0.631), cw=(1, 70) )
                                JCS=self.jointsColorSlider
                                self.setSelectedJointColorButton=button(l='Selected', ann="Set selected joints color.")
                                self.setSelectedJointColorButton.setCommand(self.setSelectedJointColor)
                                SSJCB=self.setSelectedJointColorButton
                                self.setHierarchyJointColorButton=button(l='Hierarchy', ann="Set hierarchy joints color.")
                                self.setHierarchyJointColorButton.setCommand(self.setHierarchyJointColor)
                                SHJCB=self.setHierarchyJointColorButton
                            formLayout(self.jointsColorForm, e=True, af=[(JCS,'top',0), (JCS,'left',0), (SSJCB,'top',0), (SHJCB,'top',0), (SHJCB,'right',0)], ap=[(JCS,'right',0,60), (SSJCB,'left',0,60), (SSJCB,'right',0,80), (SHJCB,'left',0,80)])
                            self.randomColorCheck=checkBoxGrp(cw=[1,200], numberOfCheckBoxes=3, label='Select Color Elements to Random Set', labelArray3=['H', 'S', 'V'], v1=True)
                            with formLayout(numberOfDivisions=100) as self.randomColorForm:
                                self.randomJointColorButton=button(l='Random Color', ann='Based on the above parameters to random set joint\'s color.', h=30)
                                self.randomJointColorButton.setCommand(self.randomJointColor)
                                RJCB=self.randomJointColorButton
                                self.cleanJointColorButton=button(l='Clean Color', ann='Remove joint\'s color.', h=30)
                                self.cleanJointColorButton.setCommand(self.cleanJointColor)
                                CJCB=self.cleanJointColorButton
                            formLayout(self.randomColorForm, e=True, af=[(RJCB,'top',0), (RJCB,'left',0), (CJCB,'right',0), (CJCB,'top',0)], ap=[(RJCB,'right',0,50), (CJCB,'left',0,50)])

                    with frameLayout(bv=True,lv=True,label='Joint Info',cll=False, bgc=[0.0,0.35,0.0], fn='smallObliqueLabelFont') as self.jointInfoFrame:
                        with columnLayout(cat=('both', 0), rs=0, adj=True) as self.jointInfoClumn:
                            self.setJointLabelToNameButton=button(l='Label = Name', ann='Set Joint\'s Label to Joint\'s Name', h=30)
                            self.setJointLabelToNameButton.setCommand(self.setJointLabelToName)
                            #SJLN=self.setJointLabelToNameButton
                            with formLayout(numberOfDivisions=100) as self.showJointlabelForm:
                                self.showJointlabelButton=button(l='Label [o]', ann='Show Joint\'s Label', h=30)
                                self.showJointlabelButton.setCommand(self.jointsLabelVisible)
                                SJLB=self.showJointlabelButton
                                self.hideJointlabelButton=button(l='Label [-]', ann='Hide Joint\'s Label', h=30)
                                self.hideJointlabelButton.setCommand(self.jointslabelInvisible)
                                HJLB=self.hideJointlabelButton
                            formLayout(self.showJointlabelForm, e=True, af=[(SJLB,'top',0), (SJLB,'left',0), (HJLB,'right',0), (HJLB,'top',0)], ap=[(SJLB,'right',0,50), (HJLB,'left',0,50)])
                            with formLayout(numberOfDivisions=100) as self.showJointAxisForm:
                                self.showJointAxisButton=button(l='Axis [o]', ann='Show Joint\'s Local Rotation Axes', h=30)
                                self.showJointAxisButton.setCommand(self.jointsAxisVisible)
                                SJAB=self.showJointAxisButton
                                self.hideJointAxisButton=button(l='Axis [-]', ann='Hide Joint\'s Local Rotation Axes', h=30)
                                self.hideJointAxisButton.setCommand(self.jointsAxisInvisible)
                                HJAB=self.hideJointAxisButton
                            formLayout(self.showJointAxisForm, e=True, af=[(SJAB,'top',0), (SJAB,'left',0), (HJAB,'right',0), (HJAB,'top',0)], ap=[(SJAB,'right',0,50), (HJAB,'left',0,50)])

                    with frameLayout(bv=True,lv=True,label='Bind Pose',cll=False, bgc=[0.0,0.35,0.0], fn='smallObliqueLabelFont') as self.bindPoseFrame:
                        with columnLayout(cat=('both', 0), rs=0, adj=True) as self.bindPoseClumn:
                            self.queryPosesButton=button(l='Query Poses', ann='Finding out the poses connect to the joints.', h=30)
                            self.queryPosesButton.setCommand(self.queryPoses)
                            with paneLayout(configuration='vertical3', w=330) as self.bindPosePane:
                                self.posesList = textScrollList(ams=True)
                                self.posesList.selectCommand(self.poseSelectCmd)
                                self.posesList.doubleClickCommand(self.poseDoubleClickCmd)
                                self.posesList.deleteKeyCommand(self.poseDeleteCmd)
                                self.skinsList = textScrollList(ams=True)
                                self.skinsList.selectCommand(self.skinSelectCmd)
                                self.skinsList.doubleClickCommand(self.skinDoubleClickCmd)
                                self.geometriesList = textScrollList(ams=True)
                                self.geometriesList.selectCommand(self.geometrySelectCmd)

                            with formLayout(numberOfDivisions=100) as self.scopeOfApplyForm:
                                self.scopeOfApplyLable=text( label='Scope of Apply' )
                                SAL=self.scopeOfApplyLable
                                self.scopeOfApplyCollection = radioCollection()
                                self.allHierarchy = radioButton('SOA_allHierarchy', label='All Hierarchy')
                                SAAH=self.allHierarchy
                                self.childernHierarchy = radioButton('SOA_childernHierarchy', label='Childern Hierarchy', sl=True)
                                SACH=self.childernHierarchy
                                self.onlySelected = radioButton('SOA_onlySelected', label='Only the Selected')
                                SAOS=self.onlySelected
                            formLayout(self.scopeOfApplyForm, e=True, af=[(SAL,'top',0), (SAL,'left',0), (SAAH,'top',0), (SACH,'top',0), (SAOS,'top',0), (SAOS,'right',0)],\
                                                                      ap=[(SAL,'right',0,25), (SAAH,'left',0,25), (SAAH,'right',0,50), (SACH,'left',0,50), (SAAH,'right',0,75), (SAOS,'left',0,75)])

                            with formLayout(numberOfDivisions=90) as self.gotoNewPoseForm:
                                self.gotoSelectedPoseButton=button(l='Go to Pose', ann='Go to selected pose.', h=30)
                                self.gotoSelectedPoseButton.setCommand(self.gotoSelectedPose)
                                GSPB=self.gotoSelectedPoseButton
                                self.newPoseButton=button(l='New Pose', ann='Create a new pose with selected objects.', h=30)
                                self.newPoseButton.setCommand(self.newPose)
                                NPB=self.newPoseButton
                                self.switchBindPosesButton=button(l='Switch BindPoses', ann='Switch selected poses to bindPose or non-bindPose.', h=30)
                                self.switchBindPosesButton.setCommand(self.switchBindPoses)
                                SBPB=self.switchBindPosesButton
                            formLayout(self.gotoNewPoseForm, e=True, af=[(GSPB,'top',0), (GSPB,'left',0), (NPB,'top',0), (SBPB,'top',0), (SBPB,'right',0)],\
                                                                     ap=[(GSPB,'right',0,30), (NPB,'left',0,30), (NPB,'right',0,60), (SBPB,'left',0,60)])
                            with formLayout(numberOfDivisions=100) as self.addRemoveToPoseForm:
                                self.addToPoseButton=button(l='Add to Pose', ann='Adding the selected items to the dagPose.', h=30)
                                self.addToPoseButton.setCommand(self.addToPose)
                                ATPB=self.addToPoseButton
                                self.removeFromPoseButton=button(l='Remove from Pose', ann='Remove the selected joints from the specified pose.', h=30)
                                self.removeFromPoseButton.setCommand(self.removeFromPose)
                                RFPB=self.removeFromPoseButton
                            formLayout(self.addRemoveToPoseForm, e=True, af=[(ATPB,'top',0), (ATPB,'left',0), (RFPB,'right',0), (RFPB,'top',0)], ap=[(ATPB,'right',0,50), (RFPB,'left',0,50)])
                            with formLayout(numberOfDivisions=100) as self.resetPoseForm:
                                self.resetPoseButton=button(l='Reset Pose', ann='Set current pose to selected pose.', h=30)
                                self.resetPoseButton.setCommand(self.resetPose)
                                REPB=self.resetPoseButton
                                self.rebindSkinButton=button(l='Rebind Skin', ann='Rebind selected skin geometry at current pose, and keep the skin weights.', h=30)
                                self.rebindSkinButton.setCommand(self.rebindSkin)
                                RBSB=self.rebindSkinButton
                            formLayout(self.resetPoseForm, e=True, af=[(REPB,'top',0), (REPB,'left',0), (RBSB,'right',0), (RBSB,'top',0)], ap=[(REPB,'right',0,50), (RBSB,'left',0,50)])

                    with frameLayout(bv=True,lv=True,label='Joint Lock and Hide',cll=False, bgc=[0.0,0.35,0.0], fn='smallObliqueLabelFont') as self.jointLockAndHideFrame:
                        with columnLayout(cat=('both', 0), rs=0, adj=True) as self.jointLockAndHideFrame:
                            self.lockAndHideCheck=checkBoxGrp(cw=[1,150], numberOfCheckBoxes=3, label='Select Attributes to Apply', labelArray3=['Translate', 'Rotate', 'Scale'], v1=True, v2=True, v3=True)
                            with formLayout(numberOfDivisions=100) as self.lockAndHideForm:
                                self.unlockAndShowButton=button(l='Unlock && Show', ann='Unlock and Show Joint\'s Transform Attributes', h=30)
                                self.unlockAndShowButton.setCommand(self.unlockAndShowJointsAttr)
                                USB=self.unlockAndShowButton
                                self.lockAndHideButton=button(l='Lock && Hide', ann='Lock and Hide Joint\'s Transform Attributes', h=30)
                                self.lockAndHideButton.setCommand(self.lockAndHideJointsAttr)
                                LHB=self.lockAndHideButton
                            formLayout(self.lockAndHideForm, e=True, af=[(USB,'top',0), (USB,'left',0), (LHB,'right',0), (LHB,'top',0)], ap=[(USB,'right',0,50), (LHB,'left',0,50)])

                    with frameLayout(bv=True,lv=True,label='Pick Out Joints',cll=False, bgc=[0.0,0.35,0.0], fn='smallObliqueLabelFont') as self.pickOutJointsFrame:
                        with columnLayout(cat=('both', 0), rs=0, adj=True) as self.pickOutJointsClumn:
                            with formLayout(numberOfDivisions=100) as self.pickOutJointsForm:
                                self.selectRootJointsButton=button(l='Root Joints', ann='Select Joints at The Root of Hierarchy', h=30)
                                self.selectRootJointsButton.setCommand(self.selectRootJoints)
                                SRJB=self.selectRootJointsButton
                                self.selectEndJointsButton=button(l='End Joints', ann='Select Joints at The End of Hierarchy', h=30)
                                self.selectEndJointsButton.setCommand(self.selectEndJoints)
                                SEJB=self.selectEndJointsButton
                            formLayout(self.pickOutJointsForm, e=True, af=[(SRJB,'top',0), (SRJB,'left',0), (SEJB,'right',0), (SEJB,'top',0)], ap=[(SRJB,'right',0,50), (SEJB,'left',0,50)])

                    with frameLayout(bv=True,lv=True,label='Other Rigging Tools',cll=False, bgc=[0.0,0.35,0.0], fn='smallObliqueLabelFont') as self.otherRigToolFrame:
                        with gridLayout(cellWidthHeight=(110, 30), columnsResizable=True) as self.otherRigToolGrid:
                            self.jointOrientZeroButton=button(l='Orient = 0', ann='Set Joint Orient to Zero')
                            self.jointOrientZeroButton.setCommand(self.setJointOrientZero)
                            self.kinect1to2Button=button(l='Kinect 1 -> 2', ann='Convert Kinect1 System to Kinect2')
                            self.kinect1to2Button.setCommand(self.kinect1to2)
                            self.removeInvalidIntermediateButton=button(l='[X] Bad Intermediate', ann='Remove the Invalid Intermediate nodes under the selected objects.')
                            self.removeInvalidIntermediateButton.setCommand(self.removeInvalidIntermediate)
                            self.showIntermediateButton=button(l='[o] Intermediate', ann='Show the Intermediate nodes under the selected objects.')
                            self.showIntermediateButton.setCommand(self.showIntermediate)
                            self.swithIntermediateButton=button(l='-><- Intermediate', ann='Quick switch between the Final objects and the Origin Intermediate objects. It\'s very useful to do some modify before the Construction History.')
                            self.swithIntermediateButton.setCommand(self.swithIntermediate)

            formLayout(self.form, e=True, af=[(self.clumn,'top',0), (self.clumn,'left',0), (self.clumn,'right',0), (self.clumn,'bottom',0)])
        self.embed=self.frame #This attribute is used to embed in MayaMiscTools's Layout.

    def getHierarchy(self, objs):
        #selObjs=ls(sl=True, objectsOnly=True, typ='transform')
        hierObjs=objs[:]
        if(len(objs)):
            [hierObjs.append(y) for x in objs for y in listRelatives(x, ad=True, typ='transform') if not y in hierObjs]
        return hierObjs

    def getItemsForApply(self, objType=''):
        items=ls(sl=True, objectsOnly=True, typ=objType)
        scope=self.scopeOfApplyCollection.getSelect()
        if scope=='SOA_allHierarchy':
            items=self.getHierarchy( self.findAllRoots(objs=items, objtype=objType, no_selected_return_all=False) )
        elif scope=='SOA_childernHierarchy':
            items=self.getHierarchy(items)
        return items

    # Finding out given object's root.
    def findRoot(self, obj, objtype=''):
        pa=listRelatives(obj, parent=True, typ=objtype)
        return self.findRoot(obj=pa[0], objtype=objtype) if len(pa) else obj

    # If there have some selected objects then return all selected object's roots otherwise return all roots.
    def findAllRoots(self, objs, objtype='', no_selected_return_all=True):
        roots=[]
        if(len(objs)):
            [roots.append(self.findRoot(obj=x, objtype=objtype)) for x in objs if not x in roots]
        elif no_selected_return_all:
            roots=[x for x in ls(objectsOnly=True, typ=objtype) if not len(listRelatives(x, parent=True, typ=objtype))]
        return roots

    def rebindSkin(self, val):
        pass

    def addToPose(self, val):
        objs=self.getItemsForApply(objType='transform')
        if not len(objs):
            print 'Hierarchy Objects must be selected.'
        else:
            select(objs)
            [dagPose(name=self.list_poses[i-1], addToPose=True, selection=True) for i in self.posesList.getSelectIndexedItem()]

    def removeFromPose(self, val):
        objs=self.getItemsForApply(objType='transform')
        if not len(objs):
            print 'Hierarchy Objects must be selected.'
        else:
            [dagPose(objs, name=self.list_poses[i-1], remove=True) for i in self.posesList.getSelectIndexedItem()]

    def newPose(self, val):
        self.queryPoses(val)
        nodes=self.getItemsForApply(objType='transform')
        if not len(nodes):
            print 'Hierarchy Objects must be selected.'
        else:
            newPose=dagPose(nodes, save=True, selection=True)
            self.list_poses.append(newPose)
            bp='<BP>' if getAttr(newPose+'.bindPose') else ''
            skin='<Skin>' if len(listConnections((newPose+'.message'), type='skinCluster')) else ''
            self.posesList.append(newPose+bp+skin)
            self.posesList.setSelectIndexedItem(len(self.list_poses))
            self.poseSelectCmd()

    def switchBindPoses(self, val):
        ids=[i for i in self.posesList.getSelectIndexedItem()]
        poses=[self.list_poses[i-1] for i in ids]
        isbp=True
        for x in poses:
            isbp=not getAttr(x+'.bindPose')
            setAttr((x+'.bindPose'), isbp)
        self.queryPoses(val)
        self.posesList.setSelectIndexedItem(ids)
        self.poseSelectCmd()

    def resetPose(self, val):
        poses=[self.list_poses[i-1] for i in self.posesList.getSelectIndexedItem()]
        for x in poses:
            dagPose(dagPose(x, query=True, members=True), x, reset=True)

    def gotoSelectedPose(self, val):
        [dagPose(self.list_poses[i-1], restore=True) for i in self.posesList.getSelectIndexedItem()]
        '''
        # Go to bindPose.
        cmds.dagPose([''], restore=True, bindPose=True)
        # Reset the pose on the selected joints. If you are resetting pose data for a bindPose, take care.
        cmds.dagPose([''], reset=True, bindPose=True)
        # Finding out bindPose's name.
        cmds.dagPose([''], query=True, bindPose=True)
        # Adding the selected items to the dagPose.
        cmds.dagPose([''],addToPose=True, name='bindPose3')
        '''

    def poseSelectCmd(self):
        # Clean all self list.
        self.list_skins=[]
        self.skinsList.removeAll()
        self.list_geometries=[]
        self.geometriesList.removeAll()
        poseMembers=[]
        members=[]
        # Get selected poses.
        selectedItemPoses=[self.list_poses[i-1] for i in self.posesList.getSelectIndexedItem()]
        # Get Skinclusters and poses's members.
        for x in selectedItemPoses:
            self.list_skins.extend(listConnections((x+'.message'), type='skinCluster'))
            members=dagPose(x, query=True, members=True)
            if members:
                poseMembers.extend(members)
        # Refresh skinList.
        [self.skinsList.append(x) for x in self.list_skins]
        select(poseMembers)

    def poseDoubleClickCmd(self):
        selectedItemPoses=[self.list_poses[i-1] for i in self.posesList.getSelectIndexedItem()]
        select(selectedItemPoses)

    def poseDeleteCmd(self):
        selectedItemPoses=[self.list_poses[i-1] for i in self.posesList.getSelectIndexedItem()]
        delete(selectedItemPoses)
        self.queryPoses(False)

    def skinSelectCmd(self):
        self.list_geometries=[]
        self.geometriesList.removeAll()
        selectedItemSkins=[]
        [selectedItemSkins.append(self.list_skins[i-1]) for i in self.skinsList.getSelectIndexedItem()]
        [self.list_geometries.extend(listConnections((x+'.outputGeometry'))) for x in selectedItemSkins]
        [self.geometriesList.append(x) for x in self.list_geometries]

    def skinDoubleClickCmd(self):
        selectedItemSkins=[self.list_skins[i-1] for i in self.skinsList.getSelectIndexedItem()]
        select(selectedItemSkins)

    def geometrySelectCmd(self):
        selectedItemGeometry=[self.list_geometries[i-1] for i in self.geometriesList.getSelectIndexedItem()]
        #[selectedItemGeometry.append(self.list_geometries[i-1]) for i in self.geometriesList.getSelectIndexedItem()]
        select(selectedItemGeometry)

    def queryPoses(self, val):
        self.list_poses=[]
        self.posesList.removeAll()
        self.list_skins=[]
        self.skinsList.removeAll()
        self.list_geometries=[]
        self.geometriesList.removeAll()
        bp=''
        skin=''
        #for x in dagPose(self.getJoints(), query=True, bindPose=True):
        for x in ls(type='dagPose'):
            self.list_poses.append(x)
            bp='<BP>' if getAttr(x+'.bindPose') else ''
            skin='<Skin>' if len(listConnections((x+'.message'), type='skinCluster')) else ''
            self.posesList.append(x+bp+skin)

    def removeInvalidIntermediate(self, val):
        allShapes=listRelatives(children=True, shapes=True)
        noIntermediateObjs=listRelatives(children=True, shapes=True, noIntermediate=True)
        intermediateObj=list(set(allShapes)-set(noIntermediateObjs))
        for x in intermediateObj:
            if not len(listConnections(x)):
                delete(x)

    def showIntermediate(self, val):
        allShapes=listRelatives(children=True, shapes=True)
        noIntermediateObjs=listRelatives(children=True, shapes=True, noIntermediate=True)
        intermediateObj=list(set(allShapes)-set(noIntermediateObjs))
        [setAttr((x+'.intermediateObject'), False) for x in intermediateObj]

    def swithIntermediate(self, val):
        allShapes=listRelatives(children=True, shapes=True)
        noIntermediateObjs=listRelatives(children=True, shapes=True, noIntermediate=True)
        intermediateObj=list(set(allShapes)-set(noIntermediateObjs))
        [setAttr((x+'.intermediateObject'), False) for x in intermediateObj]
        [setAttr((x+'.intermediateObject'), True) for x in noIntermediateObjs]

    def randomJointColor(self, val):
        color=self.jointsColorSlider.getHsvValue()
        hsv=[0,0,0]
        for x in self.getJoints():
            hsv[0] = random.random() if self.randomColorCheck.getValue1() else color[0]/360
            hsv[1] = random.random() if self.randomColorCheck.getValue2() else color[1]
            hsv[2] = random.random() if self.randomColorCheck.getValue3() else color[2]
            rgb=mel.eval('hsv_to_rgb(<<'+str(hsv[0])+','+str(hsv[1])+','+str(hsv[2])+'>>)')
            setAttr((x+'.useObjectColor'), 2)
            setAttr((x+'.wireColorRGB'), rgb)

    def cleanJointColor(self, val):
        [setAttr((x+'.useObjectColor'), 0) for x in self.getJoints()]

    def setSelectedJointColor(self, val):
        color=self.jointsColorSlider.getRgbValue()
        for x in ls(sl=True, typ='joint'):
            setAttr((x+'.useObjectColor'), 2)
            setAttr((x+'.wireColorRGB'), color)

    def setHierarchyJointColor(self, val):
        color=self.jointsColorSlider.getRgbValue()
        for x in self.getJoints():
            setAttr((x+'.useObjectColor'), 2)
            setAttr((x+'.wireColorRGB'), color)

    # Select joints at the root of hierarchy.
    def selectRootJoints(self, val):
        select(self.findAllRoots(ls(sl=True, objectsOnly=True, typ='joint'), objtype='joint'))

    # Select joints at the end of hierarchy.
    def selectEndJoints(self, val):
        select( [x for x in self.getJoints() if not len(listRelatives(x, ad=True, typ='joint'))] )

    # Set joint orient attribute to zero.
    def setJointOrientZero(self, val):
        [setAttr((x+'.jointOrient'), (0,0,0)) for x in self.getJoints(no_selected_return_all=False)]

    # Set joint's Transform Attributes Locked and Invisible.
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

    # Set joint's Transform Attributes Unlocked and Visible.
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

    # Set joint's Local Rotation Axes visible.
    def jointsAxisInvisible(self, val):
        [setAttr((x+'.displayLocalAxis'), False) for x in self.getJoints()]

    # Set joint's Local Rotation Axes visible.
    def jointsAxisVisible(self, val):
        [setAttr((x+'.displayLocalAxis'), True) for x in self.getJoints()]

    def setJointSize(self, val):
        value=self.jointSizeSlider.getValue()
        jointDisplayScale(value)

    # Set Joint's Label to Joint's Name
    def setJointLabelToName(self, val):
        [setAttr((x+'.otherType'), x.nodeName(), type='string') for x in self.getJoints()]

    # Set joint's label visible.
    def jointsLabelVisible(self, val):
        for x in self.getJoints():
            setAttr((x+'.drawLabel'), True)
            if not getAttr((x+'.type')):
                setAttr((x+'.type'), 18)
                setAttr((x+'.otherType'), x.nodeName(), type='string')

    # Set joint's label invisible.
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

    # Convert Kinect1 Skeleton System to Kinect2
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
        parent('SHOULDERRIGHT', 'SHOULDERLEFT', w=True)
        newJo=insertJoint('SPINESHOULDER')
        newJo=rename(newJo, 'NECK')
        pos=getAttr('HEAD.t')*.25
        joint(newJo, e=True, co=True, r=True, p=pos)
        parent('SHOULDERRIGHT', 'SHOULDERLEFT', 'SPINESHOULDER')
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
        # Add all joints to bindPose
        K2Joints=['SPINEBASE', 'SPINEMID', 'SPINESHOULDER', 'NECK', 'HEAD', 'SHOULDERLEFT', 'ELBOWLEFT', 'WRISTLEFT', 'HANDLEFT', 'HANDTIPLEFT', 'THUMBLEFT', 'SHOULDERRIGHT',\
        'ELBOWRIGHT', 'WRISTRIGHT', 'HANDRIGHT', 'HANDTIPRIGHT', 'THUMBRIGHT', 'HIPLEFT', 'KNEELEFT', 'ANKLELEFT', 'FOOTLEFT', 'HIPRIGHT', 'KNEERIGHT', 'ANKLERIGHT', 'FOOTRIGHT']
        dagPose(K2Joints, addToPose=True, name=bindPoses[0])
