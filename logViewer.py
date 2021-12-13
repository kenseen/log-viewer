import sys
import re
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog


class MyWindow(QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100, 100, 1000, 500)
        self.setMinimumSize(250, 250)
        self.setWindowTitle("Log Parser")
        self.resized.connect(self.updateSize)
        self.darkMode = False

        extractAction = QtWidgets.QAction("&Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)

        extractAction2 = QtWidgets.QAction("&Import", self)
        extractAction2.setShortcut("Ctrl+I")
        extractAction2.setStatusTip('Import log file')
        extractAction2.triggered.connect(self.importFile)

        windowAction = QtWidgets.QAction("&Light mode", self)
        windowAction.setStatusTip('Switch layout mode to light')
        windowAction.triggered.connect(lambda: self.windowDarkMode(False))

        windowAction2 = QtWidgets.QAction("&Dark mode", self)
        windowAction2.setStatusTip('Switch layout mode to dark')
        windowAction2.triggered.connect(lambda: self.windowDarkMode(True))

        self.textLog = "Your log will appear here:"

        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setText(self.textLog)

        statBar = self.statusBar()
        statBar.setSizeGripEnabled(False)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        windowMenu = mainMenu.addMenu('&Window')

        fileMenu.addAction(extractAction2)
        fileMenu.addAction(extractAction)
        windowMenu.addAction(windowAction)
        windowMenu.addAction(windowAction2)

        self.home()

    def home(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Info label")

        self.label2 = QtWidgets.QLabel(self)
        self.label2.setText("Your Custom Filter:")
        self.label2.setGeometry(0, 50, 140, 30)

        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(140, 50, 820, 30)
        self.lineEdit.setStyleSheet("background-color: white; border: 1px solid black")

        self.runCustomFilterButton = QtWidgets.QPushButton("Run", self)
        self.runCustomFilterButton.clicked.connect(lambda: self.showLog("custom"))

        self.leftButton1 = QtWidgets.QPushButton("All log", self)
        self.leftButton1.setGeometry(0, 100, 170, 30)
        self.leftButton1.clicked.connect(lambda: self.showLog("all"))

        self.leftButton2 = QtWidgets.QPushButton("Order", self)
        self.leftButton2.setGeometry(0, 130, 170, 30)
        self.leftButton2.clicked.connect(lambda: self.showLog("order"))

        self.leftButton3 = QtWidgets.QPushButton("Message", self)
        self.leftButton3.setGeometry(0, 160, 170, 30)
        self.leftButton3.clicked.connect(lambda: self.showLog("message"))

        self.leftButton4 = QtWidgets.QPushButton("something", self)
        self.leftButton4.setGeometry(0, 190, 170, 30)
        self.leftButton4.clicked.connect(lambda: self.showLog(""))

        self.leftButton5 = QtWidgets.QPushButton("State", self)
        self.leftButton5.setGeometry(0, 220, 170, 30)
        self.leftButton5.clicked.connect(lambda: self.showLog("state"))

        self.leftButton6 = QtWidgets.QPushButton("Status", self)
        self.leftButton6.setGeometry(0, 250, 170, 30)
        self.leftButton6.clicked.connect(lambda: self.showLog("status"))

        self.windowDarkMode(False)
        self.show()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MyWindow, self).resizeEvent(event)

    def updateSize(self):
        self.textBrowser.setGeometry(170, 100, self.width() - 170, self.height() - 122)
        self.label.setGeometry(0, 20, self.width(), 30)
        self.lineEdit.setGeometry(140, 50, self.width() - 180, 30)
        self.runCustomFilterButton.setGeometry(self.width() - 40, 50, 40, 30)

    def close_application(self):
        choice = QMessageBox.question(self, 'Exiting!',
                                      "Are you sure to quit?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def importFile(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)
        if name != "":
            file = open(name, 'r')
            self.label.setText('File opened: {}'.format(name))
            self.label.setStyleSheet("background-color: rgb(237, 137, 61); border: 1px solid black")

            with file:
                self.wholeLog = file.read()
                self.textBrowser.setText(self.wholeLog)

        else:
            self.label.setText("Warning: No new file imported")
            self.label.setStyleSheet("background-color: yellow; border: 1px solid black")

    def windowDarkMode(self, darkMode):
        if not darkMode:
            self.darkMode = False
            self.textBrowser.setStyleSheet("background-color: white; border: 1px solid black; font: normal")
            self.setStyleSheet("font: bold")
            self.resetButtonColor()
            self.lineEdit.setStyleSheet("border: 1px solid black")
            self.label.setStyleSheet("background-color: rgb(237, 137, 61); border: 1px solid black")
            self.label2.setStyleSheet("background-color: rgb(240, 158, 98); border: 1px solid black; font: normal")

        if darkMode:
            self.darkMode = True
            self.setStyleSheet("background-color: rgb(43, 43, 43); color: rgb(159, 174, 191); font: bold")
            self.textBrowser.setStyleSheet("background-color: rgb(43, 43, 43); border: 1px solid rgb(85, 85, 85);"
                                           "color: rgb(159, 174, 191); font: normal")
            self.resetButtonColor()
            self.lineEdit.setStyleSheet("background-color: rgb(124, 130, 133); border: 1px solid black; color: black")
            self.label.setStyleSheet("background-color: rgb(79, 75, 65); border: 1px solid rgb(85, 85, 85)")
            self.label2.setStyleSheet(
                "background-color: rgb(60, 63, 65); border: 1px solid rgb(85, 85, 85); font: normal")


    def filterLog(self, filter):
        result = ""

        if filter == "all":
            result = self.wholeLog

        if filter == "order":
            result = "\n".join(re.findall(".*order.*", self.wholeLog))

        if filter == "message":
            result = "\n".join(re.findall(".*message*", self.wholeLog))

        if filter == "state":
            result = "\n".join(re.findall(".*state.*", self.wholeLog))

        if filter == "custom":
            print(self.lineEdit.text())
            result = "\n".join(re.findall(".*{}.*".format(self.lineEdit.text()), self.wholeLog))

        if filter == "status":
            print(self.lineEdit.text())
            result = "\n".join(re.findall(".*status.*", self.wholeLog))

        return result

    def showLog(self, filter):
        self.resetButtonColor()

        if hasattr(self, 'wholeLog'):

            if filter == "custom":
                self.runCustomFilterButton.setStyleSheet("background-color: green;")
                self.textBrowser.setText(self.filterLog(filter))

            if filter == "all":
                self.leftButton1.setStyleSheet("background-color: green;")
                self.textBrowser.setText(self.filterLog(filter))

            if filter == "order":
                self.leftButton2.setStyleSheet("background-color: green;")
                self.textBrowser.setText(self.filterLog(filter))

            if filter == "message":
                self.leftButton3.setStyleSheet("background-color: green;")
                self.textBrowser.setText(self.filterLog(filter))

            if filter == "":
                self.leftButton4.setStyleSheet("background-color: green;")
                self.textBrowser.setText(self.filterLog(filter))

            if filter == "state":
                self.leftButton5.setStyleSheet("background-color: green;")
                self.textBrowser.setText(self.filterLog(filter))

            if filter == "status":
                self.leftButton6.setStyleSheet("background-color: green;")
                self.textBrowser.setText(self.filterLog(filter))

        else:
            self.label.setText("Warning: No file imported")
            self.label.setStyleSheet("background-color: yellow; border: 1px solid black")
            print(self.height())
            print(self.width())
            self.textBrowser.setGeometry(170, 100, self.width() - 170, self.height() - 120)

    def resetButtonColor(self):
        self.buttonBackgroundColor = "rgb(60, 63, 65)" if self.darkMode == True else "white"

        self.runCustomFilterButton.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
        self.leftButton1.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
        self.leftButton2.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
        self.leftButton3.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
        self.leftButton4.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
        self.leftButton5.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
        self.leftButton5.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
        self.leftButton6.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))


def run():
    app = QApplication(sys.argv)
    GUI = MyWindow()
    sys.exit(app.exec_())


run()