# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 12:08:10 2022

@author: M0188337
"""

from PyQt5 import QtWidgets, uic
import sys
import xlsxwriter
import time
from textwrap import wrap


import glob
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QHeaderView
from PyQt5 import QtCore

from canVariable import CanVariable
from m20Datalogger import M20Datalogger
from canTrace import CanTrace

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
        self.decodeMessageButton.clicked.connect(self.DecodeMessage)
        
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
        
        # Reset timer
        startProcessingTime = datetime.now()
        
        # Read data and convert to standard format
        self.currentData = M20Datalogger.ReadData(M20Datalogger, self.dataFile[0])
        
        # End time
        self.plainTextEdit.appendPlainText("Time loading and pre-processing file: " + str(datetime.now() - startProcessingTime))
        
        # for item in self.currentData:
        #      print (item.time + " " + item.trace + " " + item.message)
        
    def DecodeMessage(self):
        # Get message
        messageToDecode = self.canMessageInput.text()
        print("Message to decode: " + messageToDecode)
        
        # Get trace
        messageTrace = self.canTraceInput.text()
        print("Message trace: " + messageTrace)
        
        print("Trace: " + self.dbcDict[messageTrace].ShowTrace())
        
        self.plainTextEdit.appendPlainText("")
        self.plainTextEdit.appendPlainText(self.dbcDict[messageTrace].ShowTraceName())
        
        # For each variable in the trace
        for variable in self.dbcDict[messageTrace].traceVariables:
            # "{:.2f}".format(float)
            # self.plainTextEdit.appendPlainText("    Var name: " + variable.variableName + " Value: " + str(self.CalculateValue(variable, messageToDecode)))
            self.plainTextEdit.appendPlainText("    Var name: " + variable.variableName + " Value: " + "{:.2f}".format(self.CalculateValue(variable, messageToDecode)))
            print(" Var name: " + variable.variableName + " Value: " + str(self.CalculateValue(variable, messageToDecode)))
        # tempVariable = self.CalculateValue(self.dbcDict[], )
        
        # Decode message
        
        # Print variable on plain text edit
        # print("tempVariable: " + tempVariable)
        
        
    ##########################################################################################################################################
    ###
    ###                                                         Application control methods
    ###
    ##########################################################################################################################################      
    
    def StartProcess(self):
        
            # self.ReadDict(self.dbcDict)
        
        # # Try to get trade data
        #     try:
        #         # Get trace information from dictionary
        #         currTrace = self.dbcDict.get("272")
        #         print(currTrace)
        #     except Exception as e: 
        #         print(e)
        #     else:
        #         # print("Trace found: " + str(currTrace))
        #         # for variable in currTrace.traceVariables:
        #         #     # Append data to the variable
        #         #     print(self.CalculateValue(variable, "246B41A4A5000000"))
                    
        #         for variable in currTrace.traceVariables:    
        #             print(self.CalculateValue(variable, "000000A5A4416B24"))

                
        
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
            
            
        #     # # Find can tracce on data list
        #     # for i in self.variableList:
        #     #     # print("i.tramaNumber: " + (i.tramaNumber) + " rawData.trace: " + rawData.trace)
        #     #     if i.tramaNumber == rawData.trace:
                     
        #     #           # print ("Founded trace!")
                     
        #     #           # Get index of matched trace
        #     #           self.traceIndex = self.variableList.index(i)
                     
        #     #           # Add data 
        #     #           self.variableList[self.traceIndex].AppendNewData(rawData.time, rawData.message)
        #     #           # print(self.variableList[self.traceIndex].data.timeStamp)
        
        # End time
        self.plainTextEdit.appendPlainText("Time processing file: " + str(datetime.now() - startProcessingTime))
        
        # Export data to file
        self.ExportResults()
    
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
        
        self.currentKeyTraceNumber = ""
        self.currentKeyTraceName = ""
        
        # Database file analisis
        for line in self.DBClines:
            
            # if line starts with BO_ it's trama line
            if line.startswith("BO_ "):
                self.currentKeyTraceNumber = line.split(" ")[1]
                self.currentKeyTraceName = line.split(" ")[2]
                
                # Add trace to trace dictionary
                self.dbcDict[self.currentKeyTraceNumber] = CanTrace(self.currentKeyTraceNumber, self.currentKeyTraceName)
                
                # print(self.currentKeyTraceNumber)

            # if line starts with SG_ it's variable
            if line.startswith(" SG_ "):
                self.currentVariableName = line.split(" ")[2]
                
                # Instanciate the can variable
                self.currItem = CanVariable(self.currentVariableName, self.dbcDict[self.currentKeyTraceNumber])
                
                # Add variable to the variable list on the trace
                self.dbcDict[self.currentKeyTraceNumber].traceVariables.append(self.currItem)
                
                # Set bit info
                self.SetLineBitInfo(line, self.currItem)
                
                # Set gain and offset
                self.SetLineBitAdjust(line, self.currItem)
                
            if line == "\n":
                self.currentKeyTraceNumber = ""
                self.currentKeyTraceName = ""
        
        # Debug
        # self.ReadVariableDict(self.dbcDict)     
    
    # Method to get and set bit info from a line to the given object
    def SetLineBitInfo(self, line, targetObj):
        
        # Process bit info
        self.currentVariableBitInfo = line.split(" ")[4] # Result example: 0|8@1+
        self.currentVariableBitPos = self.currentVariableBitInfo.split("|")[0] 
        self.currentVariableBitLength = self.currentVariableBitInfo.split("|")[1].split("@")[0] # Result example 8@1+
        self.currentVariableByteOrder = self.currentVariableBitInfo.split("|")[1].split("@")[1][0] # Result example 1
        
        # Set variable bit info
        targetObj.SetBitInfo(self.currentVariableBitPos, self.currentVariableBitLength, self.currentVariableByteOrder)
    
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
    
    def DecodeData(self, rawData, trace):
        
        # Append time to the trace
        trace.traceTimeStamp.append(rawData.time)
        
        # For all variables in trace
        for variable in trace.traceVariables:
            # Append data to the variable
            variable.varData.append(self.CalculateValue(variable, rawData.message))
            
            
            # print("Time: " + rawData.time + " Data: " + rawData.message + " Type: " + str(type(rawData.message)))
            # variable.AppendNewData(rawData.time, self.CalculateValue(variable, rawData.message))
            #print("Time: " + rawData.time + " Data: " + str(self.CalculateValue(variable, rawData.message)))

    ##########################################################################################################################################
    ###
    ###                                                         Process methods
    ###
    ##########################################################################################################################################      
     
    # Method to calculat the decimal value of a variable (variable) in a can message (hexValue)
    def CalculateValue(self, variable, hexValue):
        
        # Store the message lenght in binary (hex*4)
        messageLength = 4*len(hexValue)
        
        # Preprocess HEX
        # Divide HEX message in groups of two units
        hexValueSplited = wrap(hexValue, 2)
        
        # Invert the order of the groups
        hexValueSplited = hexValueSplited[::-1]
        
        hexValueReversed = ""
        
        for block in hexValueSplited:
            hexValueReversed += block
        
        # Convert string to HEX and hex to bin
        value = bin(int(hexValueReversed, base = 16))

        # Get the binary number of the variable
        value = self.SplitBinaryNumber(value, variable.startBit, variable.bitLenght, messageLength)
        
        # print("Current number: " + str(value) + " Byte order: " + variable.byteOrder)
        
        # Apply bit order (1 = intel, 0 = motorola)
        if variable.byteOrder == "0":
            # If is motorola order, invert the string
            self.plainTextEdit.appendPlainText("")
            self.plainTextEdit.appendPlainText("#################################")
            self.plainTextEdit.appendPlainText("WARNING!!!! : Variable with inverted byte order found: CHECK IF WORKS : Contact to pablo.molina@mahle.com")
            self.plainTextEdit.appendPlainText("#################################")
            self.plainTextEdit.appendPlainText("")
            
            print("Variable with inverted byte order found: CHECK IF WORKS")
            
            value = self.InvertByteOrder(value)
        
        # Convert to decimal
        value = int(value, 2)
        
        # Apply gain
        value *= float(variable.gain)
        
        # Apply obset
        value += float(variable.offset)
        
        # print("Final value: " + str(value))
        
        return value  
     
    # Method to extract the binary value of the current variable
    def SplitBinaryNumber(self, numberToSplit, startIndex, lenght, messageLength):
         
        strResult = ""
        
        # print(numberToSplit)
        
        numberToSplit = numberToSplit[2:]
        
        # print(numberToSplit)
        numberToSplit = numberToSplit.zfill(messageLength)
        
        # print(numberToSplit)
        
        # print(numberToSplit)
        
        # print("String: " + numberToSplit + " Start: " + startIndex + " Length: " + lenght)
        
        # for i in range(int(startIndex), int(startIndex) + int(lenght)):
        #     strResult += numberToSplit[i]
        
        
        for i in range(messageLength - int(startIndex) - int(lenght), messageLength - int(startIndex)):
            strResult += numberToSplit[i]
        
        # print("strResult: " + strResult)
        
        return strResult
   
    # Method to invert Byte order for Motorola type variables
    def InvertByteOrder(self, numberToInvert):
                
        # print("Start number: " + str(numberToInvert))
        
        # str to hex
        numberToInvert = hex(int(numberToInvert, 2))
        
        # print("Hex number: " + str(numberToInvert))
        
        # Remove 0x letter of hex number
        numberToInvert = numberToInvert[2:]
        # print("Remove 0x from hex: " + str(numberToInvert))
        
        # Split in groups
        numberToInvert = wrap(numberToInvert, 2)
        
        # print("Splited number: " + str(numberToInvert))
        
        # Invert order
        numberToInvert = numberToInvert[::-1]
        # print("Inverted number list: " + str(numberToInvert))
        
        invertedNumber = ""
        
        # Concatenate splited hex
        for block in numberToInvert:
            invertedNumber += block
        
        # print("Inverted number concatenated: " + str(invertedNumber))
        
        # Convert to binary
        invertedNumber = int(invertedNumber, 16)
        # print("Convert to dec: " + str(invertedNumber))
        
        # Convert to bin
        invertedNumber = bin(invertedNumber)
        # print("Convert to bin: " + str(invertedNumber))
                
        # Remove 0b letter of hex number
        invertedNumber = invertedNumber[2:]
        # print("Remove 0b from bin: " + str(invertedNumber))
        
        return invertedNumber
     

    ##########################################################################################################################################
    ###
    ###                                                         Export methods
    ###
    ##########################################################################################################################################      

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
            
            ## Cell format
            
            # TimeStamp title format
            timeStampTitleFormat = workbook.add_format()
            timeStampTitleFormat.set_bg_color("#8DEEEE")
            # timeStampTitleFormat.set_rotation(90)
            
            # Variable title format
            variableTitleFormat = workbook.add_format()
            variableTitleFormat.set_bg_color("#B4EEB4")
            # variableTitleFormat.set_rotation(70)
            
            # Column counter
            columnCounter = 0
            
            # Debug
            # print("DBC lenght: " + str(len(self.dbcDict)))
            # for key in self.dbcDict:
            #     print("Trace: " + self.dbcDict[key].traceNumber + " number of time data: " + str(len(self.dbcDict[key].traceTimeStamp)))
            
            # Trace
            for trace in self.dbcDict:
                # If trace has timestamp
                
                # print("trace.traceTimeStamp: " + self.dbcDict[trace].traceNumber + " trace name: " + self.dbcDict[trace].traceName)
                
                if len(self.dbcDict[trace].traceTimeStamp) > 0:
                    # Write time column title
                    worksheet.write(0, columnCounter, self.dbcDict[trace].traceName + "_time", timeStampTitleFormat)
                    
                    # Row counter                
                    rowCounter = 1
                    
                    # Write time column data
                    for timeStamp in self.dbcDict[trace].traceTimeStamp:
                        worksheet.write(rowCounter, columnCounter, timeStamp)
                        rowCounter += 1 # Counter increment for next row
                        
                    # Increase colum counter for the first variable of this trace
                    columnCounter += 1
                    
                    # Write variables
                    for traceVariable in self.dbcDict[trace].traceVariables:
                        # Write variable title
                        worksheet.write(0, columnCounter, traceVariable.variableName, variableTitleFormat)
                        
                        # Row counter reset            
                        rowCounter = 1
                        
                        # Write variable data
                        for variableData in traceVariable.varData:
                            # Write data replacing "." by ","
                            worksheet.write_number(rowCounter, columnCounter, variableData)
                            rowCounter += 1 # Counter increment for next row
                        
                        # Increase colum counter for the next variable column
                        columnCounter += 1
                
            # Block panels
            worksheet.freeze_panes(1, 0)
                
            # Close file
            workbook.close()
            
            # End time
            self.plainTextEdit.appendPlainText("Time exporting to excel file: " + str(datetime.now() - startProcessingTime))
        
    ##########################################################################################################################################
    ###
    ###                                                         Auxiliary methods
    ###
    ##########################################################################################################################################            
    
    # Auxiliary method to show dictionary data 
    def ReadDict(self, readDict):
        
        # Print dictionary
        #print(readDict)
         
        # Print keys
        for key, value in readDict.items():
            print("Trace: " + key)
            # Print trace variables
            for var in readDict[key].traceVariables:
                print("  Var name: " + var.variableName)
    
    # Auxiliaty method to show data
    def ReadVariableDict(self, dictToRead):
        
        # Show dictionary data
        # for item in dictToRead:
        #     print(item, '->', dictToRead[item].ShowTrama())
        
        # Show list data
        for trace in dictToRead:
            print("Trace: " + dictToRead[trace].traceNumber + " Trace name: " + dictToRead[trace].traceName)
            for var in dictToRead[trace].traceVariables: 
                print(var.ShowVariableData()) 
            
                   
        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
        
        
