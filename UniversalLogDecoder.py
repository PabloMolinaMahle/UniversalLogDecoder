# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 12:08:10 2022

@author: M0188337
"""

from PyQt5 import QtWidgets, uic
import sys
import xlsxwriter
import time

import glob
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QHeaderView
from PyQt5 import QtCore

from canVariable import CanVariable
from m20Datalogger import M20Datalogger


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('ULDGui.ui', self) # Load the .ui file
        
        # Data file
        # self.currentDatafile = open("")
        
        # List for database
        self.variableList = []
        
        # Database dictionary
        self.dbcDict = {}
        
        # List of current data
        self.currentData = []
        
        # Database and data files
        self.dbcFile = '(\",\")'
        self.dataFile = '(\",\")'
        
        # Subscribe to button events
        self.pushButton_1.clicked.connect(self.SelectDBC)
        self.pushButton_2.clicked.connect(self.SelectFile)
        self.startButton.clicked.connect(self.StartProcess)
        self.load_dbc.clicked.connect(self.LoadDBCdata)
        self.load_data.clicked.connect(self.LoadFileData)
        
        # Subscribe to listWidget events
        # self.trama_listWidget.itemClicked.connect(self.trama_listWidget_itemClicked_event)
        # self.variables_listWidget.itemClicked.connect(self.variables_listWidget_itemClicked_event)
        # self.selectedVariables_listWidget.itemClicked.connect(self.selectedVariables_listWidget_itemClicked_event)
        
        # Clean plain text edit
        self.plainTextEdit.clear()
        
        # Show the GUI on screen
        self.show() # Show the GUI
    
    ##########################################################################################################################################
    ###
    ###                                                         Trama selection methods
    ###
    ##########################################################################################################################################
        
    # def trama_listWidget_itemClicked_event(self, item):
    #     print()
        
    # def variables_listWidget_itemClicked_event(self, item):
    #     if item.text() not in self.Variablelist["Variables"]:
    #         self.plainTextEdit.appendPlainText(item.text())
    #         self.Variablelist["Variables"].append(item.text())
        
    # def selectedVariables_listWidget_itemClicked_event(self, item):
    #     print()
    
    # def LoadTramas(self):
    #     self.listWidget.clear()
    #     for item in self.TramaDict[self.comboBox.currentText()]:
    #         self.listWidget.addItem(item)
            
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
    
    def LoadFileData(self):
        self.plainTextEdit.appendPlainText("Reading data file: " + self.dataFile[0])
        self.currentDatafile = open(self.dataFile[0],"r")
        self.currentData = M20Datalogger.ReadData(M20Datalogger, self.dataFile[0])
        
        # for item in self.currentData:
        #      print (item.time + " " + item.trace + " " + item.message)
        
    ##########################################################################################################################################
    ###
    ###                                                         Application control methods
    ###
    ##########################################################################################################################################      
    
    def StartProcess(self):
        
        self.plainTextEdit.appendPlainText("Start processing file")
        
        # Reset timer
        startProcessingTime = datetime.now()
        
        # Read data info
        for rawData in self.currentData:        
            
            # Try to get trade data
            try:
                # Get trace information from dictionary
                currTrace = self.dbcDict.get(rawData.trace)
            except Exception as e: 
                print(e)
            else:
                # print("Trace found: " + str(currTrace))
                self.DecodeData(rawData, currTrace)
            
            
            # # Find can tracce on data list
            # for i in self.variableList:
            #     # print("i.tramaNumber: " + (i.tramaNumber) + " rawData.trace: " + rawData.trace)
            #     if i.tramaNumber == rawData.trace:
                     
            #           # print ("Founded trace!")
                     
            #           # Get index of matched trace
            #           self.traceIndex = self.variableList.index(i)
                     
            #           # Add data 
            #           self.variableList[self.traceIndex].AppendNewData(rawData.time, rawData.message)
            #           # print(self.variableList[self.traceIndex].data.timeStamp)
        
        # End time
        self.plainTextEdit.appendPlainText("Time processing file: " + str(datetime.now() - startProcessingTime))
        
        # Export data to file
        self.ExportResults()
    
    def DecodeData(self, rawData, trace):
        
        # For all variables in trace
        for variable in trace:
            # print("Time: " + rawData.time + " Data: " + rawData.message + " Type: " + str(type(rawData.message)))
            variable.AppendNewData(rawData.time, self.CalculateValue(variable, rawData.message))
            #print("Time: " + rawData.time + " Data: " + str(self.CalculateValue(variable, rawData.message)))
        
    def ExportResults(self):
        
        self.plainTextEdit.appendPlainText("Exporting results")
        
        # Reset timer
        startProcessingTime = datetime.now()
        
        # Open file
        try:
            # Create new excel book
            workbook = xlsxwriter.Workbook(self.dataFile[0] + 'Proc.xlsx')
        except Exception as e: 
            print(e)
        else:
            # Add worksheet to book
            worksheet = workbook.add_worksheet()
            
            # Column counter
            columnCounter = 0

            # For each variable
            for variable in self.variableList:
                # Write time column title
                worksheet.write(0, columnCounter, variable.variableName + "_time")
                
                # Write data column title
                worksheet.write(0, columnCounter + 1, variable.variableName + "_data")
                
                # Row counter                
                rowCounter = 1
                
                # Write time data column
                for data in variable.data:
                    # Write time data
                    worksheet.write(rowCounter, columnCounter, data.timeStamp)
                    
                    # Write data
                    # print("data: " + data.variableData)
                    worksheet.write(rowCounter, columnCounter + 1, str(data.variableData))
                    
                    rowCounter += 1
                
                columnCounter += 2
                
            # Close file
            workbook.close()
            
            # End time
            self.plainTextEdit.appendPlainText("Time exporting to excel file: " + str(datetime.now() - startProcessingTime))
        
    # def contains(self, list, filter):
    #     for x in list:
    #         print("X: " + str(x) + " Index: " + str(list.index(x)))
    #         if filter(x):
    #             print("X: " + x + " Index: " + list.index(x))
    #             return list.index(x)
    #     raise ValueError
        
    def CalculateValue(self, variable, hexValue):
        
        # Preprocess HEX
        
        # Convert string to HEX and hex to bin
        value = bin(int(hexValue, base = 16))
        
        # print(value)
        # Divide with startbit and lenght (bin -> str , truncate, str -> bin)
        
        # print("Trama: " + variable.tramaNumber + " Variable name: " + variable.variableName + "Start: " + variable.startBit + " End: " + str(int(variable.startBit)) + str(int(variable.bitLenght)))
        # value = value[int(variable.startBit) + 2 :] # delete firsts elements
        # value = value[:int(variable.startBit) + int(variable.bitLenght)]
        value = self.SplitBinaryNumber(value, variable.startBit, variable.bitLenght)
        
        # print(value)
        # Convert to decimal
        value = int(value, 2)
        
        # print(value)
        # Apply gain
        value *= float(variable.gain)
        
        # print(value)
        # Apply obset
        value += float(variable.offset)
        
        return value  
    
    def SplitBinaryNumber(self, numberToSplit, startIndex, lenght):
        
        strResult = ""
        
        numberToSplit = numberToSplit[2:]
        numberToSplit = numberToSplit.zfill(64)
        
        # print("String: " + numberToSplit + " Start: " + startIndex + " Length: " + lenght)
        
        for i in range(int(startIndex), int(startIndex) + int(lenght)):
            strResult += numberToSplit[i]
        
        return strResult

    
    #     # # If no database file is selected
    #     # if self.dbcFile == "" or self.dbcFile == '(\",\")':
    #     #     self.plainTextEdit.appendPlainText("dbc is not selected")
    #     #     self.plainTextEdit.appendPlainText(str(self.dbcFile))
        
    #     # # If no data file is selected
    #     # if self.dataFile == "" or self.dataFile == '(\",\")':
    #     #     self.plainTextEdit.appendPlainText("data file is not selected")
    #     #     self.plainTextEdit.appendPlainText(str(self.dataFile))
            
    #     #if:
    #     self.plainTextEdit.appendPlainText("Start processing...")
        
    #

        
    #     #self.ProcessDatabase()
    #     #self.ReadDict(self.Variablelist)
    
    
    ##########################################################################################################################################
    ###
    ###                                                         Database methods
    ###
    ##########################################################################################################################################          
    
    # Read database
    def ReadDatabase(self):
        # Debug
        self.plainTextEdit.appendPlainText("Reading database")
        print("Start reading database")
        
        # Load data from file DBC
        # self.DBClines = self.dbcFile[0].readlines()
        self.DBClines = open(self.dbcFile[0],"r")
        
        self.currentKeyTramaNumber = ""
        self.currentKeyTramaName = ""
        
        # Database file analisis
        for line in self.DBClines:
            
            # if line starts with BO_ it's trama line
            if line.startswith("BO_ "):
                self.currentKeyTramaNumber = line.split(" ")[1]
                self.currentKeyTramaName = line.split(" ")[2]
                
                
                self.dbcDict[self.currentKeyTramaNumber] = []
                # print(self.currentKeyTramaNumber)
                
                # self.tramaDict[self.currentKeyTrama] = []
            
            # if line starts with SG_ it's variable
            if line.startswith(" SG_ "):
                self.currentVariableName = line.split(" ")[2]
                
                # print(self.currentVariableName)
                
                # Instanciate the can variable
                self.currItem = CanVariable(self.currentKeyTramaNumber, self.currentKeyTramaName, self.currentVariableName)
                
                # Add variable to the list
                self.variableList.append(self.currItem)
                self.dbcDict[self.currentKeyTramaNumber].append(self.currItem)
                
                # Set bit info
                self.SetLineBitInfo(line, self.currItem)
                
                # Set gain and offset
                self.SetLineBitAdjust(line, self.currItem)
                
            if line == "\n":
                self.currentKeyTramaNumber = ""
                self.currentKeyTramaName = ""
        
        # self.CreateDatabaseDictionary(self.variableList)
        
        # Debug
        # self.ReadDict(self.dbcDict)     
            
    def CreateDatabaseDictionary(self, variableList):
        
        # Read List and create dictionary
        for variable in variableList:
            self.variableDict[variable.tramaNumber] = variable
        
        # self.ReadDict(self.variableDict)
        
                # print(" ")
                
                # print("Bitpos: " + self.currentVariableBitPos + " BitLength: " + self.currentVariableBitLength)
                
                #self.tramaDict[self.currentKeyTrama].append(self.currentVariable)
                  
            # print(line)
            
        # self.ReadVariableDict(self.variableList)
    
    
    # Auxiliary method to show dictionary data 
    def ReadDict(self, readDict):
        
        # Print dictionary
        #print(readDict)
         
        # Print keys
        for key, value in readDict.items():
            print("Trace: " + key)
            # Print trace variables
            for var in value:
                print("  Var name: " + var.variableName)
    
    # Method to get and set bit info from a line to the given object
    def SetLineBitInfo(self, line, targetObj):
        
        # Process bit info
        self.currentVariableBitInfo = line.split(" ")[4] # Result example: 0|8@1+
        self.currentVariableBitPos = self.currentVariableBitInfo.split("|")[0] 
        self.currentVariableBitLength = self.currentVariableBitInfo.split("|")[1].split("@")[0]
        
        # Set variable bit info
        targetObj.SetBitInfo(self.currentVariableBitPos, self.currentVariableBitLength)
    
    # Method to get and set gain and obsset from a line to given object
    def SetLineBitAdjust(self, line, targetObj):
        
        # Process bit adjust (gain and offset)
        self.currentVariableBitAdjust = line.split(" ")[5] # Result example: (1,-100)
        
        # Remove first caracter
        self.currentVariableBitAdjust = self.currentVariableBitAdjust[1:] # Result example: 1,-100)
        # Remove last caracter
        self.currentVariableBitAdjust = self.currentVariableBitAdjust[:-1] # Result example: 1,-100
        
        # print(self.currentVariableBitAdjust)
        
        # Split data
        self.currentGain = self.currentVariableBitAdjust.split(",")[0]
        self.currentOffset  = self.currentVariableBitAdjust.split(",")[1]
        
        # Set bit adjust
        targetObj.SetGainOffset(self.currentGain, self.currentOffset)
    
    # Auxiliaty method to show data
    def ReadVariableDict(self, dictToRead):
        
        # Show dictionary data
        # for item in dictToRead:
        #     print(item, '->', dictToRead[item].ShowTrama())
        
        # Show list data
        for item in dictToRead:
            print(item.ShowVariableData()) 
            
            

        
        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
        
        
