from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QApplication, QTextEdit
from PyQt5.QtGui import QColor, QTextFormat, QPainter, QTextCursor
from PyQt5.QtCore import QRect, pyqtSlot, Qt, QSize
from PyQt5 import uic, QtGui

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
    'lines': 'black',
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
    
class LineNumberArea(QWidget):
	def __init__(self, editor):
		QWidget.__init__(self, parent=editor)
		self.codeEditor = editor

	def sizeHint(self):
		return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

	def paintEvent(self, event):
		self.codeEditor.lineNumberAreaPaintEvent(event)

class CodeEditor(QPlainTextEdit):
	def __init__(self, parent=None):
		QPlainTextEdit.__init__(self, parent)
		self.lineNumberArea = LineNumberArea(self)
		self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
		self.updateRequest.connect(self.updateLineNumberArea)
		self.cursorPositionChanged.connect(self.highlightCurrentLine)
		self.updateLineNumberAreaWidth(0)
		self.highlightCurrentLine()

	def lineNumberAreaPaintEvent(self, event):
		painter = QPainter(self.lineNumberArea)
		#painter.fillRect(event.rect(), Qt.lightGray)
		painter.setPen(QColor(STYLES['lines']))

		block = self.firstVisibleBlock()
		blockNumber = block.blockNumber();
		top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
		bottom = top + self.blockBoundingRect(block).height()

		while block.isValid() and top <= event.rect().bottom():
			if block.isVisible() and bottom >= event.rect().top():
				number = str(blockNumber + 1)
				
				painter.drawText(0, top, self.lineNumberArea.width(), 
					self.fontMetrics().height(),
					Qt.AlignRight, number)
			block = block.next()
			top = bottom
			bottom = top + self.blockBoundingRect(block).height()
			blockNumber += 1

	def lineNumberAreaWidth(self):
		digits = len(str(self.blockCount()))
		space = 3 + self.fontMetrics().width('9')*digits
		return space

	def resizeEvent(self, event):
		QPlainTextEdit.resizeEvent(self, event)
		cr = self.contentsRect()
		self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

	def keyPressEvent(self, event):
		cursor = self.textCursor()
		if event.key() == Qt.Key_Tab:
			cursor.insertText(' ' * 4)
		elif event.key() == Qt.Key_Return:
			# Находим количество пробелов и табуляций в начале строки
			text = cursor.block().text()
			leading_spaces = len(text) - len(text.lstrip(' '))
			leading_tabs = len(text) - len(text.lstrip('\t'))
			# Вставляем новую строку с таким же количеством пробелов и табуляций
			cursor.insertText('\n' + ' ' * leading_spaces + '\t' * leading_tabs)
		else:
			super().keyPressEvent(event)

	def drawIndentationLines(self):
		painter = QPainter(self.viewport())
		painter.setPen(QColor(STYLES['lines']))
		font_metrics = self.fontMetrics()

		block = self.firstVisibleBlock()
		top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
		bottom = top + self.blockBoundingRect(block).height()

		while block.isValid() and top <= self.contentsRect().bottom():
			if block.isVisible():
				leading_spaces = len(block.text()) - len(block.text().lstrip())
				if leading_spaces > 0:
					x = self.lineNumberAreaWidth() + font_metrics.averageCharWidth() * leading_spaces // 2
					painter.drawLine(x-13, top, x-13, bottom)
			block = block.next()
			top = bottom
			bottom = top + self.blockBoundingRect(block).height()

	def paintEvent(self, event):
		self.drawIndentationLines()
		super().paintEvent(event)

	@pyqtSlot(int)
	def updateLineNumberAreaWidth(self, newBlockCount):
		self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

	@pyqtSlot()
	def highlightCurrentLine(self):
		extraSelections = []
		if not self.isReadOnly() and False:
			selection = QTextEdit.ExtraSelection()
			lineColor = QColor(Qt.blue).lighter(160)
			selection.format.setBackground(lineColor)
			selection.format.setProperty(QTextFormat.FullWidthSelection, True)
			selection.cursor = self.textCursor()
			selection.cursor.clearSelection()
			extraSelections.append(selection)
		self.setExtraSelections(extraSelections)

	@pyqtSlot(QRect, int)
	def updateLineNumberArea(self, rect, dy):
		if dy:
			self.lineNumberArea.scroll(0, dy)
		else:
			self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
		if rect.contains(self.viewport().rect()):
			self.updateLineNumberAreaWidth(0)