# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 12:08:10 2022

@author: M0188337
"""

from PyQt5 import QtWidgets, uic
import sys
import glob
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QHeaderView
from PyQt5 import QtCore

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('ULDGui.ui', self) # Load the .ui file
        
        # Dictionary for database
        self.tramaDict = {}
        
        # Dicctionary for can message
        self.Variablelist={"Variables":[],"Trama":[],"startbit":[],"endbit":[],"Gain":[],"Offset":[],"timestamp":[[]],"data":[[]]}
        
        self.dbcFile = '(\",\")'
        self.dataFile = '(\",\")'
        
        # Subscribe to button events
        self.pushButton_1.clicked.connect(self.SelectDBC)
        self.pushButton_2.clicked.connect(self.SelectFile)
        self.pushButton_3.clicked.connect(self.StartProcess)
        self.load_dbc.clicked.connect(self.LoadDBCdata)
        
        # Subscribe to listWidget events
        self.trama_listWidget.itemClicked.connect(self.trama_listWidget_itemClicked_event)
        self.variables_listWidget.itemClicked.connect(self.variables_listWidget_itemClicked_event)
        self.selectedVariables_listWidget.itemClicked.connect(self.selectedVariables_listWidget_itemClicked_event)
        
        # Clean plain text edit
        self.plainTextEdit.clear()
        
        self.show() # Show the GUI
    
    
    
    # Process data
    def ProcessDatabase(self):
        
        # Load data from file DBC
        self.DBClines = open(self.dbcFile[0],"r")
        
        # For all selected variables
        for i in range(len(self.Variablelist["Variables"])):
            
            # This first part add the selected tramas of the app to the dictionary
            # For each key in TranaDict
            for key in self.TramaDict:
                # For each item in TramaDict
                for item in self.TramaDict[key]:
                    # If item is on selected variables, append it
                    if self.Variablelist["Variables"][i] == item:
                        self.Variablelist["Trama"].append(key)
                      
            
            for line in self.DBClines:
                if (self.Variablelist["Variables"][i] in line) and ("CM_" not in line) and ("VAL_" not in line) and ("SB_DU_Index = 1" not in line) and ("BO_" not in line):

                    ####Start/end Bits
                    Split1= line.split("|")
                    Split2=Split1[0].split(" ")
                    self.Variablelist["startbit"].append(Split2[4])
                    #print(Split1)
                    Split3=Split1[1].split("@")
                    length=Split3[0]
                    self.Variablelist["endbit"].append(str(int(self.Variablelist["startbit"][i])+int(length)))
                    
                    ###Conversion
                    Split4=Split1[1].split(" ")
                    Split5=Split4[1].split(",")
                    self.Variablelist["Gain"].append(Split5[0].split("(")[1])
                    self.Variablelist["Offset"].append(Split5[1].split(")")[0])
                    
                if ((self.Variablelist["Trama"][i]) in line) and ("BO_" in line) and ("GenMsgDelayTime" not in line) and ("GenMsgCycleTime" not in line):
                    var=line.split(" ")
                    #print(self.Variablelist["Trama"],line, var[1])
                    ID=hex(int(var[1]))[2:]
                    self.Variablelist["Trama"][i]=ID
    
    # Read data file
      
    
    # Convert data file 
    
    ##########################################################################################################################################
    ###
    ###                                                         Trama selection methods
    ###
    ##########################################################################################################################################
        
    def trama_listWidget_itemClicked_event(self, item):
        print()
        
    def variables_listWidget_itemClicked_event(self, item):
        if item.text() not in self.Variablelist["Variables"]:
            self.plainTextEdit.appendPlainText(item.text())
            self.Variablelist["Variables"].append(item.text())
        
    def selectedVariables_listWidget_itemClicked_event(self, item):
        print()
    
    def LoadTramas(self):
        self.listWidget.clear()
        for item in self.TramaDict[self.comboBox.currentText()]:
            self.listWidget.addItem(item)
            
    ##########################################################################################################################################
    ###
    ###                                                         Button events methods
    ###
    ##########################################################################################################################################        
    
    def SelectDBC(self):
        self.dbcFile = QFileDialog.getOpenFileName(self,"Choose database (dbc)","C:\\Users\\M0188337\\Desktop\\M20 script test", "Database file (*.dbc)")
        self.lineEdit_1.setText(str(self.dbcFile[0]))
    
    def LoadDBCdata(self):
        self.ReadDatabase()
    
    def SelectFile(self):
        self.dataFile = QFileDialog.getOpenFileName(self,"Choose Directory1","C:\\Users\\M0188337\\Desktop\\M20 script test", "log file (*.log)")
        self.lineEdit_2.setText(str(self.dataFile[0]))
    
    def StartProcess(self):

        # # If no database file is selected
        # if self.dbcFile == "" or self.dbcFile == '(\",\")':
        #     self.plainTextEdit.appendPlainText("dbc is not selected")
        #     self.plainTextEdit.appendPlainText(str(self.dbcFile))
        
        # # If no data file is selected
        # if self.dataFile == "" or self.dataFile == '(\",\")':
        #     self.plainTextEdit.appendPlainText("data file is not selected")
        #     self.plainTextEdit.appendPlainText(str(self.dataFile))
            
        #if:
        self.plainTextEdit.appendPlainText("Start processing...")
        
        self.ProcessDatabase()
        self.ReadDict(self.Variablelist)
        
    # Read database
    def ReadDatabase(self):
        self.plainTextEdit.appendPlainText("Reading database")
        print("Start reading database")
        
        # Load data from file DBC
        # self.DBClines = self.dbcFile[0].readlines()
        self.DBClines = open(self.dbcFile[0],"r")
        
        self.currentKeyTrama = ""
        
        # Database file analisis
        for line in self.DBClines:
            
            # if line starts with BO_ it's trama line
            if line.startswith("BO_ "):
                self.currentKeyTrama = line.split(" ")[1]
                # print(self.currentKeyTrama)
                self.tramaDict[self.currentKeyTrama] = []
            
            # if line starts with SG_ it's variable
            if line.startswith(" SG_ "):
                self.currentVariable = line.split(" ")[2]
                # print(self.currentVariable)
                self.tramaDict[self.currentKeyTrama].append(self.currentVariable)
                  
            # print(line)
            
        self.ReadDict(self.tramaDict)
    
    # Load database data
    def LoadDatabaseData(self):
        # Dependerá de las variables que se seleccionen en el interface, de momento se cargan todas
        
        # Read again database to load data
        for line in self.DBClines:
            
            # if line starts with BO_ it's trama line
            if line.startswith("BO_ "):
                self.currentKeyTrama = line.split(" ")[1]
                # print(self.currentKeyTrama)
                self.tramaDict[self.currentKeyTrama] = []
            
            # if line starts with SG_ it's variable
            if line.startswith(" SG_ "):
                self.currentVariable = line.split(" ")[2]
                # print(self.currentVariable)
                self.tramaDict[self.currentKeyTrama].append(self.currentVariable)
        
    
    # Auxiliary method to show dictionary data 
    def ReadDict(self, readDict):
        
        # print dictionary
        print(readDict)
         
        # print length of dictionary
        print("Length:", len(readDict))
         
        # print type
        print(type(readDict))
        
        
        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
        
        
