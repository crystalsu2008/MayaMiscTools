# This procedure is used to execute a paragraph of script in the selected files.
# Not done yet!!!
from pymel.core import *

class BatchProcessingFiles(object):
    'Batch processing files class'
    files=[]
    label='Batch Processing Fiels' #This label is used to embed in MayaMiscTools's Layout.

    def initUI(self, parentLayout=None):
        if parentLayout:
            setParent(parentLayout)
        else:
            self.win=window('batchProcessingFielsWin',t=self.label,w=400)
        with frameLayout(bv=False,lv=False,label=self.label) as self.frame:
            with formLayout(numberOfDivisions=100) as self.form:
                with paneLayout(configuration='horizontal2') as self.pane:
                    with frameLayout(bv=True,lv=True,label='Files List') as self.fileListFrame:
                        with formLayout(numberOfDivisions=100) as self.fileListForm:
                            self.filesList=textScrollList(ams=True)
                            self.addFilesButton=button(l='Add Files...',h=24)
                            self.removeFilesButton=button(l='Remove',h=24)

                            formLayout(self.fileListForm, e=True, ac=[(self.filesList,'bottom',0,self.addFilesButton)],af=[(self.filesList,'top',0),(self.filesList,'left',0),(self.filesList,'right',0)])
                            formLayout(self.fileListForm, e=True, af=[(self.addFilesButton,'bottom',0),(self.addFilesButton,'left',0),(self.removeFilesButton,'bottom',0),(self.removeFilesButton,'right',0)],\
                                ap=[(self.addFilesButton,'right',0,50),(self.removeFilesButton,'left',0,50)])
                    scrollField()
                self.processingButton=button(l='Processing...',h=30)
                formLayout(self.form, e=True, ac=[(self.pane,'bottom',0,self.processingButton)],af=[(self.pane,'top',0),(self.pane,'left',0),(self.pane,'right',0)])
                formLayout(self.form, e=True, af=[(self.processingButton,'bottom',0),(self.processingButton,'left',0),(self.processingButton,'right',0)])
        self.addFilesButton.setCommand(self.addFiles)
        self.removeFilesButton.setCommand(self.removeFiles)
        self.processingButton.setCommand(self.processing)
        self.embed=self.frame #This attribute is used to embed in MayaMiscTools's Layout.

    def openUI(self):
        if window('batchProcessingFielsWin', q=True, ex=True):
            deleteUI('batchProcessingFielsWin', wnd=True)
        self.initUI()
        showWindow(self.win)

    def addFiles(self, val):
        multipleFilters="Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
        addfiles=fileDialog2(ds=2,fm=4,cap='Select Batch Files',ff=multipleFilters,okc='Add Select')
        try:
            for addfile in addfiles:
                if not self.files.count(addfile):
                    self.files.append(addfile)
                    self.filesList.append(addfile)
        except:
            pass

    def removeFiles(self, val):
        selectfilesid=self.filesList.getSelectIndexedItem()
        selectfilesid.sort()
        selectfilesid.reverse()
        for x in selectfilesid:
            self.filesList.removeIndexedItem(x)
            self.files.pop(x-1)

    def processing(self, val):
        for x in self.files:
            print '"'+x+'",'
