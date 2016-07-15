#Rigging misc tools.

from pymel.core import *

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
                    self.showJointLableButton = button(l='Show All Joint\'s Lable', h=30)
                    self.hideJointLableButton = button(l='Hide All Joint\'s Lable', h=30)
            formLayout(self.form, e=True, af=[(self.clumn,'top',0), (self.clumn,'left',0), (self.clumn,'right',0), (self.clumn,'bottom',0)])
        self.showJointLableButton.setCommand(self.allJointsLableVisible)
        self.hideJointLableButton.setCommand(self.allJointsLableInvisible)
        self.embed=self.frame #This attribute is used to embed in MayaMiscTools's Layout.

    def openUI(self):
        if window('riggingMiscTools', q=True, ex=True):
            deleteUI('riggingMiscTools', wnd=True)
        self.initUI()
        showWindow(self.win)

    #Set all joint's lable visible
    def allJointsLableVisible(self, val):
        for x in ls(typ='joint'):
            setAttr((x+'.drawLabel'), True)
            if not getAttr((x+'.type')):
                setAttr((x+'.type'), 18)
                setAttr((x+'.otherType'), x.nodeName(), type='string')

    #Set all joint's lable invisible
    def allJointsLableInvisible(self, val):
        for x in ls(typ='joint'):
            setAttr((x+'.drawLabel'), False)
