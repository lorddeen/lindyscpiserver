import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt

#inicialization
VISA_ADRESS = 'TCPIP0:127.0.0.1::5025::SOCKET'
rm = pyvisa.ResourceManager()



#main
try:
    inst=rm.open_resource(VISA_ADRESS)
    print(inst.query("*IDN?"))
finally:
    inst.close()