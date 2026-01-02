class KeysightScpiCommands:

    def __init__(self):
        self.ID = "KEYSIGHT TECHNOLOGIES,34461A,MY53208924,A.02.17-02.40-02.17-00.52-03-01" #Device Identification String

    def receive_message(self, command: str): # Simulate SCPI command responses
        if command == "*IDN?":
            response = self.ID
        elif command == "MEAS:VOLT?":
                response = "1.2000E+01"
        elif command == "MEAS:CURR?":
            response = "1.000E-03"
        elif command == "MEAS:RES?":
            response = "1.000E+02"
        else:
            response = "ERROR: Unknown Command"
        print(response)
                

        return response


    
# testing the class
#if __name__ == "__main__":
#    scpi = KeysightScpiCommands()
#    scpi.receive_message("*IDN?")
#    scpi.receive_message("MEAS:VOLT?")
#    scpi.receive_message("MEAS:CURR?")
#    scpi.receive_message("MEAS:RES?")
#    scpi.receive_message("DUDE")    