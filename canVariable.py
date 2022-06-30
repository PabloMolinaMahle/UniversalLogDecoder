# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 09:33:05 2022

@author: M0188337
"""
# Struct to store timeStamp and data
class RawDataMessage:
    timeStamp: str
    variableData: str
    
class CanVariable:
    
    # Constructor
    def __init__(myCanVariable, tramaNumber, tramaName, variableName):
        myCanVariable.tramaNumber = tramaNumber
        myCanVariable.tramaName = tramaName
        myCanVariable.variableName = variableName
        myCanVariable.startBit = 0
        myCanVariable.bitLenght = 0
        myCanVariable.gain = 0
        myCanVariable.offset = 0
        myCanVariable.data = []

    # Method to set variable bit configuration
    def SetBitInfo(myCanVariable, startBit, bitLenght):
        myCanVariable.startBit = startBit
        myCanVariable.bitLenght = bitLenght
    
    # Method to set variable gain and offset corrections
    def SetGainOffset(myCanVariable, gain, offset):
        myCanVariable.gain = gain
        myCanVariable.offset = offset

    # Method to show variable trama data
    def ShowTrama(myCanVariable):
        
        return "Trama number: " + myCanVariable.tramaNumber + " Trama name: " + myCanVariable.tramaName


    def ShowVariableData(myCanVariable):
        
        return "Trama number: " + myCanVariable.tramaNumber + " Start bit: " + myCanVariable.startBit + " Length: " + myCanVariable.bitLenght + " Gain: " + myCanVariable.gain + " Offset: " + myCanVariable.offset
    
    def AppendNewData(myCanVariable, time, data):
        rawData = RawDataMessage()
        rawData.timeStamp = time
        rawData.variableData = data
        myCanVariable.data.append(rawData)