
from PyQt4 import QtCore, QtGui

class ui_mainwindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self)     
        self.setObjectName("mainwindow")
        self.resize(800,600)
        self.setWindowTitle(QtGui.QApplication.translate("mainwindow", "Python Photo Importer", None, QtGui.QApplication.UnicodeUTF8))
        self.setMinimumSize(QtCore.QSize(640, 480))       
                
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")   
        self.setCentralWidget(self.centralwidget)
        
        self.main_layout = QtGui.QVBoxLayout(self.centralwidget)
        
        self._add_menubar()
        self._add_statusbar()
        self._add_tabs()
        self._enable_actions()
        
    def _add_menubar(self):
        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QtCore.QRect(0,0,800, 23))
        
        #File menu actions (entries):
        self.actionQuit = QtGui.QAction(self)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.setText("Quit")
        self.actionQuit.setToolTip("Quit Application")
        self.actionQuit.setShortcut("Ctrl+Q")
        self.actionQuit.setIcon(QtGui.QIcon('icons/exit.png'))
        
        #File menu
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle("File")
        #self.menuFile.setTitle(QtGui.QApplication.translate("mainwindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.addAction(self.actionQuit)
        
        #About menu actions (entries):
        self.actionAbout = QtGui.QAction(self)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setText("About")
        
        #About menu        
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuAbout.setTitle("About")
        self.menuAbout.addAction(self.actionAbout)
        
        #add menus to the menubar
        self.menubar.addMenu(self.menuFile)
        self.menubar.addMenu(self.menuAbout)
        
        #add actions to menubar - is it necessary?
        #self.menubar.addAction(self.menuFile.menuAction())
        
        #add menubar to the main window
        self.setMenuBar(self.menubar)
        
    def _add_statusbar(self):
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setSizeGripEnabled(1)
        self.setStatusBar(self.statusbar)
        
    def _add_tabs(self):
                
        #config tab
        self.config_tab = QtGui.QWidget()
        self.config_tab.setObjectName("config_tab")
        self._build_config_tab()
        
        #groups tab
        self.groups_tab = QtGui.QWidget()
        self.groups_tab.setObjectName("groups_tab")
        
        #review tab
        self.review_tab = QtGui.QWidget()
        self.review_tab.setObjectName("review_tab")
        
        #create tabs group
        self.tabs = QtGui.QTabWidget(self.centralwidget)
        self.tabs.setObjectName("tabs")
        #self.tabs.setStyleSheet("background-color: #111111")
                
        
        self.tabs.addTab(self.config_tab,"Configuration")
        self.tabs.addTab(self.groups_tab,"Groups")
        self.tabs.addTab(self.review_tab,"Review")
        self.tabs.setCurrentIndex(0) #select which is the default tab
        self.main_layout.addWidget(self.tabs)
        
    def _build_config_tab(self):
        
        #create widgets for each group
        self.config_tab_input_widget = QtGui.QWidget(self.config_tab)
        self.config_tab_input_widget.setObjectName("config_tab_input_widget")
        
        self.config_tab_output_widget = QtGui.QWidget(self.config_tab)
        self.config_tab_output_widget.setObjectName("config_tab_output_widget")
        
        #set the tab main layout
        self.config_tab_layout = QtGui.QVBoxLayout(self.config_tab)
        self.config_tab_layout.addItem(QtGui.QSpacerItem(0,40))  
        self.config_tab_layout.addWidget(self.config_tab_input_widget)
        self.config_tab_layout.addWidget(self.config_tab_output_widget)
        self.config_tab_layout.addItem(QtGui.QSpacerItem(0,0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))

        #set the layout for each widget
        self.input_source_layout = QtGui.QHBoxLayout(self.config_tab_input_widget)
        self.input_source_layout.setObjectName("input_source_layout")
        
        self.output_source_layout = QtGui.QHBoxLayout(self.config_tab_output_widget)
        self.output_source_layout.setObjectName("output_source_layout")

        #create elements for input widget
        self.input_source_label = QtGui.QLabel(self.config_tab_input_widget)
        self.input_source_label.setObjectName("input_source_label")
        self.input_source_label.setText("Source folder:")   
        self.input_source_label.setMinimumWidth(120)   
        
        self.input_source_text = QtGui.QLineEdit(self.config_tab_input_widget)
        self.input_source_text.setObjectName("input_source_text")
        #self.input_source_text.setMinimumSize(QtCore.QSize(420, 0))
        
        self.input_source_cmd = QtGui.QToolButton(self.config_tab_input_widget)
        self.input_source_cmd.setObjectName("input_source_cmd")
        self.input_source_cmd.setText("...")
        
        #create elements for output widget
        self.output_source_label = QtGui.QLabel(self.config_tab_output_widget)
        self.output_source_label.setObjectName("output_source_label")
        self.output_source_label.setText("Destination folder:")
        self.output_source_label.setMinimumWidth(120)      
        
        self.output_source_text = QtGui.QLineEdit(self.config_tab_output_widget)
        self.output_source_text.setObjectName("output_source_text")
        #self.output_source_text.setMinimumSize(QtCore.QSize(420, 0))
        
        self.output_source_cmd = QtGui.QToolButton(self.config_tab_output_widget)
        self.output_source_cmd.setObjectName("output_source_cmd")
        self.output_source_cmd.setText("...")
        
        
        
        #add elements to each widget
        self.input_source_layout.addWidget(self.input_source_label)
        self.input_source_layout.addWidget(self.input_source_text)
        self.input_source_layout.addWidget(self.input_source_cmd)
        
        self.output_source_layout.addWidget(self.output_source_label)
        self.output_source_layout.addWidget(self.output_source_text)
        self.output_source_layout.addWidget(self.output_source_cmd)
        
    def _get_input_folder_path(self):
        fd = QtGui.QFileDialog(self)
        self.input_source_text.setText(fd.getExistingDirectory())
        
        
    def _enable_actions(self):
        QtCore.QObject.connect(self.input_source_cmd, QtCore.SIGNAL("clicked()"), self._get_input_folder_path)
        QtCore.QMetaObject.connectSlotsByName(self)