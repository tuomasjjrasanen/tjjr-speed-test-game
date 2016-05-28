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
