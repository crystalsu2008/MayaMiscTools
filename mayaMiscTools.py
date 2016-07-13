import bpf #Tools-1, Batch Processing Files
#reload(bpf)
from pymel.core import *

class mayaMiscTools():
    
    def initUI(self): 
        self.win=window('mayaMiscTools',t='Maya Misc Tools',w=400)
        with formLayout() as self.form:
            with tabLayout(innerMarginWidth=5, innerMarginHeight=5) as self.tabs:
                #embed tab1
                tab1=bpf.batchProcessingFiles()
                tab1.initUI(self.tabs)

        formLayout( self.form, edit=True, attachForm=((self.tabs, 'top', 0), (self.tabs, 'left', 0), (self.tabs, 'bottom', 0), (self.tabs, 'right', 0)) )
        tabLayout( self.tabs, edit=True, tabLabel=(tab1.embed, tab1.lable) )

    def openUI(self):
        if window('mayaMiscTools', q=True, ex=True):
            deleteUI('mayaMiscTools', wnd=True)
        self.initUI()
        showWindow(self.win)

mmt=MayaMiscTools()
mmt.openUI()


