'''
Created on Oct 19, 2009

@author: alex
'''

import sys
from PyQt4 import QtCore, QtGui

#from mainwindow_ui import Ui_main_window
from about_dialog import ui_about_dialog
from mainwindow import ui_mainwindow

class MyForm(ui_mainwindow):
    def __init__(self, parent = None):
        ui_mainwindow.__init__(self, parent)

        #extra slots and signals, that are not embedded in main window
        QtCore.QObject.connect(self.actionAbout, QtCore.SIGNAL("activated()"), self.show_about)
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def show_about(self):
        about = ui_about_dialog(self)
        about.show()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())