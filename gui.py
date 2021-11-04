import sys
import math

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from qt_material import apply_stylesheet


alignments = {
    'top': QtCore.Qt.AlignTop,
    'bottom': QtCore.Qt.AlignBottom,
    'left': QtCore.Qt.AlignLeft,
    'right': QtCore.Qt.AlignRight,
}


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.vbox = QtWidgets.QVBoxLayout
        self.hbox = QtWidgets.QHBoxLayout
        self.Tree = QtWidgets.QTreeView()
        self.width = 0
        self.height = 0
        self.center_frame = QtWidgets.QFrame()
        self.splitter = QtWidgets.QSplitter(self.center_frame)
        self.mediaview = QtWidgets.QListView()
        self.create_central_widget()
        self.statusBar = None
        self.create_menu()
        self.setFixedSize(self.get_geom(0.75))
    
    def get_geom(self, factor=1):
        geom = QtCore.QRect(QtWidgets.QDesktopWidget().availableGeometry(self))
        geom = QtCore.QSize(math.ceil(geom.width() * factor), math.ceil(geom.height() * factor))
        return geom
        


    def create_central_widget(self):
        self.setCentralWidget(self.center_frame)

    @QtCore.pyqtSlot()
    def on_change_theme(self):
        self.statusBar.showMessage('THEMES')

    def create_menu(self):
        menu1 = self.menuBar().addMenu('Menu')
        open_file_dialog = QtWidgets.QAction('Open Folder', self)
        menu1.addAction(open_file_dialog)
        open_file_dialog.triggered.connect(self.open_file_dialog)

        menu1.addAction('Preference')
        menu2 = self.menuBar().addMenu("Themes")
        change_theme = QtWidgets.QAction('CT', self)
        menu2.addAction(change_theme)
        change_theme.triggered.connect(self.on_change_theme)

    @QtCore.pyqtSlot()
    def open_file_dialog(self):
        fd = QtWidgets.QFileDialog()
        fd.FileMode(fd.DirectoryOnly)
        fd.Option(fd.DontUseNativeDialog | fd.ShowDirsOnly)
        folder = fd.getExistingDirectory(None, "Select Directory")
        folder = str(folder)
        files = QtCore.QDir(folder)
        filters = files.Filter(files.Files | files.NoDotAndDotDot)
        lists = files.entryInfoList(filters)
        files_any = map(lambda i: i.fileName(), lists)
        files_ts = filter(lambda any: any.endswith('.ts'), files_any)
        model = QtCore.QStringListModel(files_ts)
        self.mediaview.setGridSize(self.mediaview.gridSize())
        self.mediaview.ViewMode(self.mediaview.ListMode)
        self.mediaview.Flow(self.mediaview.LeftToRight)
        self.mediaview.Movement(self.mediaview.Snap)
        self.mediaview.setModel(model)

    def create_toolbar(self):
        tb = self.addToolBar('settings')
        tb.addAction('change')
    
    def set_layout(self, layout):
        self.central_layout = layout
        self.central_frame.setLayout(layout)
    
    def create_dockwidget(self, widget_holder):
        dw = QtWidgets.QDockWidget()
        dw.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        dw.setWidget(widget_holder)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dw)
    
    def create_statusbar(self):
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready!")

class PlaceHolder(QtWidgets.QWidget):
    def __init__(self, layout, parent=None, alignment='top'):
        super(PlaceHolder, self).__init__(parent)
        self.layout = layout
        self.alignment = alignment

    def place_element(self, widget):
        self.layout.addWidget(widget,alignment=alignments[self.alignment])
        self.setLayout(self.layout)

class MediaList(QtWidgets.QTreeView):
    def __init__(self):
        super(MediaList,self).__init__()

    def clicked(self, item):
        pass


def btn_cliked(self):
    self.statusBar.showMessage('btn_clicked')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    layers_frame = PlaceHolder(None)
    main = MainWindow()
    layers_splitter_frame = QtWidgets.QSplitter(QtCore.Qt.Vertical ,layers_frame)


    #main.central_layout = main.hbox(main.central_frame)
    layer_a_group = QtWidgets.QGroupBox("Layer A (1 Seg)")
    layer_a_layout = main.vbox()

    layer_b_group = QtWidgets.QGroupBox("Layer B (12 Seg)")
    layer_b_layout = main.vbox()

    ts_group = QtWidgets.QGroupBox('TS Files')
    ts_group.setFixedSize(main.get_geom(0.1))
    ts_group_layout = main.vbox()

    layer_a_frame = QtWidgets.QFrame()
    layer_a_frame.setMinimumSize(main.get_geom(0.2))
    layer_a_loop = QtWidgets.QCheckBox('loop')
    layer_a_layout.addWidget(layer_a_frame)
    layer_a_layout.addWidget(layer_a_loop)
    layer_b_loop = QtWidgets.QCheckBox('loop')
    layer_b_frame = QtWidgets.QFrame()
    layer_b_frame.setMinimumSize(main.get_geom(0.2))
    layer_b_layout.addWidget(layer_b_frame)
    layer_b_layout.addWidget(layer_b_loop)

    layer_a_group.setLayout(layer_a_layout)
    layer_b_group.setLayout(layer_b_layout)
  
    media = PlaceHolder(main.vbox())

    ts_group_layout.addWidget(main.mediaview)

    layers_splitter_frame.addWidget(layer_a_group)
    layers_splitter_frame.addWidget(layer_b_group)

    form = QtWidgets.QFormLayout()
    form.addRow("ts", QtWidgets.QLineEdit())
    form.addRow("Frequency", QtWidgets.QLineEdit())
    form.addRow("Bandwidth", QtWidgets.QComboBox())
    left_dock = QtWidgets.QFrame()
    left_dock.setLayout(form)
    dockwidget = PlaceHolder(main.vbox())
    dockwidget.setMinimumWidth(main.get_geom(0.18).width())
    dockwidget.place_element(left_dock)

    #main.splitter.addWidget(ts_group)
    main.splitter.addWidget(layers_splitter_frame)

    main.create_dockwidget(dockwidget)
    main.create_statusbar()
    apply_stylesheet(app, theme='dark_pink.xml')
    main.setWindowTitle("RURALSYNC")
    main.show()

    app.exec_()
