'''
Created on Oct 19, 2009

@author: alex
'''

from PyQt4 import QtCore, QtGui

class ui_about_dialog(QtGui.QDialog):
    '''
    The about dialog
    '''
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setObjectName("about_dialog")
        self.resize(280, 180)
        self.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(30, 140, 230, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("button_box")
        
        self.setWindowTitle(QtGui.QApplication.translate("about_dialog", "About Pymporter", None, QtGui.QApplication.UnicodeUTF8))
        
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("clicked(QAbstractButton*)"), self.close)
        #QtCore.QMetaObject.connectSlotsByName(about_dialog)
        