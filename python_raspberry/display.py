import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import json
import itertools

from python_raspberry import tts

color_code = 'orangeA'
color_data = json.load(open('python_raspberry/colordata.json', 'r'))
font_color = '#000000' if color_code in ['cyanA', 'greenA', 'lightgreen', 'lightgreenA', 'lime', 'limeA', 'yellow', 'yellowA', 'amber', 'amberA', 'orange', 'orangeA', 'bw'] else '#FFFFFF'
back_color = color_data.get(color_code, color_data['gray'])
debug = True

script = {
        'duplicate':'중복되는 파일이 존재합니다.\n다시 시도해주십시요.',
        'start':'안녕하세요\n입력시작 버튼을 누르면 입력을 시작합니다.',
        'readytitle':'기록을 시작하기전에 제목을 입력해야 합니다.\n준비가 되었다면 좌측 상단 버튼을 눌러 제목을 입력해주세요.',
        'readybody':'본문 입력을 시작합니다.\n좌측 상단 버튼을 눌러 기록을 시작해 주십시오',
        'readyrecord':'해당파일로 입력을 시작합니다.',
        'fatal':'음성인식을 실행할 수 없습니다.\ncredential path 및 Google Cloud Platform console을 확인해주세요.\n입력종료 버튼을 누르면 프린트과정이 종료됩니다.',
        'overtime':'입력 시간이 초과하였거나 입력에 실패하였습니다.\n다시 시도해주십시요.',
        'isright':'다음 내용이 맞습니까?',
        'commit':'입력되었습니다. 다음줄로 이동합니다.',
        'end_not_save':'현재 진행하던 내용이 저장되지 않습니다. 종료하시려면 버튼을 한번 더 입력해 주세요',
        'end':'종료하시려면 버튼을 한번 더 입력해 주세요',
        'empty_title':'아무 내용도 입력되어 있지 않습니다. 먼저 입력시작 버튼으로 입력을 시작해주세요',
        'empty_body':'현재 본문으로 아무 내용도 입력되어 있지 않습니다. 제목을 바꾸시려면 버튼을 한번 더 입력해주세요',
        'delete_guide_1':'방금 입력하신 내용',
        'delete_guide_2':'을 삭제합니다. 삭제 하시려면 버튼을 한번 더 입력해주세요.',
        'delete_process':'삭제가 진행중입니다. 잠시만 기다려 주십시오.',
        'delete_failed':'해당 내용이 이미 인쇄 대기열에 포함되어 삭제할 수 없습니다.',
        'delete_comp':'성공적으로 삭제 되었습니다.',
        'text_error':'스크립트를 읽을 수 없습니다. 스크립트 파일을 확인해주세요'
}

btn_1_script={
    'main':'음성 프린트를 진행하는 버튼입니다. 음성 프린트 실행을 위해 버튼을 한번 더 눌러주세요.',
    'print_main':'새로운 파일로 기록합니다. 새 파일로 시작을 위해 버튼을 한번 더 눌러주세요.',
    'record_main':'새로운 파일로 기록합니다. 새 파일로 시작을 위해 버튼을 한번 더 눌러주세요.',
    'doc_main':'새로운 파일로 기록합니다. 새 파일로 시작을 위해 버튼을 한번 더 눌러주세요.'
}
btn_2_script={
    'main':'재안내 버튼입니다.',
    'print_main':'재안내 버튼입니다.'
}
btn_3_script={
    'main':'녹음 프린트를 진행하는 버튼입니다. 녹음 프린트 실행을 위해 버튼을 한번 더 눌러주세요.',
    'print_main':'기존 파일에 이어서 기록합니다. 기존 파일로 시작을 위해 버튼을 한번 더 눌러주세요.',
    'record_main':'기존 파일에 이어서 기록합니다. 기존 파일로 시작을 위해 버튼을 한번 더 눌러주세요.',
    'doc_main':'기존 파일에 이어서 기록합니다. 기존 파일로 시작을 위해 버튼을 한번 더 눌러주세요.'
}
btn_4_script={
    'main':'문서 프린트를 진행하는 버튼입니다. 문서 프린트 실행을 위해 한번 더 눌러주세요.',
    'print_main':'현재 선택을 취소하고 뒤로 돌아갑니다. 뒤로 가기 위해 한번 더 눌러주세요.',
    'record_main':'현재 선택을 취소하고 뒤로 돌아갑니다. 뒤로 가기 위해 한번 더 눌러주세요.',
    'doc_main':'현재 선택을 취소하고 뒤로 돌아갑니다. 뒤로 가기 위해 한번 더 눌러주세요.'
}

btn_script_connect = {
    'btn_1_func':btn_1_script,
    'btn_2_func':btn_2_script,
    'btn_3_func':btn_3_script,
    'btn_4_func':btn_4_script,
    'error':'error'
} 

mode_info_script ={
    'main':'음성 인식 점자 프린터 입니다. 각각의 버튼을 눌러 기능을 확인하시고 원하시는 기능을 선택하여 주십시오. 다시 들으시려면 우측 상단 버튼을 눌러주세요',
    'print_main':'음성 프린트에 진입하셨습니다. 이곳에서 음성으로 점자를 기록 할 수 있습니다. 각각의 버튼을 눌러 기능을 확인할 수 있고 다시 들으시려면 우측 상단 버튼을 눌러주세요',
    'record_main':'녹음 프린트에 진입하셨습니다. 이곳에서 녹음 파일을 점자로 변환 할 수 있습니다. 각각의 버튼을 눌러 기능을 확인할 수 있고 다시 들으시려면 우측 상단 버튼을 눌러주세요',
    'doc_main':'문서 프린트에 진입하셨습니다. 이곳에서 문서를 점자로 변환 할 수 있습니다. 각각의 버튼을 눌러 기능을 확인할 수 있고 다시 들으시려면 우측 상단 버튼을 눌러주세요',
    'extend':'파일 브라우저입니다. 이곳에서 파일을 선택 할 수 있습니다. 좌측 상단 버튼과 좌측 하단 버튼으로 아이템을 선택 할 수 있고 결정하시려면 우측 상단 버튼을 눌러주세요',
    'print':''
}

