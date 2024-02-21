# imports
import json
import sys, os
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import traceback
from highlighter import *
import webbrowser
import multiprocessing
from presence import set_discord_rpc_filename, update_presence
from QImageWidget import QImageWidget
import subprocess

# Give imports up
Ui_MainWindow, QtBaseClass = uic.loadUiType('EditorUI.ui')

def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QtGui.QColor()
    _color.setNamedColor(color)

    _format = QtGui.QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QtGui.QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)
    return _format

try:
    STYLES = eval(open(open('themes/current_theme.txt', 'r').read(), 'r').read())
except:
    STYLES = {
    "lines": "#AAAAAA",
    "background": "white",
    "text": "black",
    "keyword": format("blue"),
    "keyword2": format("#fd7e00"),
    "keyword3": format("grey", "italic"),
    "operator": format("red"),
    "brace": format("darkGray"),
    "defclass": format("black", "bold"),
    "string": format("magenta"),
    "string2": format("darkMagenta"),
    "comment": format("darkGreen", "italic"),
    "self": format("black", "italic"),
    "numbers": format("brown")
}


# Main window of the program
class RickWindow(QMainWindow):
    docs_links = [
    'https://github.com/Rick-Lang/rickroll-lang/blob/main/doc.md',
    'https://github.com/Rick-Lang/rickroll-lang/blob/main/doc-Ch.md',
    'https://github.com/Rick-Lang/rickroll-lang/blob/main/doc-RU.md'
    ]
    rickroll_folder = open('rcllngdir', 'r').read()
    def __init__(self):
        super().__init__()
        # Variables
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.curFile = None
        self.curFolder = None
        self.curTheme = open('themes/current_theme.txt', 'r').read()
        # Asking how does window feeling
        uic.loadUi('ui/code.ui', self)
        print('''------------------------------------------------------------------------------
 ------------------####################################------------------------
 --------------##################################################--------------
 --------------######################################################----------
 ------------##########################################################--------
 ----------############################################################--------
 ----------##################--------##################################--------
 --------################----------##----##############--------##########------
 --------##############------------####----########------------############----
 ------####------##################------########------######################--
 ----####--######------####----####################--##############----######--
 --####--######--######----########################--######--------##########--
 --####--####------##################################--######################--
 --####--##----####----##############--################--##########--########--
 --####--######--######------########--##----########----########----######----
 ----##########----####--####------##--##########----##########--------####----
 ------##########----------########--------################------------####----
 --------########--####------######--######------------------####------####----
 --------##########--##--##----------########--####--######--##--------##------
 ----------##########----########--------------------------------------##------
 ----------############--########--####--------------------------------##------
 ------------############----####--########--##----------------------####------
 --------------############------##########--######--####--##--##----######----
 ----------------##############------######--######--##----##------########----
 --------------------##################------------------------############----
 ----------------------####################################################----
 ----------------------------##############################################----
 --------------------------------##########################################----
 ------------------------------------####################################------
 ----------------------------------------################################------
 ------------------------------------------------####################----------''')

        # Tell the window how it should feel
        self.setWindowTitle(f'Rickroll IDE')
        set_discord_rpc_filename("Rickroll IDE")
        self.setWindowIcon(QtGui.QIcon(self.scriptDir + os.path.sep + 'ui/src/icon.png'))

        # Give some shit up
        self.codeEdit.hide()
        self.foldersList.hide()

        # Oh yes, preparing code area
        self.highlighter = RickHighlighter(STYLES, self.codeEdit.document())
        self.codeEdit.setTabStopDistance(4)
        self.codeEdit.setTabStopWidth(20)
        self.logo = QImageWidget(self, 'ui/src/icon.png')
        self.show()
        
        # Connecting widgets to events

        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSave_as.triggered.connect(self.saveFileAs)
        self.actionSave_as.triggered.connect(self.saveFileAs)
        self.actionNew.triggered.connect(self.newFile)
        self.actionThemes.triggered.connect(self.themes_options)
        self.foldersList.itemDoubleClicked.connect(self.folderClicked)
        self.update_theme(self.curTheme)
        self.actionEnglish.triggered.connect(lambda: webbrowser.open(self.docs_links[0]))
        self.actionChinese.triggered.connect(lambda: webbrowser.open(self.docs_links[1]))
        self.actionRussian.triggered.connect(lambda: webbrowser.open(self.docs_links[2]))
        self.actionRun_current_script.triggered.connect(self.runscript)
        self.actionAbout_IDE.triggered.connect(lambda: webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ'))
        self.actionSelInt.triggered.connect(self.askforfolder)
        #Keybinds
        self.actionSave.setShortcut(QtGui.QKeySequence("Ctrl+s"))
        self.actionNew.setShortcut(QtGui.QKeySequence("Ctrl+n"))
        self.actionOpen.setShortcut(QtGui.QKeySequence("Ctrl+o"))


        if self.rickroll_folder == '':
            self.askforfolder()

    def runscript(self):
        with open('script.bat', 'w') as f:
            f.write(f"python -i {self.rickroll_folder} {self.curFile}")
        subprocess.Popen(f"start script.bat", shell=True)
        print(f"script {self.curFile} opened via {self.rickroll_folder}")

    def askforfolder(self):
        folder = QFileDialog.getOpenFileName(
            self, 'Select interpreter (RickRoll.py)', os.getcwd(),
            'Python script(*.py)')[0]
        with open('rcllngdir', 'w') as f:
            f.write(str(folder))
        self.rickroll_folder = folder


    def resizeEvent(self, event):
        size = self.size()
        codepos = self.codeEdit.geometry()
        folderpos = self.foldersList.geometry()
        #self.codeEdit.resize(self.size().width() - codepos.left() - 10, self.size().height() - codepos.top() - 30)
        self.codeEdit.resize(self.size().width() - codepos.left() - 10, self.size().height() - codepos.top() - 30)
        self.foldersList.resize(folderpos.width(), self.size().height() - folderpos.top() - 30)
        if not self.codeEdit.isVisible():
            self.logo.setScale((self.height() // 1.6, self.height() // 1.6), Qt.KeepAspectRatio)
            self.logo.move((self.width() - self.logo.width()) // 2, (self.height() - self.logo.height()) // 2)
        
    # Themes
    def update_theme(self, folder):
        try:
            theme = eval(open(folder, 'r').read())
            self.highlighter = RickHighlighter(theme, self.codeEdit.document())
            self.setStyleSheet(f"background-color: {theme['background']};\ncolor: {theme['text']}")
            with open('themes/current_theme.txt', 'w') as f:
                f.write(folder)
        except:
            pass

    # Set window title when it has a file
    def setTitle(self):
        self.setWindowTitle(f'{self.curFile.split("/")[-1]} - {self.curFolder}')
        set_discord_rpc_filename(self.curFile.split("/")[-1])
        self.folder()

    #Options
        
    def themes_options(self, checked):
        self.themesw = ThemesWindow(self)
        self.themesw.show()
        
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
            self.codeEdit.setPlainText(open(folder, 'r', encoding="utf-8").read())
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
        self.logo.hide()
        self.setWindowTitle(f'Rickroll IDE (New unnamed file)')
        set_discord_rpc_filename("New unnamed file")
        
    def saveFile(self):
        if not self.curFile:
            self.saveFileAs()
        else:
            with open(self.curFile, 'w', encoding="utf-8") as file:
                file.write(self.codeEdit.toPlainText())
                           
    def saveFileAs(self):
        folder = QFileDialog.getSaveFileName(
            self, 'Create file', os.getcwd(),
            'Rickroll script (*.rickroll);;Another file type(*)')[0]
        with open(folder, 'w', encoding="utf-8") as file:
            file.write(self.codeEdit.toPlainText())
            self.curFile = folder
            self.curFolder = '/'.join(folder.split('/')[:-1]) + '/'
            print(self.curFolder)
        self.setTitle()

    def openFile(self):
        folder = QFileDialog.getOpenFileName(
            self, 'Select file', os.getcwd(),
            'Rickroll script (*.rickroll);;Another file type(*)')[0]
        self.codeEdit.setPlainText(open(folder, 'r').read())
        self.codeEdit.show()
        self.foldersList.show()
        self.logo.hide()
        self.curFile = folder
        self.curFolder = '/'.join(self.curFile.split('/')[:-1]) + '/'
        self.setTitle()


class ThemesWindow(QWidget):
    def __init__(self, parent):
        self.main = parent
        super().__init__()
        uic.loadUi('ui/themes.ui', self)
        self.setWindowTitle(f'Themes options')
        set_discord_rpc_filename("Themes options")
        try:
            self.update_theme(self.main.curTheme)
        except Exception:
            pass
        self.selectButton.clicked.connect(self.addTheme)

    def addTheme(self):
        folder = folder = QFileDialog.getOpenFileName(
            self, 'Select file', os.getcwd() + '/themes',
            'Json theme file (*.json);;Another file type(*)')[0]
        self.main.curTheme = folder
        self.main.update_theme(folder)
        self.update_theme(folder)
        self.close()
        
    def update_theme(self, folder):
        try:
            theme = eval(open(folder, 'r').read())
            self.highlighter = RickHighlighter(theme, self.codeEdit.document())
            self.setStyleSheet(f"background-color: {theme['background']};\ncolor: {theme['text']}")
        except:
            pass


def log_uncaught_exceptions(ex_cls, e, tb):  # Let errors cry
    text = '{}: {}:\n'.format(ex_cls.__name__, e)

    text += ''.join(traceback.format_tb(tb))

    print(text)
    #QMessageBox.critical(None, 'Error', text)

    # sys.exit()


if __name__ == '__main__':
    # Give presence up
    multiprocessing.freeze_support()
    p = multiprocessing.Process(target=update_presence)
    #p.daemon = True
    p.start()

    never = QApplication(sys.argv)
    sys.excepthook = log_uncaught_exceptions
    gonna = RickWindow()
    gonna.show()
    sys.exit(never.exec_())
