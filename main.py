import cv2
import numpy as np
import PyQt5
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QFileDialog, QMessageBox, QMainWindow, QAction, \
    qApp, QWidget, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
import time
import serial
import Xaaaaaar
import sys

'''
class VideoViewer(QWidget):
    def __init__(self, parent=None):
        super(VideoViewer, self).__init__(parent)
        self.image = QImage()
        self.setAttribute(Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QImage()

    def initUI(self):
        self.setWindowTitle('Test')

    @pyqtSlot(QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()


class ShowVideo(QObject):
    flag = 0

    camera = cv2.VideoCapture(0)

    ret, image = camera.read()

    height, width = image.shape[:2]

    VideoSignal1 = pyqtSignal(QImage)

    VideoSignal2 = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @pyqtSlot()
    def startVideo(self):
        try:
            print('1')
            global image

            run_video = True
            while run_video:
                ret, image = self.camera.read()
                color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                qt_image1 = QImage(color_swapped_image.data,
                                        self.width,
                                        self.height,
                                        color_swapped_image.strides[0],
                                        QImage.Format_RGB888)
                self.VideoSignal1.emit(qt_image1)

                print('3')
                if self.flag:
                    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    img_canny = cv2.Canny(img_gray, 50, 100)

                    qt_image2 = QImage(img_canny.data,
                                             self.width,
                                             self.height,
                                             img_canny.strides[0],
                                             QImage.Format_Grayscale8)

                    self.VideoSignal2.emit(qt_image2)
                    print('4')


                loop = QEventLoop()
                QTimer.singleShot(25, loop.quit) #25 ms
                loop.exec_()
        except Exception as E:
            print(E)


    @pyqtSlot()
    def canny(self):
        self.flag = 1 - self.flag

'''


class imageViewer(QThread):

    def run(self):
        try:

            pixmap = QPixmap("cycle_" + str(main_gui.cycle_num) + ".png")
            pixmap = pixmap.scaledToHeight(300)
            main_gui.label.setPixmap(pixmap)
            time.sleep(1)
            print("하위 " + str(main_gui.cycle_num))


        except Exception as E:
            print(E)


class Xaar(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.cycle_num = -1

    def initUI(self):
        self.setWindowTitle('Xaar')
        self.resize(600, 500)

        start_btn = QPushButton('start run', self)
        start_btn.move(150, 400)
        start_btn.clicked.connect(self.synthesis)

        streaming_btn = QPushButton('Streaming', self)
        streaming_btn.move(150, 450)
        streaming_btn.clicked.connect(self.streaming)

        print_btn = QPushButton('print', self)
        print_btn.move(450, 400)
        print_btn.clicked.connect(self.printing)

        stop_btn = QPushButton('close', self)
        stop_btn.move(450, 450)
        stop_btn.clicked.connect(self.stop_btn_clicked)

        position = QLabel('position', self)
        position.move(470, 200)

        self.add_position = QLineEdit(self)
        self.add_position.move(450, 250)

        move_btn = QPushButton('move', self)
        move_btn.move(450, 300)
        move_btn.clicked.connect(self.move_btn_clicked)

        # 이미지 추가할 label
        self.label = QLabel('image', self)
        self.label.resize(300, 400)
        self.label.move(50, 0)

        self.show()

    def stop_btn_clicked(self):
        sys.exit()

    def image_load(self, cycle_num):
        print("C1")
        self.viewer = imageViewer()
        self.viewer.start()

    def move_btn_clicked(self):
        current_position = str(self.add_position.text())
        print(current_position)
        print("move")
        Xaaaaaar.moving(current_position)

    def printing(self):

        Xaaaaaar.print_thread()
        self.image_load(self.cycle_num)
        Xaaaaaar.img_num = self.cycle_num

        Xaaaaaar.printing_state = True

    # 이거는 webcam 쓰는거
    def streaming(self):
        cam = cv2.VideoCapture(0)
        cam.set(3, 1280)  # CV_CAP_PROP_FRAME_WIDTH
        cam.set(4, 720)  # CV_CAP_PROP_FRAME_HEIGHT
        # cam.set(5,0) #CV_CAP_PROP_FPS

        while True:
            ret_val, img = cam.read()  # 캠 이미지 불러오기

            cv2.imshow("Cam Viewer", img)  # 불러온 이미지 출력하기

            key = cv2.waitKey(1);
            if key == ord('q'):
                break

            elif key == ord('s'):
                file = datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S") + '.jpg'
                cv2.imwrite(file, img)
                print(file, ' saved')
                cam.release()
                cv2.destroyAllWindows()

        for i in range(0, 3):
            pixmap = QPixmap("bogum" + str(i) + ".jpg")
            pixmap = pixmap.scaledToHeight(300)
            self.label.setPixmap(pixmap)
            time.sleep(3)

    # 이거는 라즈베리파이 스트리밍화면 불러오는 거
    def streamer(self):

        cap = cv2.VideoCapture("http://192.168.0.28:8091/?action=stream")

        while (True):
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()

        cv2.destroyAllWindows()

    def synthesis():
        for i in range(0, self.oligo_size):  # oligo_size :합성하려는 oligo 길이
            self.cycle_num = i
            # Deblock 하는 함수

            # coupling하는 함수
            self.printing(self.cycle_num)

            # oxidation하는 함수


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # streaming = ShowVideo()

    main_gui = Xaar()

    sys.exit(app.exec_())
