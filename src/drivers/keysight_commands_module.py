class KeysightGenericCommands:

    def __init__(self):
        self.ID = "LINDY TECHNOLOGIES,34461A,CZ26A10001,A.01.00-00.00-00.00-00.00-00-00" #Device Identification String
        self.STB = 0x00 #Status Byte register initialization
        self.QSR = 0x00 #Questionable Status Register initialization
        self.MODE = "VOLT" #Measurement mode initialization
        self.RANGE = "AUTO" #Measurement range initialization
        self.RESOLUTION = 5 #Measurement resolution initialization

    def receive_message(self, command: str, datapoint_s: str): # Simulate SCPI command responses
        if not datapoint_s:
            datapoint_s = "ERROR: NO DATA"

        if command == "*IDN?":
            response = self.ID
        elif command == "MEAS:VOLT?":
                
                response = f"{float(datapoint_s):.5E}"#formatting the voltage measurement in scientific notation
        elif command == "MEAS:CURR?":
            response = "NICE TRY, NO CURRENT MEASUREMENT"
        elif command == "MEAS:RES?":
            response = "NICE TRY, NO RESISTANCE MEASUREMENT"
        else:
            response = "ERROR: Unknown Command"
        print(response)
                

        return response