class generate_display(QtWidgets.QDialog):
    def __init__(self, mode, fontsize, parent=None):
        super(generate_display, self).__init__(parent)
        self.fontsize = str(fontsize)
        self.mode = mode
        self.font_color = font_color
        self.back_color = back_color
        self.debug = debug
        self.play_voice = None
        self.current_voice = str()
        self.call_voice = str()
        self.mode_script = ''
        self.sel_item = str()

        self.mainDialog = QtWidgets.QDialog()
        self.mainDialog.resize(1024, 600)
        self.mainDialog.setWindowTitle("음성인식 점자프린터")
        self.mainDialog.setStyleSheet(
                'background: '+ self.back_color[3] +';'
                )

        # Layout
        self.mainLayout = QtWidgets.QGridLayout() # Buttons
        self.mainLayout_2 = QtWidgets.QGridLayout() # mainInfo and spacer
        self.mainLayout_3 = QtWidgets.QGridLayout() # workTable and listView
        self.mainLayout_4 = QtWidgets.QGridLayout(self.mainDialog) # mainLayout and mainLayout_2
        self.mainLayout.setContentsMargins(75, 0, 75, 50)
        self.mainLayout_3.setContentsMargins(75, 0, 75, 0)
        self.mainLayout_4.addLayout(self.mainLayout_2, 0, 0, 1, 1)

        # Button
        self.mainBtn = [QtWidgets.QPushButton()] * 4
        for i in range(4):
            self.mainBtn[i] = QtWidgets.QPushButton(self.mainDialog)
            self.mainBtn[i].setStyleSheet(
                'color:'+ self.font_color +';' +
                'font-size:'+ self.fontsize +'px;' +
                'background: '+ self.back_color[0] +';' +
                'border-radius: 10px'
                )
            self.mainLayout.addWidget(self.mainBtn[i], int(i//2), int(i%2), 1, 1)

        # mainInfo
        self.mainInfo = QtWidgets.QTextBrowser(self.mainDialog)
        self.mainInfo.setMinimumSize(QtCore.QSize(0, 45))
        self.mainInfo.setMaximumSize(QtCore.QSize(500, 45))
        self.mainInfo.setStyleSheet(
                'font-size:'+ self.fontsize +'px;' +
                'background: '+ self.back_color[1] +';' +
                'border-radius: 10px'
                )
        self.mainLayout_2.addWidget(self.mainInfo, 0, 0, 1, 1)
        
        QtCore.QMetaObject.connectSlotsByName(self.mainDialog)
        # self.mainDialog.show() 
        self.mainDialog.showFullScreen()       

    def set_clickevent(self, *args):
        for i in range(4):
            self.mainBtn[i].clicked.connect(args[i])

    def get_mode(self):
        print('getmode: {}'.format(self.mode))
        return self.mode
    
    def set_mode(self, mode):
        if self.debug : print('<', __name__, '>', 'set_mode:', mode)
        self.mode = mode
        self.current_func = None
        self.call_voice = self.mode_script = mode_info_script.get(self.mode, 'error')
        self.make_voice()

    def set_infotext(self, data):
        if self.debug : print('<', __name__, '>', 'set_infotext:', data)
        if len(self.workTable.toPlainText()) < 1 :
            self.workTable.setText(data)
        else:
            self.workTable.append(data)

    def refresh_ui(self, text_list):
        if self.debug : print('<', __name__, '>', 'refresh_ui:', text_list)
        for i in range(5):
            if i == 0 : self.mainInfo.setText(text_list[i])          
            else : self.mainBtn[i-1].setText(text_list[i])

    def make_voice(self):
        if self.play_voice is not None:
            self.play_voice.stop()
            self.play_voice = None
        if self.call_voice != '':
            if self.call_voice in script:
                self.current_voice = script.get(self.call_voice, script['text_error'])
                self.play_voice = tts.run_voice(script.get(self.call_voice, script['text_error']))
            else:
                self.current_voice = self.call_voice
                self.play_voice = tts.run_voice(self.call_voice)
            self.play_voice.start()

    def make_voice_btn(self, func):
        self.run_flag = itertools.cycle([False, True]).__next__
        self.current_func = None
        def voice():
            if func.__name__ == 'btn_2_func':
                self.current_func = func.__name__
                func(self)
            else:
                if self.current_func == func.__name__:
                    func(self)
                    self.call_voice = self.mode_script
                    self.make_voice()
                else:
                    self.current_func = func.__name__
                    print('play:{}, call:{}, curr:{}'.format(self.play_voice, self.call_voice, self.current_voice))
                    self.call_voice = btn_script_connect.get(self.current_func, 'error connect').get(self.mode, 'error script')
                    self.make_voice()
        return voice

    
def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = generate_display('main',30)
    sys.exit(app.exec_())
    pass

if __name__ == "__main__":
    main()