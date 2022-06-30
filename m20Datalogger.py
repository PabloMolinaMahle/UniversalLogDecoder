# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 12:48:10 2022

@author: M0188337
"""

from datetime import datetime

# Struct to store raw CAN data
class RawDataMessage:
    time: str
    trace: str
    message: str

class M20Datalogger:
    
  
    def LoadDataFile(self):
        pass
    
    
    def ReadData(self, file):
        
        # Open file
        self.data = open(file,"r")
        
        # Read file data
        self.datos = self.data.readlines()
        
        # List to store splited data
        self.splitedData = []
        
        # Start reading data and spliting
        for item in self.datos:
            
            # First split
            self.time, self.can, self.trace = item.split(" ")
            
            # Check if is a line to process
            if self.can == "can0":
                # initzialice new raw data variable
                self.currRawDatamessage = RawDataMessage()
                
                # process time
                self.currRawDatamessage.time = self.processTime(self.time)
                
                # process trace CONVERTED TO DECIMAL!
                self.currRawDatamessage.trace = str(int(self.trace.split("#")[0], 16))
                
                # process message
                self.currRawDatamessage.message = self.trace.split("#")[1]
                
                # append data
                self.splitedData.append(self.currRawDatamessage)
        
        # Debug
        # for item in self.splitedData:
        #     print(item)
            
        return self.splitedData
    
    # Method to process time variable
    def processTime(timeToProcess):
        
        # Remove first caracter
        timeToProcess = timeToProcess[1:]
        # Remove last caracter
        timeToProcess = timeToProcess[:-1]
        
        # Split time 
        realPart, decimalPart = timeToProcess.split(".")
        
        # Convert time Epoch to real time
        dateAndTime = datetime.fromtimestamp(int(realPart))
        
        # Convert date and time to excel format
        dateAndTime = str(datetime.fromtimestamp(int(realPart)).hour) + ":" + str(datetime.fromtimestamp(int(realPart)).minute) + ":" + str(datetime.fromtimestamp(int(realPart)).second)  + "," + str(datetime.fromtimestamp(int(realPart)).microsecond)
        
        # Add decimal part
        dateAndTime += decimalPart
        
        return str(dateAndTime)

    