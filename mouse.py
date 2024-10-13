import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage, QCursor
from PyQt5.QtCore import Qt, QTimer
from PIL import ImageGrab, Image

class MouseLupa(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.label = QLabel(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateMagnifier)
        self.timer.start(100)
        self.showFullScreen()

    def updateMagnifier(self):
        cursor_pos = QCursor.pos()
        x, y = cursor_pos.x(), cursor_pos.y()
        r = 50  # Radius of the magnifier
        bbox = (x - r, y - r, x + r, y + r)
        img = ImageGrab.grab(bbox=bbox)
        img = img.resize((300, 300), Image.BICUBIC)  # Adjust the zoom level
        img = img.resize((300, 300), Image.NEAREST)  # Keep the zoom level static
        qimage = QImage(img.tobytes(), img.width, img.height, img.width * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        self.label.setPixmap(pixmap)
        self.label.setGeometry(x, y, 400, 400)  # Center the magnifier

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MouseLupa()
    sys.exit(app.exec_())
