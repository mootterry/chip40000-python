# This Python file uses the following encoding: utf-8
import sys

from PySide2.QtCore import QPointF, Qt
from PySide2.QtGui import QColor, QImage
from PySide2.QtWidgets import QApplication, QWidget, QSplitter, QGraphicsScene, QHBoxLayout

from chip import Chip
from view import View

import images


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.populateScene(self.scene)
        h1Splitter = QSplitter()
        h2Splitter = QSplitter()
        vSplitter = QSplitter()
        vSplitter.setOrientation(Qt.Vertical)
        vSplitter.addWidget(h1Splitter)
        vSplitter.addWidget(h2Splitter)

        view = View("Top left view",self)
        view.view().setScene(self.scene)
        h1Splitter.addWidget(view)

        view = View("Top right view",self)
        view.view().setScene(self.scene)
        h1Splitter.addWidget(view)

        view = View("Bottom left view",self)
        view.view().setScene(self.scene)
        h2Splitter.addWidget(view)

        view = View("Bottom right view",self)
        view.view().setScene(self.scene)
        h2Splitter.addWidget(view)

        layout = QHBoxLayout()
        layout.addWidget(vSplitter)
        self.setLayout(layout)
        self.setWindowTitle(self.tr("Chip Example"))

    def populateScene(self, scene: QGraphicsScene):
        image = QImage(":/qt4logo.png")
        xx = 0
        nitems = 0
        i = -11000
        while i < 11000:
            ++xx
            yy: int = 0
            j: int = -7000
            while j < 7000:
                ++yy
                x = (i + 11000) / 22000.0
                y = (j + 7000) / 14000.0

                color = QColor(image.pixel(int(image.width() * x), int(image.height() * y)))
                # color = QColor(0, 255, 0)
                item = Chip(color, xx, yy)
                item.setPos(QPointF(i, j))
                scene.addItem(item)
                ++nitems
                j += 70
            i += 110


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1280, 720)
    window.show()
    sys.exit(app.exec_())
