import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

from mainwindow import Ui_Dialog as mainDialog
from printwindow import Ui_Dialog as printDialog
from extendwindow import Ui_Dialog as extendDialog

def main():
    place_display = mainDialog
    next_mode = 'main'
    app = QtWidgets.QApplication(sys.argv)

    change_display = {
        'print':printDialog,
        'extend':extendDialog,
        'main':mainDialog
    }

    while 1:
        ui = place_display(next_mode, 30)
        app.exec_()
        next_mode = ui.mode
        print(next_mode, '로 화면이 전환됩니다.')

        place_display = change_display.get(ui.mode, place_display['main'])

if __name__ == '__main__':
    main()