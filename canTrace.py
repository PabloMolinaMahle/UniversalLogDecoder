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
        