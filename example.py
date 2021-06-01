#코드 구성요소 호출
#PyQt5.QtWidgets는 기본적인 UI 구성요소를 제공하는 위젯을 보유
#아이콘은 QtGui
#내부의 element를 이용하기 위해서는 QtCore가 필요함

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMainWindow, QAction, \
    qApp, QDesktopWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QGridLayout, QCheckBox, \
    QRadioButton, QComboBox, QProgressBar
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import  QCoreApplication, QDateTime, Qt, QBasicTimer

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30,40,200,25)

        self.btn = QPushButton('Start', self)
        self.btn.move(40,80)
        self.btn.clicked.connect(self.doAction)

        self.timer = QBasicTimer()
        self.step = 0

        self.setWindowTitle('Window')
        self.setGeometry(300,300,300,200)
        self.show()

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            reture

        self.step = self.step + 2
        self.pbar.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')

        else:
            self.timer.start(100, self)
            self.btn.setText('Stop')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

