from PySide2.QtCore import Qt, QSize, QRectF
from PySide2.QtGui import QWheelEvent, QIcon, QMatrix, QPainter
from PySide2.QtOpenGL import QGLFormat, QGLWidget, QGL
from PySide2.QtWidgets import QGraphicsView, QFrame, QWidget, QStyle, QToolButton, QSlider, QVBoxLayout, \
    QButtonGroup, QGridLayout, QHBoxLayout, QLabel


class GraphicsView(QGraphicsView):
    def __init__(self, view):
        super().__init__()
        self.view = view

    def wheelEvent(self, e: QWheelEvent):
        if e.modifiers() & Qt.ControlModifier:
            if e.delta() > 0:
                self.view.zoomIn(6)
            else:
                self.view.zoomOut(6)
        else:
            super().wheelEvent(e)


class View(QFrame):
    def __init__(self, name: str, parent: QWidget):
        super().__init__(parent)
        self.name = name
        self.setFrameShape(QFrame.Shape(QFrame.Sunken | QFrame.StyledPanel))
        graphicsView = GraphicsView(self)
        graphicsView.setRenderHint(QPainter.Antialiasing, False)
        graphicsView.setDragMode(QGraphicsView.RubberBandDrag)
        graphicsView.setOptimizationFlag(QGraphicsView.DontSavePainterState)
        graphicsView.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)
        graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        size = self.style().pixelMetric(QStyle.PM_ToolBarIconSize)
        iconSize = QSize(size, size)
        zoomInIcon = QToolButton()
        zoomInIcon.setAutoRepeat(True)
        zoomInIcon.setAutoRepeatInterval(33)
        zoomInIcon.setAutoRepeatDelay(0)
        zoomInIcon.setIcon(QIcon(":/zoomin.png"))
        zoomInIcon.setIconSize(iconSize)

        zoomOutIcon = QToolButton()
        zoomOutIcon.setAutoRepeat(True)
        zoomOutIcon.setAutoRepeatInterval(33)
        zoomOutIcon.setAutoRepeatDelay(0)
        zoomOutIcon.setIcon(QIcon(":/zoomout.png"))
        zoomOutIcon.setIconSize(iconSize)

        zoomSlider = QSlider()
        zoomSlider.setMinimum(0)
        zoomSlider.setMaximum(500)
        zoomSlider.setValue(250)
        self.zoomSlider = zoomSlider
        zoomSlider.setTickPosition(QSlider.TicksRight)

        zoomSliderLayout = QVBoxLayout()
        zoomSliderLayout.addWidget(zoomInIcon)
        zoomSliderLayout.addWidget(zoomSlider)
        zoomSliderLayout.addWidget(zoomOutIcon)
        rotateLeftIcon = QToolButton()
        rotateLeftIcon.setIcon(QIcon(":/rotateleft.png"))
        rotateLeftIcon.setIconSize(iconSize)
        rotateRightIcon = QToolButton()
        rotateRightIcon.setIcon(QIcon(":/rotateright.png"))
        rotateRightIcon.setIconSize(iconSize)
        rotateSlider = QSlider()
        rotateSlider.setOrientation(Qt.Horizontal)
        rotateSlider.setMinimum(-360)
        rotateSlider.setMaximum(360)
        rotateSlider.setValue(0)
        rotateSlider.setTickPosition(QSlider.TicksBelow)
        self.rotateSlider = rotateSlider

        # Rotate slider layout
        rotateSliderLayout = QHBoxLayout()
        rotateSliderLayout.addWidget(rotateLeftIcon)
        rotateSliderLayout.addWidget(rotateSlider)
        rotateSliderLayout.addWidget(rotateRightIcon)

        resetButton = QToolButton()
        resetButton.setText(self.tr("0"))
        resetButton.setEnabled(False)
        self.resetButton = resetButton

        # Label layout
        labelLayout = QHBoxLayout()
        label = QLabel(name)
        label2 = QLabel(self.tr("Pointer Mode"))
        selectModeButton = QToolButton()
        selectModeButton.setText(self.tr("Select"))
        selectModeButton.setCheckable(True)
        selectModeButton.setChecked(True)
        self.selectModeButton = selectModeButton
        dragModeButton = QToolButton()
        dragModeButton.setText(self.tr("Drag"))
        dragModeButton.setCheckable(True)
        dragModeButton.setChecked(False)
        antialiasButton = QToolButton()
        antialiasButton.setText(self.tr("Antialiasing"))
        antialiasButton.setCheckable(True)
        antialiasButton.setChecked(False)
        self.antialiasButton = antialiasButton
        openGlButton = QToolButton()
        openGlButton.setText(self.tr("OpenGL"))
        openGlButton.setCheckable(True)
        openGlButton.setEnabled(QGLFormat.hasOpenGL())
        self.openGlButton = openGlButton
        printButton = QToolButton()
        printButton.setIcon(QIcon(":/fileprint.png"))

        pointerModeGroup = QButtonGroup(self)
        pointerModeGroup.setExclusive(True)
        pointerModeGroup.addButton(selectModeButton)
        pointerModeGroup.addButton(dragModeButton)

        labelLayout.addWidget(label)
        labelLayout.addStretch()
        labelLayout.addWidget(label2)
        labelLayout.addWidget(selectModeButton)
        labelLayout.addWidget(dragModeButton)
        labelLayout.addStretch()
        labelLayout.addWidget(antialiasButton)
        labelLayout.addWidget(openGlButton)
        labelLayout.addWidget(printButton)

        topLayout = QGridLayout()
        topLayout.addLayout(labelLayout, 0, 0)
        topLayout.addWidget(graphicsView, 1, 0)
        topLayout.addLayout(zoomSliderLayout, 1, 1)
        topLayout.addLayout(rotateSliderLayout, 2, 0)
        topLayout.addWidget(resetButton, 2, 1)
        self.setLayout(topLayout)

        resetButton.clicked.connect(self.resetView)
        zoomSlider.valueChanged.connect(self.setupMatrix)
        rotateSlider.valueChanged.connect(self.setupMatrix)

        graphicsView.verticalScrollBar().valueChanged.connect(self.setResetButtonEnabled)
        graphicsView.horizontalScrollBar().valueChanged.connect(self.setResetButtonEnabled)
        selectModeButton.toggled.connect(self.togglePointerMode)
        dragModeButton.toggled.connect(self.togglePointerMode)
        antialiasButton.toggled.connect(self.toggleAntialiasing)
        openGlButton.toggled.connect(self.toggleOpenGL)
        rotateLeftIcon.clicked.connect(self.rotateLeft)
        rotateRightIcon.clicked.connect(self.rotateRight)
        zoomInIcon.clicked.connect(self.zoomIn)
        zoomOutIcon.clicked.connect(self.zoomOut)
        printButton.clicked.connect(self.print)

        self.graphicsView = graphicsView

    def view(self):
        return self.graphicsView

    def resetView(self):
        self.zoomSlider.setValue(250)
        self.rotateSlider.setValue(0)
        self.setupMatrix()
        self.graphicsView.ensureVisible(QRectF())
        self.resetButton.setEnabled(False)

    def setResetButtonEnabled(self):
        self.resetButton.setEnabled(True)

    def setupMatrix(self):
        scale = pow(2.0, (self.zoomSlider.value() - 250) / 50.0)
        print(F"zoomSlider.value = {self.zoomSlider.value()} scale={scale}")
        matrix = QMatrix()
        matrix.scale(scale, scale)
        matrix.rotate(self.rotateSlider.value())

        self.graphicsView.setMatrix(matrix)
        self.setResetButtonEnabled()

    def togglePointerMode(self):
        isChecked = self.selectModeButton.isChecked()
        self.graphicsView.setDragMode(QGraphicsView.RubberBandDrag if isChecked else GraphicsView.ScrollHandDrag)
        self.graphicsView.setInteractive(isChecked)

    def toggleOpenGL(self):
        self.graphicsView.setViewport(
            QGLWidget(QGLFormat(QGL.SampleBuffers)) if self.openGlButton.isChecked() else QWidget)

    def toggleAntialiasing(self):
        self.graphicsView.setRenderHint(QPainter.Antialiasing, self.antialiasButton.isChecked())

    def print(self):
        pass

    def zoomIn(self):
        self.zoom(1)

    def zoomOut(self):
        self.zoom(-1)

    def zoom(self, level: int):
        self.zoomSlider.setValue(self.zoomSlider.value() + level)

    def rotateLeft(self):
        self.rotateSlider.setValue(self.rotateSlider.value() - 10)

    def rotateRight(self):
        self.rotateSlider.setValue(self.rotateSlider.value() + 10)
