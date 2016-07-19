# This module is a collection that include all tool's module files and organize the UI.

from pymel.core import *
import unique_name_manager as unm
import batch_processing_files as bpf

if not 'rigging_misc_tools' in sys.modules:
   import rigging_misc_tools as rmt
else:
   reload(rmt)



def openUI():
    MayaMiscTools().openUI()

class MayaMiscTools(object):
    'The base class'

    def initUI(self):
        self.win=window('mayaMiscTools',t='Maya Misc Tools',w=400)
        with formLayout() as self.form:
            with tabLayout(innerMarginWidth=5, innerMarginHeight=5) as self.tabs:
                #embed tab1
                tab1=unm.UniqueNameManager()
                tab1.initUI(self.tabs)
                #embed tab2
                tab2=bpf.BatchProcessingFiles()
                tab2.initUI(self.tabs)
                #embed tab3
                tab3=rmt.RiggingMiscTools()
                tab3.initUI(self.tabs)

        formLayout( self.form, edit=True, attachForm=((self.tabs, 'top', 0), (self.tabs, 'left', 0), (self.tabs, 'bottom', 0), (self.tabs, 'right', 0)) )
        tabLayout( self.tabs, edit=True, tabLabel=((tab1.embed, tab1.lable), (tab2.embed, tab2.lable), (tab3.embed, tab3.lable)) )

    def openUI(self):
        if window('mayaMiscTools', q=True, ex=True):
            deleteUI('mayaMiscTools', wnd=True)
        self.initUI()
        showWindow(self.win)
