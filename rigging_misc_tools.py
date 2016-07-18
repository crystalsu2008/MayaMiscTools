#Rigging misc tools.

from pymel.core import *
#import maya.cmds as cmds

class RiggingMiscTools(object):
    'This class include some little function for rigging'
    lable='Rigging Misc Tools' #This lable is used to embed in MayaMiscTools's Layout.

    def initUI(self, parentLayout=None):
        if parentLayout:
            setParent(parentLayout)
        else:
            self.win=window('riggingMiscTools',t=self.lable,w=400)
        with frameLayout(bv=True,lv=False,label=self.lable) as self.frame:
            with formLayout(numberOfDivisions=100) as self.form:
                with columnLayout(cat=('both', 0), rs=0, adj=True) as self.clumn:
                    self.jointSizeSlider=floatSliderGrp(cw=[1,60], label='Joint Size', field=True, minValue=0.01, maxValue=10.0, fieldMinValue=0.01, fieldMaxValue=100.0, precision=2, value=1)
                    with gridLayout(  cellWidthHeight=(30, 30),columnsResizable=True) as self.sizeButtongrid:
                        button(l='0.01', h=30, command='jointDisplayScale(0.01)')
                        button(l='0.25', h=30, command='jointDisplayScale(0.25)')
                        button(l='0.5', h=30, command='jointDisplayScale(0.5)')
                        button(l='0.75', h=30, command='jointDisplayScale(0.75)')
                        button(l='1', h=30, command='jointDisplayScale(1)')
                        for i in range(2,11):
                            button(l=(i), h=30, command=('jointDisplayScale('+str(i)+')'))
                    with formLayout(numberOfDivisions=100) as self.showJointLableForm:
                        self.showJointLableButton=button(l='Show Joint\'s Lable', h=30)
                        SJLB=self.showJointLableButton
                        self.hideJointLableButton=button(l='Hide Joint\'s Lable', h=30)
                        HJLB=self.hideJointLableButton
                    formLayout(self.showJointLableForm, e=True, af=[(SJLB,'top',0), (SJLB,'left',0), (HJLB,'right',0), (HJLB,'top',0)], ap=[(SJLB,'right',0,50), (HJLB,'left',0,50)])
                    with formLayout(numberOfDivisions=100) as self.showJointAxisForm:
                        self.showJointAxisButton=button(l='Show Joint\'s Local Rotation Axes', h=30)
                        SJAB=self.showJointAxisButton
                        self.hideJointAxisButton=button(l='Hide Joint\'s Local Rotation Axes', h=30)
                        HJAB=self.hideJointAxisButton
                    formLayout(self.showJointAxisForm, e=True, af=[(SJAB,'top',0), (SJAB,'left',0), (HJAB,'right',0), (HJAB,'top',0)], ap=[(SJAB,'right',0,50), (HJAB,'left',0,50)])
            formLayout(self.form, e=True, af=[(self.clumn,'top',0), (self.clumn,'left',0), (self.clumn,'right',0), (self.clumn,'bottom',0)])
        self.jointSizeSlider.changeCommand(self.setJointSize)
        self.jointSizeSlider.dragCommand(self.setJointSize)
        self.showJointLableButton.setCommand(self.jointsLableVisible)
        self.hideJointLableButton.setCommand(self.jointsLableInvisible)
        self.showJointAxisButton.setCommand(self.jointsAxisVisible)
        self.hideJointAxisButton.setCommand(self.jointsAxisInvisible)
        self.embed=self.frame #This attribute is used to embed in MayaMiscTools's Layout.

    #Set joint's Local Rotation Axes visible
    def jointsAxisInvisible(self, val):
        seljoints=ls(sl=True, typ='joint')
        joints=seljoints
        if(len(seljoints)):
            for x in seljoints:
                [joints.append(y) for y in listRelatives(x, ad=True, typ='joint') if not y in joints]
        else:
            joints=ls(typ='joint')
        [setAttr((x+'.displayLocalAxis'), False) for x in joints]

    #Set joint's Local Rotation Axes visible
    def jointsAxisVisible(self, val):
        seljoints=ls(sl=True, typ='joint')
        joints=seljoints
        if(len(seljoints)):
            for x in seljoints:
                [joints.append(y) for y in listRelatives(x, ad=True, typ='joint') if not y in joints]
        else:
            joints=ls(typ='joint')
        for x in joints:
            setAttr((x+'.displayLocalAxis'), True)

    def setJointSize(self, val):
        value=self.jointSizeSlider.getValue()
        jointDisplayScale(value)

    #Set joint's lable visible
    def jointsLableVisible(self, val):
        seljoints=ls(sl=True, typ='joint')
        joints=seljoints
        if(len(seljoints)):
            for x in seljoints:
                [joints.append(y) for y in listRelatives(x, ad=True, typ='joint') if not y in joints]
        else:
            joints=ls(typ='joint')
        for x in joints:
            setAttr((x+'.drawLabel'), True)
            if not getAttr((x+'.type')):
                setAttr((x+'.type'), 18)
                setAttr((x+'.otherType'), x.nodeName(), type='string')

    #Set joint's lable invisible
    def jointsLableInvisible(self, val):
        seljoints=ls(sl=True, typ='joint')
        joints=seljoints
        if(len(seljoints)):
            for x in seljoints:
                [joints.append(y) for y in listRelatives(x, ad=True, typ='joint') if not y in joints]
        else:
            joints=ls(typ='joint')
        [setAttr((x+'.drawLabel'), False) for x in joints]

    def openUI(self):
        if window('riggingMiscTools', q=True, ex=True):
            deleteUI('riggingMiscTools', wnd=True)
        self.initUI()
        showWindow(self.win)
