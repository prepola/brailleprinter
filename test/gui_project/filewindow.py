import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

class Ui_Dialog(object):
    def __init__(self, mode, fontsize):
        self.mainDialog = QtWidgets.QDialog()
        self.mainDialog.resize(1024, 600)
        self.mainDialog.setWindowTitle("음성인식 점자프린터")
        
        # Layout
        self.mainLayout = QtWidgets.QGridLayout() # Buttons
        self.mainLayout_2 = QtWidgets.QGridLayout() # mainInfo and spacer
        self.mainLayout_3 = QtWidgets.QGridLayout() # workTable and listView
        self.mainLayout_4 = QtWidgets.QGridLayout(self.mainDialog) # mainLayout and mainLayout_2
        self.mainLayout.setContentsMargins(75, 0, 75, 50)
        self.mainLayout_3.setContentsMargins(75, 0, 75, 0)
        self.mainLayout_4.addLayout(self.mainLayout_2, 0, 0, 1, 1)
        self.mainLayout_2.setContentsMargins(20, 30, 20, 30)
        self.mainLayout_4.addLayout(self.mainLayout_3, 1, 0, 1, 1)
        self.mainLayout_4.addLayout(self.mainLayout, 2, 0, 1, 1)

        # Button
        self.mainBtnlist = [QtWidgets.QPushButton()] * 4
        for i in range(4):
            self.mainBtnlist[i] = QtWidgets.QPushButton(self.mainDialog)
            self.mainBtnlist[i].setMinimumSize(QtCore.QSize(300, 75))
            self.mainBtnlist[i].setStyleSheet('font-size:'+str(fontsize)+'px;')
            self.mainLayout.addWidget(self.mainBtnlist[i], int(i//2), int(i%2), 1, 1)

        # mainInfo
        self.mainInfo = QtWidgets.QTextBrowser(self.mainDialog)
        self.mainInfo.setMinimumSize(QtCore.QSize(0, 45))
        self.mainInfo.setMaximumSize(QtCore.QSize(500, 45))
        self.mainInfo.setStyleSheet('font-size:'+str(fontsize)+'px;')
        self.mainLayout_2.addWidget(self.mainInfo, 0, 0, 1, 1)

        #listView
        self.itemList = os.listdir('C://')
        self.listView = QtWidgets.QListView()
        self.model = QtGui.QStandardItemModel()
        for item in self.itemList:
            self.model.appendRow(QtGui.QStandardItem(item))
        self.listView.setModel(self.model)
        self.listView.setStyleSheet('font-size:'+str(fontsize)+'px;')
        self.mainLayout_3.addWidget(self.listView, 0, 0, 1, 1)

        QtCore.QMetaObject.connectSlotsByName(self.mainDialog)
        self.mainDialog.show()
    
    def refresh_ui(self, text_list, ints):
        for i in range(5):
            if i == 0 : self.mainInfo.setText(text_list[i])          
            else : self.mainBtnlist[i-1].setText(text_list[i])
        print(ints, text_list[0])

def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog("extend",30)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()