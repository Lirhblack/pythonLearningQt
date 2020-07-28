############################################################
######## Created By : Fernando Barrueto - Lirh  ##########
######## Date : 28/07/2020                      ##########
######## Reason: Just learning some of Qt       ##########
############################################################

import sys, psutil, os, multiprocessing
import time, datetime
import pygame


from functools import partial


from PySide2.QtWidgets import QApplication, QButtonGroup, QPushButton, QScrollArea, QLineEdit, QRadioButton, QGroupBox, QMenu
from PySide2.QtCore import QFile, QIODevice, QTime, QTimer
from PySide2.QtUiTools import QUiLoader


class getProcess():
    #Initialize the Arrays
    def __init__(self):
        self.listOfProcess = []
        self.rawProcess = []

    #Get Raw Process
    def get_rawProcess(self):
        rawProcess = []
        for proc in psutil.process_iter():
            try:
                processName = proc.name()
                rawProcess.append(processName)

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                print("There is an error, probably : No Process, AccessDenied or ZombieProcess")
    
        rawProcess.sort()
        self.rawProcess = list(dict.fromkeys(rawProcess))

    #Delete the Windows process that we dont want from the raw list
    def deletingWindowsProcess(self):
        listOfWindowsProcess = ["Agent.exe", "ApplicationFrameHost.exe", "CompPkgSrv.exe", "IntelCpHDCPSvc.exe", "IntelCpHeciSvc.exe", "LockApp.exe", 
                                "MemCompression", "MicrosoftEdge.exe", "MicrosoftEdgeCP.exe", "MicrosoftEdgeSH.exe", "MsMpEng.exe", "NVIDIA Share.exe",
                                "NVIDIA Web Helper.exe", "NisSrv.exe", "PresentationFontCache.exe", "Registry", "RtkAudUService64.exe", "RuntimeBroker.exe",
                                "SearchApp.exe", "SearchFilterHost.exe", "SearchIndexer.exe", "SearchProtocolHost.exe", "SecurityHealthService.exe", 
                                "SecurityHealthSystray.exe", "SettingSyncHost.exe", "SgrmBroker.exe", "ShellExperienceHost.exe", "SkypeApp.exe",
                                "SkypeBackgroundHost.exe", "StartMenuExperienceHost.exe", "System", "System Idle Process", "TextInputHost.exe",
                                "WmiPrvSE.exe", "audiodg.exe", "browser_broker.exe", "conhost.exe", "crss.exe", "ctfmon.exe", "designer.exe",
                                "dllhost.exe", "dwm.exe", "explorer.exe", "fontdrvhost.exe", "igfxCUIService.exe", "igfxEM.exe", "lsass.exe",
                                "nvcontainer.exe", "nvsphelper64.exe", "powershell.exe", "services.exe", "sihost.exe", "smss.exe", "spoolsv.exe",
                                "sqlwrite.exe", "svchost.exe", "taskhostw.exe", "wininit.exe", "winlogon.exe", "csrss.exe", "GoogleCrashHandler64.exe",
                                "GameBarPresenceWriter.exe", "backgroundTaskHost.exe", "smartscreen.exe"]
        
        self.listOfProcess = list(set(self.rawProcess).difference(listOfWindowsProcess))
        return self.listOfProcess

    #Just Make Thinks LUL
    def makeThinks(self):
        self.get_rawProcess()
        done = self.deletingWindowsProcess()
        return done

