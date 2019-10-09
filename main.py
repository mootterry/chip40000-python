# This Python file uses the following encoding: utf-8
import sys

from PySide2.QtCore import QPointF, Qt
from PySide2.QtGui import QColor, QImage
from PySide2.QtWidgets import QApplication, QWidget, QSplitter, QGraphicsScene, QHBoxLayout

from chip import Chip
from view import View

import rc_images


class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.scene = None
        self.populateScene()

        self.h1Splitter = QSplitter()
        self.h2Splitter = QSplitter()

        vSplitter = QSplitter()
        vSplitter.setOrientation(Qt.Vertical)
        vSplitter.addWidget(self.h1Splitter)
        vSplitter.addWidget(self.h2Splitter)

        view = View("Top left view", self)
        view.view().setScene(self.scene)
        self.h1Splitter.addWidget(view)

        view = View("Top right view", self)
        view.view().setScene(self.scene)
        self.h1Splitter.addWidget(view)

        view = View("Bottom left view", self)
        view.view().setScene(self.scene)
        self.h2Splitter.addWidget(view)

        view = View("Bottom right view", self)
        view.view().setScene(self.scene)
        self.h2Splitter.addWidget(view)

        layout = QHBoxLayout()
        layout.addWidget(vSplitter)
        self.setLayout(layout)

        self.setWindowTitle(self.tr("Chip Example"))

    def populateScene(self):

        self.scene = QGraphicsScene(self)

        image = QImage(":/qt4logo.png")
        xx: int = 0
        nitems: int = 0
        for i in range(-11000, 11000, 110):
            xx += 1
            yy: int = 0
            for j in range(-7000, 7000, 70):
                yy += 1
                x = (i + 11000) / 22000.0
                y = (j + 7000) / 14000.0

                color = QColor(image.pixel(int(image.width() * x), int(image.height() * y)))
                item = Chip(color, xx, yy)
                item.setPos(QPointF(i, j))
                self.scene.addItem(item)
                nitems += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
