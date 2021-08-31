from PyQt5 import QtCore
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow,QApplication
import sys
from PyQt5.QtWebEngineWidgets import QWebEnginePage


# import UI file
from UI_main import Ui_MainWindow

class myBrowser(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self) 


        # Hide Widnow Frameless && Translucent Background
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)        
        

        # Configure close and Min btns
        self.btn_close.clicked.connect(lambda: self.close())
        self.btn_min.clicked.connect(lambda: self.showMinimized())
        
        # Max Btn 
        self.btn_max.setCheckable(True)
        self.btn_max.clicked.connect(self.maxWindow)
        
        # Configure WebEngine
        self.lineEdit_url.returnPressed.connect(self.loadUrl)
        self.btn_back.clicked.connect(self.backward)
        self.btn_forward.clicked.connect(self.forward)
        self.btn_reload.clicked.connect(self.reload)
        
        
        self.offset = None
        
        self.center()
        self.update()
        
        
    # Set Window in The Center Position
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    # Make frameless dragable
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    def maxWindow(self):
        if self.btn_max.isChecked():
            self.showMaximized()
            self.btn_max.setText(";")
        else:
            self.showNormal()
            self.btn_max.setText("")

    def loadUrl(self):
        url = QtCore.QUrl.fromUserInput(self.lineEdit_url.text())
        if url.isValid():
            self.webEngineView.load(url)
    def reload(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Reload)
    def backward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Back)
    def forward(self):
        self.webEngineView.page().triggerAction(QWebEnginePage.Forward)
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = myBrowser()
    window.show()
    app.exec_()