class windowsDefault():
    #Initialize all the values
    def __init__(self, windowsTitle, processList, uiFile='desktop.ui',  app=QApplication([]), value=0):
        self.uiFile= uiFile
        self.windows = None
        self.title = windowsTitle
        self.app = app
        self.processList = processList
        self.value = value
        self.stop = False
        pygame.mixer.init()
        

    #Making the windows, setting self.windows
    def makeWindows(self):
        self.uiFile = QFile(self.uiFile)

        if not self.uiFile.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(self.uiFile, self.uiFile.errorString))
            sys.exit(1)

        self.windows = QUiLoader().load(self.uiFile)
        self.uiFile.close()

        if not self.windows:
            print(QUiLoader.errorString())
            sys.exit(1)

    #Just put tittle and show
    def putTittle(self):
        self.windows.setWindowTitle(self.title)
        self.windows.show()
        sys.exit(self.app.exec_())

    #Setting the processWindows to default
    def defaultProcessWindows(self):
        for lineEdits in self.windows.scrollArea.findChildren(QLineEdit):
            lineEdits.setHidden(True)
            lineEdits.setReadOnly(True)
        
        for pushButtons in self.windows.scrollArea.findChildren(QPushButton):
            pushButtons.setHidden(True)
   
    #Setting the Details windows to default
    def defaultDetailsWindow(self):
        self.windows.btnGroupDetails = QButtonGroup()

        for rdButtons in self.windows.groupBox.findChildren(QRadioButton):
            self.windows.btnGroupDetails.addButton(rdButtons)
        
        self.windows.lineEdit_nameofProcess.setEnabled(False)
        self.windows.lineEdit_nameofProcess.setReadOnly(True)
        self.windows.radioButton_1.setChecked(True)

    #Setting the Notifications windows to default
    def defaultNotificationWindows(self):
        self.windows.btnGroupNotifications = QButtonGroup()

        for rdButtons in self.windows.groupBox_2.findChildren(QRadioButton):
            self.windows.btnGroupNotifications.addButton(rdButtons)

        for qPushButtons in self.windows.groupBox_2.findChildren(QPushButton):
            qPushButtons.clicked.connect(lambda: self.reproduceSong())

        
        
    #Function for button pressed        
    def processButtonPressed(self, text):
        self.windows.lineEdit_nameofProcess.setEnabled(True)
        self.windows.lineEdit_nameofProcess.setText(text)

        for rdButton in self.windows.groupBox.findChildren(QRadioButton):
            if rdButton.isChecked() == True:
                self.value = int(rdButton.text().split(" ")[0])
                break
        


    #Function that reproduce a .mp3 song
    def reproduceSong(self):
        pygame.mixer.music.stop()
        aux = ""
        for rdButton in self.windows.groupBox_2.findChildren(QRadioButton):
            if rdButton.isChecked() == True:
                aux = str(rdButton.text() + '.wav')
                break

        pygame.mixer.music.load(aux)
        pygame.mixer.music.play(self.value)
        
        

    #Function that allow lineEdit in process windows and fill the Text camps
    def putProcessInProcessWindows(self):
        for x in range(1, len(self.processList)):
            lineEdit = self.windows.scrollArea.findChild(QLineEdit, 'lineEdit1_' + str(x))
            lineEdit.setHidden(False)
            lineEdit.setText(self.processList[x-1])

            clickButton = self.windows.scrollArea.findChild(QPushButton, 'clickButton01_' + str(x))
            clickButton.setHidden(False)


            clickButton.clicked.connect(partial(lambda x=x: self.processButtonPressed(self.processList[x-1])))
    
    #Function for the reset Button
    def cleanWindows(self):
        self.defaultProcessWindows()
        self.windows.lineEdit_nameofProcess.setText("")
        pygame.mixer.music.stop()
    
    #Better idea its just add all this attributes to the desktop.ui file, but, its for learning process, dont make drama!        
    def defaultWindowsApplication(self):
        windowApp.makeWindows()
        self.defaultProcessWindows()
        self.defaultDetailsWindow()
        self.defaultNotificationWindows()
        self.windows.pushButton_Process.clicked.connect(lambda: self.putProcessInProcessWindows())
        self.windows.pushButton_Reset.clicked.connect(lambda: self.cleanWindows())
        self.windows.radioButton_notification_1.setChecked(True)
        windowApp.putTittle()
    

processList = getProcess().makeThinks()
windowApp = windowsDefault('Desktop Notification V.1.0', processList)

windowApp.defaultWindowsApplication()
