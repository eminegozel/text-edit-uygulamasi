import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QFileDialog,
    QMessageBox, QToolBar, QSpinBox, QColorDialog, QFontComboBox, QStyle
)
from PyQt5.QtGui import QIcon, QFont, QTextCharFormat, QTextCursor
from PyQt5.QtCore import Qt

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Text Editör")
        self.setGeometry(100, 100, 800, 600)
        self.filename = None
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.textEdit)
        self.statusBar().showMessage('Hazır')

        # Dosya araç çubuğu
        fileBar = QToolBar('Dosya', self)
        fileBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(fileBar)
        fileBar.addAction(self._action('Yeni', 'Ctrl+N', self.newFile,
            icon=self.style().standardIcon(QStyle.SP_FileIcon)))
        fileBar.addAction(self._action('Aç', 'Ctrl+O', self.openFile,
            icon=self.style().standardIcon(QStyle.SP_DialogOpenButton)))
        fileBar.addAction(self._action('Kaydet', 'Ctrl+S', self.saveFile,
            icon=self.style().standardIcon(QStyle.SP_DialogSaveButton)))

        # Biçim araç çubuğu
        fmtBar = QToolBar('Biçim', self)
        fmtBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(fmtBar)

        # Font seçici
        fontBox = QFontComboBox(self)
        fontBox.currentFontChanged.connect(self.setFontFamily)
        fmtBar.addWidget(fontBox)

        # Punto seçici
        sizeBox = QSpinBox(self)
        sizeBox.setRange(6, 72)
        sizeBox.setValue(12)
        sizeBox.valueChanged.connect(self.setFontSize)
        fmtBar.addWidget(sizeBox)

        # Renk seçici
        fmtBar.addAction(self._action('Renk', None, self.selectColor,
            icon=self.style().standardIcon(QStyle.SP_DialogResetButton)))

        # Stil butonları
        fmtBar.addAction(self._action('Kalın', 'Ctrl+B', self.toggleBold, checkable=True))
        fmtBar.addAction(self._action('İtalik', 'Ctrl+I', self.toggleItalic, checkable=True))
        fmtBar.addAction(self._action('Altı Çizili', 'Ctrl+U', self.toggleUnderline, checkable=True))

    def _action(self, text, shortcut, slot, checkable=False, icon=None):
        if icon:
            act = QAction(icon, text, self)
        else:
            act = QAction(text, self)
        if shortcut:
            act.setShortcut(shortcut)
        act.triggered.connect(slot)
        act.setCheckable(checkable)
        return act

    def newFile(self):
        if self._maybeSave(): return
        self.textEdit.clear()
        self.filename = None
        self.statusBar().showMessage('Yeni dosya')

    def _maybeSave(self):
        if self.textEdit.document().isModified():
            resp = QMessageBox.question(self, 'Kaydedilsin mi?', 'Değişiklikler kaydedilsin mi?',
                                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if resp == QMessageBox.Yes:
                return not self.saveFile()
            if resp == QMessageBox.Cancel:
                return True
        return False

    def openFile(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Dosya Aç', '',
            'Metin Dosyaları (*.txt);;Tüm Dosyalar (*)')
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                self.textEdit.setPlainText(f.read())
            self.filename = path
            self.statusBar().showMessage(f'Açıldı: {path}')

    def saveFile(self):
        if not self.filename:
            return self.saveAsFile()
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(self.textEdit.toPlainText())
        self.textEdit.document().setModified(False)
        self.statusBar().showMessage(f'Kaydedildi: {self.filename}')
        return True

    def saveAsFile(self):
        path, _ = QFileDialog.getSaveFileName(self, 'Farklı Kaydet', '',
            'Metin Dosyaları (*.txt);;Tüm Dosyalar (*)')
        if path:
            self.filename = path
            return self.saveFile()
        return False

    def setFontFamily(self, font):
        fmt = QTextCharFormat()
        fmt.setFontFamily(font.family())
        self._mergeFormat(fmt)

    def setFontSize(self, size):
        fmt = QTextCharFormat()
        fmt.setFontPointSize(size)
        self._mergeFormat(fmt)

    def selectColor(self):
        col = QColorDialog.getColor(self.textEdit.textColor(), self)
        if col.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(col)
            self._mergeFormat(fmt)

    def toggleBold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if self.textEdit.fontWeight() != QFont.Bold else QFont.Normal)
        self._mergeFormat(fmt)

    def toggleItalic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(not self.textEdit.fontItalic())
        self._mergeFormat(fmt)

    def toggleUnderline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(not self.textEdit.fontUnderline())
        self._mergeFormat(fmt)

    def _mergeFormat(self, fmt):
        cursor = self.textEdit.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(fmt)
        self.textEdit.mergeCurrentCharFormat(fmt)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())
