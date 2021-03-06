import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt

# from python_raspberry import display
from python_raspberry.display import generate_display

#ㅡㅡㅡㅡㅡㅡㅡㅡㅡ
#| btn_1 | btn_2 |
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡ
#| btn_3 | btn_4 |
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡ

#test
gui_textlist = {
        'error':["프로그램 재시작 필요", "-", "-", "-", "-"],
        'main':["메인 화면", "음성인식 프린트\n시작", '음성 재안내', "녹음된 음성파일을 이용하여\n프린트", "문서 파일을 이용하여\n프린트"],
        'print_main':["프린트", "새로 기록", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        'record_main':["녹음파일로 기록", "새로 기록", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"],
        'doc_main':["문서파일의 내용을 기록", "문서 선택", "음성 재안내", "기존파일에 이어서 기록", "뒤로가기"]
}

class Ui_Dialog(generate_display):
    def __init__(self, mode, fontsize, title=None):
        super().__init__(mode, fontsize)
        self.set_buttonsize()
        self.set_layout()
        self.refresh_ui(gui_textlist['main'])
        self.set_mode('main')
        
        @self.make_voice_btn
        def btn_1_func(self) :
            if self.get_mode() == 'main':
                self.set_mode('print_main')
                self.refresh_ui(gui_textlist[self.get_mode()])
            elif self.get_mode() == 'print_main':
                self.mode = 'print'
                self.mode_script = ''
                self.mainDialog.close()
            elif self.get_mode() == 'record_main':
                self.mode = 'extend'
                self.mode_script = ''
                self.mainDialog.close()
        
        @self.make_voice_btn
        def btn_2_func(self) :
            self.call_voice = self.mode_script
            self.make_voice()

        @self.make_voice_btn
        def btn_3_func(self) :
            if self.get_mode() == 'main':
                self.set_mode('record_main')
                self.refresh_ui(gui_textlist[self.get_mode()])
            elif self.get_mode() == 'record_main':
                self.set_mode('extend')
                self.mainDialog.close()
        
        @self.make_voice_btn
        def btn_4_func(self) :
            if self.get_mode() == 'main':
                self.set_mode('doc_main')
                self.refresh_ui(gui_textlist[self.get_mode()])
            elif self.get_mode() == 'doc_main':
                self.set_mode('extend')
                self.mainDialog.close()
            elif self.get_mode() != 'main':
                self.set_mode('main')
                self.refresh_ui(gui_textlist[self.get_mode()])

        self.btn_1 = btn_1_func
        self.btn_2 = btn_2_func
        self.btn_3 = btn_3_func
        self.btn_4 = btn_4_func

        self.set_clickevent(self.btn_1, self.btn_2, self.btn_3, self.btn_4)

    def set_buttonsize(self) :
        for i in range(4) :
            self.mainBtn[i].setMinimumSize(QtCore.QSize(300, 175))
            
    def set_layout(self):
        self.mainLayout_2.setContentsMargins(250, 30, 250, 30)
        self.mainLayout_4.addLayout(self.mainLayout, 1, 0, 1, 1)



def main():
    app = QtWidgets.QApplication(sys.argv)
    mui = Ui_Dialog('main', 30)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()