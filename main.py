# imports
import sys, os
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import traceback
from highlighter import *
# Give imports up

# Main window of all programm
class RickWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Folder variables
        self.curFile = None
        self.curFolder = None

        # Asking how does window feeling
        uic.loadUi('ui/code.ui', self)

        # Tell the window how it should feel
        self.setWindowTitle(f'Rickroll IDE')

        # Give some shit up
        self.codeEdit.hide()
        self.foldersList.hide()

        # Oh yes, preparing code area
        self.highlighter = RickHighlighter(self.codeEdit.document())
        self.codeEdit.setTabStopDistance(4)
        self.codeEdit.setTabStopWidth(20)

        # Connecting widgets to events
        self.codeEdit.textChanged.connect(self.return_tabs)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSave_as.triggered.connect(self.saveFileAs)
        self.actionNew.triggered.connect(self.newFile)
        self.foldersList.itemDoubleClicked.connect(self.folderClicked)

    # Set window title when it has a file
    def setTitle(self):
        self.setWindowTitle(f'{self.curFile.split("/")[-1]} - Rickroll script in {self.curFolder}')
        self.folder()

    # Folders
    
    def folder(self):
        foldsmb = '🗀'
        filesmb = '🗊'
        self.foldersList.clear()
        self.foldersList.addItem('...')
        for i in os.listdir(self.curFolder):
            symb = ''
            if os.path.isdir(self.curFolder + i):
                symb = foldsmb
            elif os.path.isfile(self.curFolder + i):
                symb = filesmb
            self.foldersList.addItem(symb + i)

    def folderClicked(self, event):
        if event.text() == '...':
            self.curFolder = '/'.join(self.curFolder.split('/')[:-2]) + '/'
            self.folder()
            return
        folder = self.curFolder + event.text()[1:]
        if os.path.isfile(folder):
            self.codeEdit.setPlainText(open(folder, 'r').read())
            self.curFile = folder
            self.curFolder = '/'.join(self.curFile.split('/')[:-1]) + '/'
            self.setTitle()
        else:
            self.curFolder = folder + '/'
            self.folder()

    # Files
    
    def newFile(self):
        self.codeEdit.setPlainText('')
        self.codeEdit.show()
        self.foldersList.show()
        self.setWindowTitle(f'Rickroll IDE (New unnamed file)')
        
    def saveFile(self):
        if not self.curFile:
            self.saveFileAs()
        else:
            with open(self.curFile, 'w') as file:
                file.write(self.codeEdit.toPlainText())
                           
    def saveFileAs(self):
        folder = QFileDialog.getSaveFileName(
            self, 'Create file', '',
            'Rickroll script (*.rickroll);;Another file type(*)')[0]
        with open(folder, 'w') as file:
            file.write(self.codeEdit.toPlainText())
            self.curFile = folder
            self.curFolder = '/'.join(folder.split('/')[:-1]) + '/'
            print(self.curFolder)
        self.setTitle()

    def openFile(self):
        folder = QFileDialog.getOpenFileName(
            self, 'Select file', '',
            'Rickroll script (*.rickroll);;Another file type(*)')[0]
        self.codeEdit.setPlainText(open(folder, 'r').read())
        self.codeEdit.show()
        self.foldersList.show()
        self.curFile = folder
        self.curFolder = '/'.join(self.curFile.split('/')[:-1]) + '/'
        self.setTitle()
        

    def return_tabs(self):
        if False and self.codeEdit.toPlainText()[-1] == '\n' and self.codeEdit.toPlainText()[-2].startswith('\t'):
            text = self.codeEdit.toPlainText()
            tabs = self.codeEdit.toPlainText().split('\n')[-2].count('\t')
            text = '\n'.join(text.split('\n')[:-1]) + text.split('\n')[-1] + '\n' + tabs * '\t'
            self.codeEdit.setPlainText(text)

        
def log_uncaught_exceptions(ex_cls, e, tb):  # Let errors cry
    text = '{}: {}:\n'.format(ex_cls.__name__, e)

    text += ''.join(traceback.format_tb(tb))

    print(text)
    #QMessageBox.critical(None, 'Error', text)

    # sys.exit()


if __name__ == '__main__':
    never = QApplication(sys.argv)
    sys.excepthook = log_uncaught_exceptions
    gonna = RickWindow()
    gonna.show()
    sys.exit(never.exec_())
