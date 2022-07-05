# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 09:33:05 2022

@author: M0188337
"""
    
class CanVariable:
    
    # Constructor
    def __init__(myCanVariable, variableName, canTrace):
        myCanVariable.variableName = variableName
        myCanVariable.canTrace = canTrace
        myCanVariable.startBit = 0
        myCanVariable.bitLenght = 0
        myCanVariable.byteOrder = 0
        myCanVariable.gain = 0
        myCanVariable.offset = 0
        myCanVariable.varData = []

    # Method to set variable bit configuration
    def SetBitInfo(myCanVariable, startBit, bitLenght, byteOrder):
        myCanVariable.startBit = startBit
        myCanVariable.bitLenght = bitLenght
        myCanVariable.byteOrder = byteOrder
    
    # Method to set variable gain and offset corrections
    def SetGainOffset(myCanVariable, gain, offset):
        myCanVariable.gain = gain
        myCanVariable.offset = offset

    # Method to sow Variable data
    def ShowVariableData(myCanVariable):
        
        return "   Variable name: " + myCanVariable.variableName + " Start bit: " + myCanVariable.startBit + " Length: " + myCanVariable.bitLenght + " ByteOrder: " + myCanVariable.byteOrder + " Gain: " + myCanVariable.gain + " Offset: " + myCanVariable.offset
    
    