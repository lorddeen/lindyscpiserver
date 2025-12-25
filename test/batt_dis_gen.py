import numpy
import csv
import matplotlib.pyplot as plt

#inicialization of variables
class BattDisGen:
    def __init__(self):
        pass
        self.timestep = 1 #seconds
        self.exponent = 0.005
        self.chargedbattvolt = 13 #volts
        self.dischargecurve = 4
        self.timeoffset = 3600 #seconds
        print("inicialization complete")

    def generate(self):
        #defining time array
        self.time = numpy.arange(0, self.timeoffset,self.timestep)
        print("time defined")
        #calculating discharge voltage curve
        self.discurve = self.chargedbattvolt - self.dischargecurve*numpy.exp(self.exponent*(self.time-self.timeoffset))
        print("Discharge curve calculated")
        #plotting the discharge curve
    def display(self):
        plt.plot(self.time,self.discurve)
        plt.title("Battery discharge curve for AGM Battery (common)")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Voltage (V)")
        plt.show()
        print("Discharge curve plotted")

     #testing the class 
if __name__ == "__main__":
    batt = BattDisGen()
    batt.generate()
    batt.display()  