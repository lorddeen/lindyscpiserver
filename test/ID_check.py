import pyvisa
import time
import datetime

#import numpy as np
#import matplotlib.pyplot as plt

#inicialization
VISA_ADRESS = 'TCPIP0::127.0.0.1::5025::SOCKET'
rm = pyvisa.ResourceManager()



#main
try:
    inst=rm.open_resource(VISA_ADRESS)
    inst.read_termination = '\n'
    inst.write_termination = '\n'
    print(inst.query("*IDN?"))
    time.sleep(2)
    print(inst.query("MEAS:VOLT?"))

except pyvisa.errors.VisaIOError as e:
    print(f"VISA Chyba: {e}")

except Exception as e:
    print(f"Obecná chyba: {e}")
finally:
    print("done")
    input("Press Enter to exit...")
    #inst.close()