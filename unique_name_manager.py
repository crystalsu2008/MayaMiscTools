#This is used to find out all dag nodes those have same name, and fix the problem.

from pymel.core import *

class UniqueNameManager(object):
    'This class is used to find out all dag nodes those have same name, and fix the problem.'
    multname_objs={}
    list_objs=[]
    label = 'Unique Name Manager' #This label is used to embed in MayaMiscTools's Layout.

    def initUI(self, parentLayout=None):
        if parentLayout:
            setParent(parentLayout)
        else:
            self.win=window('uniqueNameManagerWin',t=self.label,w=400)
        with frameLayout(bv=True,lv=False,label=self.label) as self.frame:
            with formLayout(numberOfDivisions=100) as self.form:
                self.analyseButton = button(l='Analyse Scene Multiple Names', h=30)
                self.listCollection = radioCollection()
                self.allRadio = radioButton( 'All', label='All')
                self.onlyTransRadio = radioButton( 'Transform', label='Transform', sl=True)
                self.onlyShapeRadio = radioButton( 'Shapes', label='Shapes' )
                self.onlyJointRadio = radioButton( 'Joints', label='Joints' )
                self.uniqueSelectedNameButton = button(l='Auto Unique Selected Objects Names', h=30)
                with columnLayout(adj=True) as self.column:
                    self.objList = textScrollList(ams=True)
            AB=self.analyseButton
            formLayout(self.form, e=True, af=[(AB,'top',0),(AB,'left',0),(AB,'right',0)])
            formLayout(self.form, e=True, ac=[(self.allRadio,'top',0,AB)], af=[(self.allRadio,'left',0)])
            formLayout(self.form, e=True, ac=[(self.onlyTransRadio,'top',0,AB), (self.onlyTransRadio,'left',0,self.allRadio)])
            formLayout(self.form, e=True, ac=[(self.onlyShapeRadio,'top',0,AB), (self.onlyShapeRadio,'left',0,self.onlyTransRadio)])
            formLayout(self.form, e=True, ac=[(self.onlyJointRadio,'top',0,AB), (self.onlyJointRadio,'left',0,self.onlyShapeRadio)])
            USNB=self.uniqueSelectedNameButton
            formLayout(self.form, e=True, af=[(USNB,'bottom',0),(USNB,'left',0),(USNB,'right',0)])
            formLayout(self.form, e=True, ac=[(self.column,'top',0,self.onlyTransRadio), (self.column,'bottom',0,USNB)], af=[(self.column,'left',0),(self.column,'right',0)])
        self.analyseButton.setCommand(self.analyse)
        self.uniqueSelectedNameButton.setCommand(self.uniqueSelectedName)
        self.objList.selectCommand(self.listselcmd)
        self.embed=self.frame #This attribute is used to embed in MayaMiscTools's Layout.

    def openUI(self):
        if window('uniqueNameManagerWin', q=True, ex=True):
            deleteUI('uniqueNameManagerWin', wnd=True)
        self.initUI()
        showWindow(self.win)

    def eraseEndNumbers(self, string):
        try:
            size = len(string)
            re.match('[0-9]', string[size-1]).group()
            string = self.eraseEndNumbers(string[:size-1])
            return string
        except:
            return string

    def uniqueObjName(self, obj):
        basename = self.eraseEndNumbers(obj.nodeName())
        otherSameBasenameObjsName = [x.nodeName() for x in ls(dag=True) if (x.nodeName().count(basename)and(x!=obj))]
        newname = basename
        num = 0
        if otherSameBasenameObjsName.count(obj.nodeName()):
            while otherSameBasenameObjsName.count(newname):
                newname = basename + str(num)
                num += 1
            print 'rename "%s" "%s";' % (obj.name(), newname)
            obj.rename(newname)
        else:
            newname = obj.nodeName()
        return newname

    def analyse(self, val):
        self.multname_objs.clear()
        types = {'All': (), 'Transform': 'transform', 'Shapes': 'shape', 'Joints': 'joint'}
        obj_multnames = ((x, x.nodeName()) for x in ls(dag=True, typ=types[self.listCollection.getSelect()]) if x.count('|'))
        for (obj, name) in obj_multnames:
            if name in self.multname_objs:
                self.multname_objs[name].append(obj)
            else:
                self.multname_objs[name]=[obj]
        self.refreshList()

    def refreshList(self):
        self.objList.removeAll()
        self.list_objs=[]
        for x in self.multname_objs:
            for y in self.multname_objs[x]:
                self.objList.append(y.type()+' / '+x+' / '+y)
                self.list_objs.append(y)
        self.objList.setHeight( max(112,self.objList.getNumberOfItems()*14) )

    def listselcmd(self):
        selobj = ( str(self.list_objs[x-1]) for x in self.objList.getSelectIndexedItem() )
        select(selobj)

    def uniqueSelectedName(self, val):
        for id in self.objList.getSelectIndexedItem():
            self.uniqueObjName(self.list_objs[id-1])
