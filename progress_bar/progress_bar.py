import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class WorkerThread(QThread):
    update_progress = pyqtSignal(int)

    def run(self):
        for j in range(20, 101, 20):
            print(j)
            time.sleep(2)
            self.update_progress.emit(j)


class DlgMain(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My GUI')

        self.progressbar = QProgressBar()
        self.progressbar.setStyle(QStyleFactory.create('Windows'))
        self.progressbar.setTextVisible(True)

        self.buttonStart = QPushButton('Start')
        self.buttonStart.clicked.connect(self.event_buttonStart_clicked)

        self.slider = QSlider()
        self.lcd = QLCDNumber()
        self.slider.valueChanged.connect(self.lcd.display)

        self.lytLCD = QHBoxLayout()
        self.lytLCD.addWidget(self.slider)
        self.lytLCD.addWidget(self.lcd)

        self.lytMain = QVBoxLayout()
        self.lytMain.addWidget(self.progressbar)
        self.lytMain.addWidget(self.buttonStart)
        self.lytMain.addLayout(self.lytLCD)
        self.setLayout(self.lytMain)

    def event_buttonStart_clicked(self):
        self.worker = WorkerThread()
        self.worker.start()
        self.worker.finished.connect(self.event_worker_finished)
        self.worker.update_progress.connect(self.event_update_progress)

    def event_worker_finished(self):
        QMessageBox.information(self, 'Done!', 'Worker thread complete')

    def event_update_progress(self, val):
        self.progressbar.setValue(val)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())
