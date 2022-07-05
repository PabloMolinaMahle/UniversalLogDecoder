# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 09:56:55 2022

@author: M0188337
"""

class CanTrace:
    
    # Constructor
    def __init__(myCanTrace, traceNumber, traceName):
        myCanTrace.traceNumber = traceNumber
        myCanTrace.traceName = traceName
        myCanTrace.traceVariables = []
        myCanTrace.traceTimeStamp = []
        
    # Method to get trace number and name as string
    def ShowTraceName(myCanTrace):
        stringToReturn = "Trace: " + myCanTrace.traceNumber + " Trace name: " + myCanTrace.traceName
        
        return stringToReturn
    
    # Method to get complete trace data as string
    def ShowTrace(myCanTrace):
        stringToReturn = "Trace: " + myCanTrace.traceNumber + " Trace name: " + myCanTrace.traceName
        
        # Print trace info
        print(stringToReturn)
        
        # Print trace variables data
        for variable in myCanTrace.traceVariables:
            print(variable.ShowVariableData())
            
        return stringToReturn