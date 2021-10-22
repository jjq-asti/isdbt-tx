import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from qt_material import apply_stylesheet

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.statusBar = None
        self.create_menu()
        self.create_toolbar()
        self.create_dockwidget()
        self.create_statusbar()
        self.setFixedSize(900, 400)

    def create_central_widget(self):
        frame =  QtWidgets.QFrame()
        layout = QtWidgets.QVBoxLayout()
        btn = QtWidgets.QPushButton('click me')
        btn.setMaximumSize(100,20)
        btn.clicked.connect(self.btn_cliked)
        layout.addWidget(btn)
        frame.setLayout(layout)
        self.setCentralWidget(frame)

    def btn_cliked(self):
        self.statusBar.showMessage('btn_clicked')

    def create_menu(self):
        menu1 = self.menuBar().addMenu('Menu')
        menu1.addAction('File')
        menu1.addAction('Preference')
        menu2 = self.menuBar().addMenu("Themes")
        change_theme = QtWidgets.QAction('CT', self)
        menu2.addAction(change_theme)
        change_theme.triggered.connect(self.on_change_theme)

    @QtCore.pyqtSlot()
    def on_change_theme(self):
        self.statusBar.showMessage('THEMES')

    def create_toolbar(self):
        tb = self.addToolBar('settings')
        tb.addAction('change')
    
    def create_dockwidget(self):
        lb = QtWidgets.QLabel("hello")
        dw = QtWidgets.QDockWidget()
        #dw.setStyleSheet("""
        #    border: 1px solid teal;
        #    border-radius: 10px;
        #    background-color: rgb(255, 255, 255);
        #"""
        #)
        dw.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        dw.setWidget(lb)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dw)
    
    def create_statusbar(self):
        self.statusBar = QtWidgets.QStatusBar()

        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready!")
        self.statusBar.setStyleSheet("""
        """)



    #def create_layout(self,direction):
    #    if direction == "vr":
    #        self.QVBoxLayout()
    
    def set_layout(self, parent_window, layout):
        parent_window.setLayout(layout)

def open_file_dialog():
        fd = QtWidgets.QFileDialog()
        fd.show()
        print(fd)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    #window = QtWidgets.QWidget()
    #open_file_dialog()
    #layout = QtWidgets.QHBoxLayout()
    #label = QtWidgets.QLabel("TS:")
    #tsinput = QtWidgets.QTextEdit()
    #tsinput.setFixedHeight(40)
    #layout.addWidget(label)
    #layout.addWidget(tsinput)
    #window.setLayout(layout)
    #window.show()
    ui.create_central_widget()
    #vl = ui.create_layout('vr')
    #ui.set_layout(ui.window, vl)
    apply_stylesheet(app, theme='dark_pink.xml')
    ui.setWindowTitle("RURALSYNC")
    ui.show()


    app.exec_()