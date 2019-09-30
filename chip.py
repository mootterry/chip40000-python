import PySide2.QtGui
import PySide2.QtWidgets
from typing import List
from PySide2.QtCore import QLineF, QRectF, QRect, Qt
from PySide2.QtGui import QColor, QBrush, QPen, QPainterPath, QPainter, QFont
from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget, QStyle


class Chip(QGraphicsItem):
    def __init__(self, color: QColor, x: int, y: int, parent=None):
        QGraphicsItem.__init__(self, parent)
        self.x = x
        self.y = y
        self.color = color
        self.stuff = []
        self.setZValue((x + y) % 2)

        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setAcceptHoverEvents(True)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, 110, 70)

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addRect(14, 14, 82, 82)
        return path

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = ...):
        fillColor = self.color.darker(150) if option.state & QStyle.State_Selected else self.color
        if option.state & QStyle.State_MouseOver:
            fillColor = fillColor.lighter(125)

        lod = option.levelOfDetailFromTransform(painter.worldTransform())

        if lod < 0.2:
            if lod < 0.125:
                painter.fillRect(QRectF(0, 0, 110, 70), fillColor)
                return

            b = painter.brush()
            painter.setBrush(fillColor)
            painter.drawRect(13, 13, 97, 57)
            painter.setBrush(b)
            return

        oldPen = painter.pen()
        pen = oldPen
        width = 0
        if option.state & QStyle.State_Selected:
            width += 2
        pen.setWidth(width)
        b = painter.brush()
        painter.setBrush(QBrush(fillColor.darker(120 if option.state & QStyle.State_Sunken else 100)))

        painter.drawRect(QRect(14, 14, 79, 39))
        painter.setBrush(b)

        if lod >= 1:
            painter.setPen(QPen(Qt.gray, 1))
            painter.drawLine(15, 54, 94, 54)
            painter.drawLine(94, 53, 94, 15)
            painter.setPen(QPen(Qt.black, 0))

        # Draw text
        if lod >= 2:
            font = QFont("Times", 10)
            font.setStyleStrategy(QFont.ForceOutline)
            painter.setFont(font)
            painter.save()
            painter.scale(0.1, 0.1)
            painter.drawText(170, 180, f"Model: VSC-2000 (Very Small Chip) at {self.x}x{self.y}")
            painter.drawText(170, 200, "Serial number: DLWR-WEER-123L-ZZ33-SDSJ")
            painter.drawText(170, 220, "Manufacturer: Chip Manufacturer")
            painter.restore()

        # Drawlines
        lines: List[QLineF] = []
        if lod >= 0.5:
            s = 1 if lod > 0.5 else 2
            for i in range(0, 11, s):
                lines.append(QLineF(18 + 7 * i, 13, 18 + 7 * i, 5))
                lines.append(QLineF(18 + 7 * i, 54, 18 + 7 * i, 62))

            for i in range(0, 7, s):
                lines.append(QLineF(5, 18 + i * 5, 13, 18 + i * 5))
                lines.append(QLineF(94, 18 + i * 5, 102, 18 + i * 5))

        if lod >= 0.4:
            lines.extend([
                QLineF(25, 35, 35, 35),
                QLineF(35, 30, 35, 40),
                QLineF(35, 30, 45, 35),
                QLineF(35, 40, 45, 35),
                QLineF(45, 30, 45, 40),
                QLineF(45, 35, 55, 35)
            ])
        painter.drawLines(lines[:])

        ## Draw red ink
        if len(self.stuff) > 1:
            p = painter.pen()
            painter.setPen(QPen(Qt.red, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setBrush(Qt.NoBrush)
            path = QPainterPath()
            path.moveTo(self.stuff[0])
            for i in range(1, len(self.stuff)):
                path.lineTo(self.stuff[i])
            painter.drawPath(path)
            painter.setPen(p)

    def mousePressEvent(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent):
        super().mousePressEvent(event)
        self.update()

    def mouseMoveEvent(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent):
        if event.modifiers() & Qt.ShiftModifier:
            self.stuff.append(event.pos())
            self.update()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent):
        super().mouseReleaseEvent(event)
        self.update()
