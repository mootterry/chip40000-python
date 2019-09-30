from PySide2.QtCore import Qt, QSize, QRectF, Slot
from PySide2.QtGui import QWheelEvent, QIcon, QMatrix, QPainter
from PySide2.QtWidgets import (QGraphicsView, QFrame, QWidget, QStyle,
                               QToolButton, QSlider, QVBoxLayout, QButtonGroup,
                               QGridLayout, QHBoxLayout, QLabel, QDialog)
from PySide2.QtOpenGL import QGLFormat, QGLWidget, QGL
from PySide2.QtPrintSupport import QPrintDialog, QPrinter


class GraphicsView(QGraphicsView):
    def __init__(self, view, parent=None):
        QGraphicsView.__init__(self, parent)
        self.view = view

    def wheelEvent(self, e: QWheelEvent):
        if e.modifiers() & Qt.ControlModifier:
            if e.delta() > 0:
                self.view.zoomIn(6)
            else:
                self.view.zoomOut(6)
        else:
            QGraphicsView.wheelEvent(e)


class View(QFrame):
    def __init__(self, name: str, parent: QWidget = None):
        QFrame.__init__(self, parent)

        self.setFrameShape(QFrame.Shape(QFrame.Sunken | QFrame.StyledPanel))
        self.graphicsView = GraphicsView(self)
        self.graphicsView.setRenderHint(QPainter.Antialiasing, False)
        self.graphicsView.setDragMode(QGraphicsView.RubberBandDrag)
        self.graphicsView.setOptimizationFlag(QGraphicsView.DontSavePainterState)
        self.graphicsView.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        self.graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        size = self.style().pixelMetric(QStyle.PM_ToolBarIconSize)
        iconSize = QSize(size, size)

        self.zoomInIcon = QToolButton()
        self.zoomInIcon.setAutoRepeat(True)
        self.zoomInIcon.setAutoRepeatInterval(33)
        self.zoomInIcon.setAutoRepeatDelay(0)
        self.zoomInIcon.setIcon(QIcon(":/zoomin.png"))
        self.zoomInIcon.setIconSize(iconSize)
        self.zoomOutIcon = QToolButton()
        self.zoomOutIcon.setAutoRepeat(True)
        self.zoomOutIcon.setAutoRepeatInterval(33)
        self.zoomOutIcon.setAutoRepeatDelay(0)
        self.zoomOutIcon.setIcon(QIcon(":/zoomout.png"))
        self.zoomOutIcon.setIconSize(iconSize)
        self.zoomSlider = QSlider()
        self.zoomSlider.setMinimum(0)
        self.zoomSlider.setMaximum(500)
        self.zoomSlider.setValue(250)
        self.zoomSlider.setTickPosition(QSlider.TicksRight)

        # Zoom slider layout
        zoomSliderLayout = QVBoxLayout()
        zoomSliderLayout.addWidget(self.zoomInIcon)
        zoomSliderLayout.addWidget(self.zoomSlider)
        zoomSliderLayout.addWidget(self.zoomOutIcon)

        self.rotateLeftIcon = QToolButton()
        self.rotateLeftIcon.setIcon(QIcon(":/rotateleft.png"))
        self.rotateLeftIcon.setIconSize(iconSize)
        self.rotateRightIcon = QToolButton()
        self.rotateRightIcon.setIcon(QIcon(":/rotateright.png"))
        self.rotateRightIcon.setIconSize(iconSize)
        self.rotateSlider = QSlider()
        self.rotateSlider.setOrientation(Qt.Horizontal)
        self.rotateSlider.setMinimum(-360)
        self.rotateSlider.setMaximum(360)
        self.rotateSlider.setValue(0)
        self.rotateSlider.setTickPosition(QSlider.TicksBelow)

        # Rotate slider layout
        rotateSliderLayout = QHBoxLayout()
        rotateSliderLayout.addWidget(self.rotateLeftIcon)
        rotateSliderLayout.addWidget(self.rotateSlider)
        rotateSliderLayout.addWidget(self.rotateRightIcon)

        self.resetButton = QToolButton()
        self.resetButton.setText(self.tr("0"))
        self.resetButton.setEnabled(False)

        # Label layout
        labelLayout = QHBoxLayout()
        self.label = QLabel(name)
        self.label2 = QLabel(self.tr("Pointer Mode"))
        self.selectModeButton = QToolButton()
        self.selectModeButton.setText(self.tr("Select"))
        self.selectModeButton.setCheckable(True)
        self.selectModeButton.setChecked(True)
        self.dragModeButton = QToolButton()
        self.dragModeButton.setText(self.tr("Drag"))
        self.dragModeButton.setCheckable(True)
        self.dragModeButton.setChecked(False)
        self.antialiasButton = QToolButton()
        self.antialiasButton.setText(self.tr("Antialiasing"))
        self.antialiasButton.setCheckable(True)
        self.antialiasButton.setChecked(False)
        self.openGlButton = QToolButton()
        self.openGlButton.setText(self.tr("OpenGL"))
        self.openGlButton.setCheckable(True)
        self.openGlButton.setEnabled(QGLFormat.hasOpenGL())
        self.printButton = QToolButton()
        self.printButton.setIcon(QIcon(":/fileprint.png"))

        pointerModeGroup = QButtonGroup(self)
        pointerModeGroup.setExclusive(True)
        pointerModeGroup.addButton(self.selectModeButton)
        pointerModeGroup.addButton(self.dragModeButton)

        labelLayout.addWidget(self.label)
        labelLayout.addStretch()
        labelLayout.addWidget(self.label2)
        labelLayout.addWidget(self.selectModeButton)
        labelLayout.addWidget(self.dragModeButton)
        labelLayout.addStretch()
        labelLayout.addWidget(self.antialiasButton)
        labelLayout.addWidget(self.openGlButton)
        labelLayout.addWidget(self.printButton)

        topLayout = QGridLayout()
        topLayout.addLayout(labelLayout, 0, 0)
        topLayout.addWidget(self.graphicsView, 1, 0)
        topLayout.addLayout(zoomSliderLayout, 1, 1)
        topLayout.addLayout(rotateSliderLayout, 2, 0)
        topLayout.addWidget(self.resetButton, 2, 1)
        self.setLayout(topLayout)

        self.resetButton.clicked.connect(self.resetView)
        self.zoomSlider.valueChanged.connect(self.setupMatrix)
        self.rotateSlider.valueChanged.connect(self.setupMatrix)
        self.graphicsView.verticalScrollBar().valueChanged.connect(self.setResetButtonEnabled)
        self.graphicsView.horizontalScrollBar().valueChanged.connect(self.setResetButtonEnabled)
        self.selectModeButton.toggled.connect(self.togglePointerMode)
        self.dragModeButton.toggled.connect(self.togglePointerMode)
        self.antialiasButton.toggled.connect(self.toggleAntialiasing)
        self.openGlButton.toggled.connect(self.toggleOpenGL)
        self.rotateLeftIcon.clicked.connect(self.rotateLeft)
        self.rotateRightIcon.clicked.connect(self.rotateRight)
        self.zoomInIcon.clicked.connect(self.zoomIn)
        self.zoomOutIcon.clicked.connect(self.zoomOut)
        self.printButton.clicked.connect(self.print)

        self.setupMatrix()

    def view(self):
        return self.graphicsView

    @Slot()
    def resetView(self):
        self.zoomSlider.setValue(250)
        self.rotateSlider.setValue(0)
        self.setupMatrix()
        self.graphicsView.ensureVisible(QRectF())

        self.resetButton.setEnabled(False)

    @Slot()
    def setResetButtonEnabled(self):
        self.resetButton.setEnabled(True)

    @Slot()
    def setupMatrix(self):
        scale = 2**((self.zoomSlider.value() - 250) / 50.0)

        matrix = QMatrix()
        matrix.scale(scale, scale)
        matrix.rotate(self.rotateSlider.value())

        self.graphicsView.setMatrix(matrix)
        self.setResetButtonEnabled()

    @Slot()
    def togglePointerMode(self):
        isChecked = self.selectModeButton.isChecked()
        self.graphicsView.setDragMode(QGraphicsView.RubberBandDrag if isChecked else GraphicsView.ScrollHandDrag)
        self.graphicsView.setInteractive(isChecked)

    @Slot()
    def toggleOpenGL(self):
        self.graphicsView.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)) if self.openGlButton.isChecked() else QWidget())

    @Slot()
    def toggleAntialiasing(self):
        self.graphicsView.setRenderHint(QPainter.Antialiasing, self.antialiasButton.isChecked())

    @Slot()
    def print(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer)
        if dialog.exec() == QDialog.Accepted:
            painter = QPainter(printer)
            self.graphicsView.render(painter)

    @Slot()
    def zoomIn(self):
        self.zoomSlider.setValue(self.zoomSlider.value() + 1)

    @Slot()
    def zoomOut(self, level=1):
        self.zoomSlider.setValue(self.zoomSlider.value() - 1)

    @Slot()
    def rotateLeft(self):
        self.rotateSlider.setValue(self.rotateSlider.value() - 10)

    @Slot()
    def rotateRight(self):
        self.rotateSlider.setValue(self.rotateSlider.value() + 10)
