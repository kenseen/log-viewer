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
        self.setWindowTitle("Log Viewer")
        self.resized.connect(self.updateSize)
        self.darkMode = False
        self.ignoreLetterCase = True
        self.actualPart = ""
        self.leftButtonNames = []

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

        '''settingsAction = QtWidgets.QAction("&Case sensitive", self)
        settingsAction.setStatusTip('Switch case sensitive ON')
        settingsAction.triggered.connect(lambda: self.windowDarkMode(False))

        settingsAction2 = QtWidgets.QAction("&Case insensitive", self)
        settingsAction2.setStatusTip('Switch case sensitive OFF')
        settingsAction2.triggered.connect(lambda: self.windowDarkMode(True))'''

        self.textLog = "Your log will appear here:"

        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setText(self.textLog)

        statBar = self.statusBar()
        statBar.setSizeGripEnabled(False)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        windowMenu = mainMenu.addMenu('&Window')
        #settingsMenu = mainMenu.addMenu('&Settings')

        fileMenu.addActions([extractAction2, extractAction])
        windowMenu.addActions([windowAction, windowAction2])

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

        self.caseSensitiveCheckBox = QtWidgets.QCheckBox(self)
        self.caseSensitiveCheckBox.setStyleSheet("background-color: white; border: 1px solid black; padding: 4px;")
        self.caseSensitiveCheckBox.setStatusTip('When selected case sensitivity for custom filter is ON')
        self.caseSensitiveCheckBox.stateChanged.connect(lambda: self.caseSensitivity())

        self.leftButton1 = QtWidgets.QPushButton(self)
        self.leftButton1.setGeometry(0, 110, 170, 30)
        self.leftButton1.clicked.connect(lambda: self.showLog(self.actualPart, 1))

        self.leftButton2 = QtWidgets.QPushButton(self)
        self.leftButton2.setGeometry(0, 140, 170, 30)
        self.leftButton2.clicked.connect(lambda: self.showLog(self.actualPart, 2))

        self.leftButton3 = QtWidgets.QPushButton(self)
        self.leftButton3.setGeometry(0, 170, 170, 30)
        self.leftButton3.clicked.connect(lambda: self.showLog(self.actualPart, 3))

        self.leftButton4 = QtWidgets.QPushButton(self)
        self.leftButton4.setGeometry(0, 200, 170, 30)
        self.leftButton4.clicked.connect(lambda: self.showLog(self.actualPart, 4))

        self.leftButton5 = QtWidgets.QPushButton(self)
        self.leftButton5.setGeometry(0, 230, 170, 30)
        self.leftButton5.clicked.connect(lambda: self.showLog(self.actualPart, 5))

        self.leftButton6 = QtWidgets.QPushButton(self)
        self.leftButton6.setGeometry(0, 260, 170, 30)
        self.leftButton6.clicked.connect(lambda: self.showLog(self.actualPart, 6))

        self.topButton1 = QtWidgets.QPushButton("Set1", self)
        self.topButton1.setGeometry(0, 80, 75, 30)
        self.topButton1.clicked.connect(lambda: self.setLeftButtonsNames("Set1")) #can use self.topButton1.text() instead of hardcoded "Charger"

        self.topButton2 = QtWidgets.QPushButton("Set2", self)
        self.topButton2.setGeometry(75, 80, 75, 30)
        self.topButton2.clicked.connect(lambda: self.setLeftButtonsNames("Set2"))

        self.topButton3 = QtWidgets.QPushButton("Set3", self)
        self.topButton3.setGeometry(150, 80, 75, 30)
        self.topButton3.clicked.connect(lambda: self.setLeftButtonsNames("Set3"))

        self.topButton4 = QtWidgets.QPushButton("Set4", self)
        self.topButton4.setGeometry(225, 80, 100, 30)
        self.topButton4.clicked.connect(lambda: self.setLeftButtonsNames("Set4"))

        self.topButton5 = QtWidgets.QPushButton("Set5", self)
        self.topButton5.setGeometry(325, 80, 115, 30)
        self.topButton5.clicked.connect(lambda: self.setLeftButtonsNames("Set5"))

        self.topButton6 = QtWidgets.QPushButton("Set6", self)
        self.topButton6.setGeometry(440, 80, 75, 30)
        self.topButton6.clicked.connect(lambda: self.setLeftButtonsNames("Set6"))

        #self.setLeftButtonsNames()
        self.windowDarkMode(False)

        self.settingsAction = QtWidgets.QAction("&Case sensitive", self)
        self.settingsAction.setStatusTip('Switch case sensitive ON')
        self.settingsAction.triggered.connect(lambda: self.windowDarkMode(False))


        self.settingsAction2 = QtWidgets.QAction("&Case insensitive", self)
        self.settingsAction2.setStatusTip('Switch case sensitive OFF')
        self.settingsAction2.triggered.connect(lambda: self.windowDarkMode(True))
        self.topButton6.addAction(self.settingsAction)
        self.topButton6.addAction(self.settingsAction2)
        self.show()

    def setLeftButtonsNames(self, part="Charger"):

        self.resetButtonColor("topMenu")
        self.resetButtonColor("sideMenu")
        self.actualPart = part

        if self.actualPart == "Set1":
           self.topButton1.setStyleSheet("background-color: green;")
           self.leftButtonNames = ["All", "Set1Filter1", "Set1Filter2", "Set1Filter3", "Set1Filter4", "Set1Filter5", "Set1Filter6"]

        elif self.actualPart == "Set2":
            self.topButton2.setStyleSheet("background-color: green;")
            self.leftButtonNames = ["All", "Set2Filter1", "Set2Filter2", "Set2Filter3", "Set2Filter4", "Set2Filter5"]

        elif self.actualPart == "Set3":
            self.topButton3.setStyleSheet("background-color: green;")
            self.leftButtonNames = ["All", "Set3Filter1", "Set3Filter2", "Set3Filter3", "Set3Filter4", "Set3Filter5"] #"ConnectorOutOfOrder",

        elif self.actualPart == "Set4":
            self.topButton4.setStyleSheet("background-color: green;")
            self.leftButtonNames = ["All", "Set4Filter1", "Set4Filter2", "Set4Filter3", "Set4Filter4", "Set4Filter5"]

        elif self.actualPart == "Set5":
            self.topButton5.setStyleSheet("background-color: green;")
            self.leftButtonNames = ["All", "Set5Filter1", "Set5Filter2", "Set5Filter3", "Set5Filter4", "Set5Filter5"]

        elif self.actualPart == "Set6":
            self.topButton6.setStyleSheet("background-color: green;")
            self.leftButtonNames = ["All", "Set6Filter1", "Set6Filter2", "Set6Filter3", "Set6Filter4", "Set6Filter5"]

        else:
            self.leftButtonNames = ["", "", "", "", "", "", "", "", "", ""]

        self.leftButton1.setText(self.leftButtonNames[0])
        self.leftButton2.setText(self.leftButtonNames[1])
        self.leftButton3.setText(self.leftButtonNames[2])
        self.leftButton4.setText(self.leftButtonNames[3])
        self.leftButton5.setText(self.leftButtonNames[4])
        self.leftButton6.setText(self.leftButtonNames[5])

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
                self.setLeftButtonsNames()
                self.showLog()

        else:
            self.label.setText("Warning: No new file imported")
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

    def setPredefinedFilters(self, part):

        if part == "Set1":
            self.predefinedFilters = ["Commit", "messageToHmi", "connectorId.*status", "outletState", "ocppj", "lithosfiltr6"]

        elif part == "Set2":
            self.predefinedFilters = ["terrafiltr1", "terrafiltr2", "terrafiltr3", "terrafiltr4", "terrafiltr5", "terrafiltr6"]

        elif part == "Set3":
            self.predefinedFilters = ["\[CpiComboDc", "\[CpiChademo", "\[V2GProxy", "chargerfiltr4", "chargerfiltr5", "chargerfiltr6"]

        elif part == "Set4":
            self.predefinedFilters = ["installerfiltr1", "installerfiltr2", "installerfiltr3", "installerfiltr4", "installerfiltr5", "installerfiltr6"]

        elif part == "Set5":
            self.predefinedFilters = ["configurefiltr1", "configurefiltr2", "configurefiltr3", "configurefiltr4", "configurefiltr5", "configurefiltr6"]

        elif part == "Set6":
            self.predefinedFilters = ["ccfiltr1", "ccfiltr2", "ccfiltr3", "ccfiltr4", "ccfiltr5", "ccfiltr6"]

    def showLog(self, part="All", buttonNumber=1):

        self.resetButtonColor("sideMenu")
        self.setPredefinedFilters(part)

        if hasattr(self, 'wholeLog'):

            if buttonNumber == 0: #Custom filter
                self.runCustomFilterButton.setStyleSheet("background-color: green;")
                self.textBrowser.setText("\n\n".join(re.findall(".*{}.*".format(self.lineEdit.text()), self.wholeLog)))

            if buttonNumber == 1 or part == "All": #Show whole log
                self.leftButton1.setStyleSheet("background-color: green;")
                self.textBrowser.setText(self.wholeLog)

            if buttonNumber == 2:
                self.leftButton2.setStyleSheet("background-color: green;")
                self.textBrowser.setText("\n\n".join(re.findall(".*{}.*".format(self.predefinedFilters[0]), self.wholeLog)))

            if buttonNumber == 3:
                self.leftButton3.setStyleSheet("background-color: green;")
                self.textBrowser.setText("\n\n".join(re.findall(".*{}.*".format(self.predefinedFilters[1]), self.wholeLog)))

            if buttonNumber == 4:
                self.leftButton4.setStyleSheet("background-color: green;")
                self.textBrowser.setText("\n\n".join(re.findall(".*{}.*".format(self.predefinedFilters[2]), self.wholeLog)))

            if buttonNumber == 5:
                self.leftButton5.setStyleSheet("background-color: green;")
                self.textBrowser.setText("\n\n".join(re.findall(".*{}.*".format(self.predefinedFilters[3]), self.wholeLog)))

            if buttonNumber == 6:
                self.leftButton6.setStyleSheet("background-color: green;")
                self.textBrowser.setText("\n\n".join(re.findall(".*{}.*".format(self.predefinedFilters[4]), self.wholeLog)))

        else:
            self.label.setText("Warning: No file imported")
            self.label.setStyleSheet("background-color: yellow; border: 1px solid black")

    def resetButtonColor(self, buttonType):
        self.buttonBackgroundColor = "rgb(60, 63, 65)" if self.darkMode == True else "white"

        if buttonType == "sideMenu":
            self.runCustomFilterButton.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
            self.leftButton1.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
            self.leftButton2.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
            self.leftButton3.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
            self.leftButton4.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
            self.leftButton5.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
            self.leftButton6.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))

        if buttonType == "topMenu":
            self.topButton1.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
            self.topButton2.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
            self.topButton3.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
            self.topButton4.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
            self.topButton5.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
            self.topButton5.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))
            self.topButton6.setStyleSheet("background-color: {};".format(self.buttonBackgroundColor))


def run():
    app = QApplication(sys.argv)
    GUI = MyWindow()
    sys.exit(app.exec_())


run()