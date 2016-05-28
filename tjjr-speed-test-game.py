#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2016 Tuomas Räsänen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class GraphicsGlowEffect(QGraphicsEffect):

    def __init__(self, color):
        super().__init__()

        self.__color  = color
        self.__extent = 100

    def boundingRectFor(self, rect):
        return QRectF(
            rect.left()   - 1 * self.__extent,
            rect.top()    - 1 * self.__extent,
            rect.width()  + 2 * self.__extent,
            rect.height() + 2 * self.__extent)

    def draw(self, painter):
        sourcePixmap, sourceOffset = self.sourcePixmap(Qt.LogicalCoordinates)

        colorizeEffect = QGraphicsColorizeEffect()
        colorizeEffect.setColor(self.__color)

        colorizedPixmap = self.applyEffectToPixmap(sourcePixmap, colorizeEffect, 0)

        blurEffect = QGraphicsBlurEffect()
        blurEffect.setBlurRadius(15)

        colorizedBlurredPixmap = self.applyEffectToPixmap(colorizedPixmap,
                                                          blurEffect,
                                                          self.__extent)

        for i in range(5):
            position = sourceOffset - QPoint(self.__extent, self.__extent)
            painter.drawPixmap(position, colorizedBlurredPixmap)
            self.drawSource(painter)

    def applyEffectToPixmap(self, sourcePixmap, effect, extent):
        if not sourcePixmap:
            return QPixmap()

        if not effect:
            return sourcePixmap

        scene  = QGraphicsScene()
        item   = QGraphicsPixmapItem()
        pixmap = QPixmap(sourcePixmap.width()  + 2 * extent,
                         sourcePixmap.height() + 2 * extent)

        item.setPixmap(sourcePixmap)
        item.setGraphicsEffect(effect)
        scene.addItem(item);
        pixmap.fill(Qt.transparent)
        scene.render(QPainter(pixmap), QRectF(),
                     QRectF(-extent, -extent, pixmap.width(), pixmap.height()))

        return pixmap

class ColorLedButton(QPushButton):

    def __init__(self, color):
        super().__init__()

        self.__color = color
        colorName = color.name()
        darkerColorName = color.darker().name()
        lighterColorName = color.lighter().name()
        self.setStyleSheet("""
ColorLedButton {
 background    : qlineargradient(x1:0, y1:-0.5, x2:0, y2:1.3,
                                 stop:0 %s, stop: 1 %s);
 border-style  : solid;
 border-width  : 1px;
 border-radius : 50px;
 border-color  : black;
 max-width     : 100px;
 max-height    : 100px;
 min-width     : 100px;
 min-height    : 100px;
}

ColorLedButton:pressed {
 background    : qlineargradient(x1:0, y1:0, x2:0, y2:3,
                                 stop:0 %s, stop: 1 %s);
 border-style  : solid;
 border-width  : 3px;
 border-radius : 50px;
 border-color  : black;
 max-width     : 96px;
 max-height    : 96px;
 min-width     : 96px;
 min-height    : 96px;
}

ColorLedButton[isLit="true"] {
 background    : qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                                 fx:0.5, fy:0.5, stop:0 %s, stop: 1 %s);
}

ColorLedButton[isLit="true"]:pressed {
 background    : qradialgradient(cx:0.5, cy:0.5, radius:0.82,
                                 fx:0.55, fy:0.55, stop:0 %s, stop: 1 %s);
}
""" % (lighterColorName, darkerColorName,
       darkerColorName, lighterColorName,
       lighterColorName, colorName,
       lighterColorName, colorName))
        rect = QRect(-2, -2, 106, 106)
        region = QRegion(rect, QRegion.Ellipse)
        self.setMask(region)
        self.setFocusPolicy(Qt.NoFocus)
        self.released.connect(self.setOff)

    def setOn(self):
        self.setGraphicsEffect(GraphicsGlowEffect(self.__color))
        self.setProperty("isLit", True)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def setOff(self):
        self.setGraphicsEffect(None)
        self.setProperty("isLit", False)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

class ButtonPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        redButton = ColorLedButton(QColor(255, 0, 0))
        greenButton = ColorLedButton(QColor(0, 255, 0))
        blueButton = ColorLedButton(QColor(0, 0, 255))
        yellowButton = ColorLedButton(QColor(255, 255, 0))
        redButton.setOn()
        greenButton.setOn()
        blueButton.setOn()
        yellowButton.setOn()
        layout.addWidget(redButton)
        layout.addWidget(greenButton)
        layout.addWidget(blueButton)
        layout.addWidget(yellowButton)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

def main():
    app = QApplication(sys.argv)

    if app.argc() > 1:
        error_message = "ERROR: invalid number of arguments ({}), expected 0"
        print(error_message.format(app.argc() - 1), file=sys.stderr)
        return 1

    win = MainWindow()
    win.show()

    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
