
from PyQt4 import QtCore, QtGui

class ui_mainwindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self)     
        self.setObjectName("mainwindow")
        self.resize(800,600)
        self.setWindowTitle(QtGui.QApplication.translate("mainwindow", "Python Photo Importer", None, QtGui.QApplication.UnicodeUTF8))       
        
        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        
        self.setCentralWidget(self.centralwidget)
        
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
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
                
        #config tab
        self.config_tab = QtGui.QWidget()
        self.config_tab.setObjectName("config_tab")
        self.config_tab.setSizePolicy(sizePolicy)
        
        #groups tab
        self.groups_tab = QtGui.QWidget()
        self.groups_tab.setObjectName("groups_tab")
        self.groups_tab.setSizePolicy(sizePolicy)
        
        #review tab
        self.review_tab = QtGui.QWidget()
        self.review_tab.setObjectName("review_tab")
        self.review_tab.setSizePolicy(sizePolicy)
        
        #create tabs group
        self.tabs = QtGui.QTabWidget(self.centralwidget)
        self.tabs.setObjectName("tabs")
        self.tabs.setGeometry(QtCore.QRect(5, 0, 791, 553))
        self.tabs.setSizePolicy(sizePolicy)
                
        
        self.tabs.addTab(self.config_tab,"Configuration")
        self.tabs.addTab(self.groups_tab,"Groups")
        self.tabs.addTab(self.review_tab,"Review")
        self.tabs.setCurrentIndex(0) #select which is the default tab
        
    def _enable_actions(self):
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL("activated()"), self.close)
        QtCore.QMetaObject.connectSlotsByName(self)