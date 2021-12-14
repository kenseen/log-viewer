import sys
import re
import json

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog


class MyWindow(QMainWindow):

    resized = QtCore.pyqtSignal()

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100, 100, 1000, 500)
        self.setMinimumSize(250, 250)
        self.setWindowTitle("Log Viewer")
        self.resized.connect(self.updateSize)
        self.darkMode = False
        self.ignoreLetterCase = True
        self.leftButtonNames = []
        self.sideButtons = []
        self.topButtons = []

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

        settingsAction = QtWidgets.QAction("&Change filters", self)
        settingsAction.setStatusTip('Import configiration file')
        settingsAction.triggered.connect(lambda: self.readConfFile("custom"))

        settingsAction2 = QtWidgets.QAction("&Use default filters", self)
        settingsAction2.setStatusTip('Switch case sensitive OFF')
        settingsAction2.triggered.connect(lambda: self.readConfFile("default"))

        self.textLog = "Your log will appear here:"

        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setText(self.textLog)

        statBar = self.statusBar()
        statBar.setSizeGripEnabled(False)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        windowMenu = mainMenu.addMenu('&Window')
        settingsMenu = mainMenu.addMenu('&Settings')

        fileMenu.addActions([extractAction2, extractAction])
        windowMenu.addActions([windowAction, windowAction2])
        settingsMenu.addActions([settingsAction, settingsAction2])

        self.readConfFile("default")

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
        self.runCustomFilterButton.clicked.connect(lambda: self.customFilter())

        self.showAllLogButton = QtWidgets.QPushButton("Show whole log", self)
        self.showAllLogButton.setGeometry(0, 80, 170, 30)
        self.showAllLogButton.clicked.connect(lambda: self.showAllLog())

        self.caseSensitiveCheckBox = QtWidgets.QCheckBox(self)
        self.caseSensitiveCheckBox.setStyleSheet("background-color: white; border: 1px solid black; padding: 4px;")
        self.caseSensitiveCheckBox.setStatusTip('When selected case sensitivity for custom filter is ON')
        self.caseSensitiveCheckBox.stateChanged.connect(lambda: self.caseSensitivity())

        self.windowDarkMode(False)
        self.createTopButtons()
        #self.createSideButtons(0)

        self.show()

    def readConfFile(self, type):
        #clear old GUI
        self.removeButtons("leftSide")
        self.removeButtons("topSide")

        if type == "default":
            f = open('initConf.json',)
            self.initConf = json.load(f)
            self.createTopButtons()

        elif type == "custom":
            self.importJsonFile()
            self.createTopButtons()

    def createTopButtons(self):
        self.removeButtons("topSide")
        self.topButtons = []

        for i in range(len(self.initConf["applications"])):
            self.topButtons.append(QtWidgets.QPushButton(self.initConf["applications"][i]["topButtonName"], self))
            self.topButtons[i].show()
        self.modifyTopButtons()

    def removeButtons(self, menuSide):
        if menuSide == "leftSide" and hasattr(self, 'sideButtons'):
            for button in self.sideButtons:
                button.deleteLater()
            del self.sideButtons
        elif menuSide == "topSide" and hasattr(self, 'topButtons'):
            for button in self.topButtons:
                button.deleteLater()
            del self.topButtons
        else:
            pass

    def createSideButtons(self, topNumber):
        self.removeButtons("leftSide")
        self.resetButtonColor("topMenu")
        self.topButtons[topNumber].setStyleSheet("background-color: green;")
        self.sideButtons = []
        self.filters = []

        for i in range(len(self.initConf["applications"][topNumber]["sideButtonName"])):
            # update list of buttons and create new buttons
            self.sideButtons.append(QtWidgets.QPushButton(self.initConf["applications"][topNumber]["sideButtonName"][i], self))
            self.sideButtons[i].show()
            # update list of filters
            self.filters.append(self.initConf["applications"][topNumber]["filter"][i])

        self.modifySideButtons()

    def modifyTopButtons(self):
        for i in range(len(self.topButtons)):
            self.topButtons[i].setGeometry(i*115+170, 80, 115, 30)
            self.topButtons[i].clicked.connect(lambda state, x=i: self.createSideButtons(x))


    def modifySideButtons(self):
        for i in range(len(self.sideButtons)):
            self.sideButtons[i].setGeometry(0, i*30+110, 170, 30)
            self.sideButtons[i].clicked.connect(lambda state, x=i: self.showLog(x))

        #more readable form above
        #for button in self.sideButtons:
        #    button.setGeometry(0, self.sideButtons.index(button) * 30 + 110, 170, 30)
        #    button.clicked.connect(lambda state, x=self.sideButtons.index(button): self.showLog(x))

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MyWindow, self).resizeEvent(event)

    def updateSize(self):
        self.textBrowser.setGeometry(170, 110, self.width() - 170, self.height() - 130)
        self.label.setGeometry(0, 20, self.width(), 30)
        self.lineEdit.setGeometry(140, 50, self.width() - 215, 30)
        self.runCustomFilterButton.setGeometry(self.width() - 75, 50, 50, 30)
        self.caseSensitiveCheckBox.setGeometry(self.width() - 25, 50, 25, 30)

    def close_application(self):
        choice = QMessageBox.question(self, 'Exiting!',
                                      "Are you sure to quit?",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def modifyFile(self):
        if self.wholeLog:
            modifiedLog = self.wholeLog.split("\n")
            for i in range(len(modifiedLog)):
                modifiedLog[i] = str(i+1) + ".) " + modifiedLog[i] + "\n"
            self.wholeLog = "\n".join(modifiedLog)
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
                self.modifyFile()
                self.showAllLog()
        else:
            self.label.setText("Warning: No new file imported")
            self.label.setStyleSheet("background-color: yellow; border: 1px solid black")

    def importJsonFile(self):
        name, _ = QFileDialog.getOpenFileName(self, 'Open Json', options=QFileDialog.DontUseNativeDialog)

        if name != "":
            file = open(name, 'r')

            with file:
                self.initConf = json.load(file)
        else:
            self.label.setText("Warning: No new configuration file imported")
            self.label.setStyleSheet("background-color: yellow; border: 1px solid black")

    def windowDarkMode(self, darkMode):
        if not darkMode:
            self.darkMode = False
            self.textBrowser.setStyleSheet("background-color: white; border: 1px solid black; font: normal")
            self.setStyleSheet("font: bold")
            self.resetButtonColor("sideMenu")
            self.resetButtonColor("topMenu")
            self.lineEdit.setStyleSheet("border: 1px solid black")
            self.label.setStyleSheet("background-color: rgb(237, 137, 61); border: 1px solid black")
            self.label2.setStyleSheet("background-color: rgb(240, 158, 98); border: 1px solid black; font: normal")

        if darkMode:
            self.darkMode = True
            self.setStyleSheet("background-color: rgb(43, 43, 43); color: rgb(159, 174, 191); font: bold")
            self.textBrowser.setStyleSheet("background-color: rgb(43, 43, 43); border: 1px solid rgb(85, 85, 85);"
                                           "color: rgb(159, 174, 191); font: normal")
            self.resetButtonColor("sideMenu")
            self.resetButtonColor("topMenu")
            self.lineEdit.setStyleSheet("background-color: rgb(124, 130, 133); border: 1px solid black; color: black")
            self.label.setStyleSheet("background-color: rgb(79, 75, 65); border: 1px solid rgb(85, 85, 85)")
            self.label2.setStyleSheet(
                "background-color: rgb(60, 63, 65); border: 1px solid rgb(85, 85, 85); font: normal")

    def caseSensitivity(self):
        if self.caseSensitiveCheckBox.isChecked() == True:
            self.ignoreLetterCase = False
        else:
            self.ignoreLetterCase = True

    def customFilter(self):
        self.resetButtonColor("sideMenu")
        self.resetButtonColor("topMenu")
        self.runCustomFilterButton.setStyleSheet("background-color: green;")

        if hasattr(self, 'wholeLog'):
            if self.ignoreLetterCase == True:
                self.textBrowser.setText("\n".join(re.findall(".*{}.*".format(self.lineEdit.text()), self.wholeLog, flags=re.IGNORECASE)))
            if self.ignoreLetterCase == False:
                self.textBrowser.setText("\n".join(re.findall(".*{}.*".format(self.lineEdit.text()), self.wholeLog)))
        else:
            self.label.setText("Warning: No file imported")
            self.label.setStyleSheet("background-color: yellow; border: 1px solid black")

    def showLog(self, number):
        self.resetButtonColor("sideMenu")

        if hasattr(self, 'wholeLog'):
            self.sideButtons[number].setStyleSheet("background-color: green;")
            self.textBrowser.setText("\n\n".join(re.findall(".*{}.*".format(self.filters[number]), self.wholeLog)))
        else:
            self.label.setText("Warning: No file imported")
            self.label.setStyleSheet("background-color: yellow; border: 1px solid black")

    def showAllLog(self):
        self.resetButtonColor("topMenu")
        self.removeButtons("leftSide")

        if hasattr(self, 'wholeLog'):
            self.showAllLogButton.setStyleSheet("background-color: green;")
            self.textBrowser.setText(self.wholeLog)
        else:
            self.label.setText("Warning: No file imported")
            self.label.setStyleSheet("background-color: yellow; border: 1px solid black")

    def resetButtonColor(self, buttonType):
        self.buttonBackgroundColor = "rgb(60, 63, 65)" if self.darkMode == True else "white"

        if buttonType == "sideMenu" and hasattr(self, 'sideButtons'):
            self.runCustomFilterButton.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))

            for button in self.sideButtons:
                button.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))

        if buttonType == "topMenu" and hasattr(self, 'topButtons'):
            self.showAllLogButton.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
            self.runCustomFilterButton.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))

            for button in self.topButtons:
                button.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))


def run():
    app = QApplication(sys.argv)
    GUI = MyWindow()
    sys.exit(app.exec_())


run()