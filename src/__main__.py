#import numpy #for algorithms
import pyvisa #for scpi commands
#import matplotlib as plt #for display
#import argparse #for command line arguments
from keysight_commands_module import KeysightScpiCommands as ksc #importing the keysight commands class
from batt_dis_gen import BattDisGen as dataset #importing the battery discharge generator class
import socket

class SCPI_Server:

    def __init__(self):
        self.datacounter = 0
        self.dataset = []
        self.time = []

    def data_generator(self):
        curve = dataset() #create an instance of the BattDisGen class
        curve.__init__()
        print("Generating data...")
        curve.generate()
        print("Data generated.")
        curve.display()
        return curve.time, curve.discurve

    def handover(self):

        print(f"Handing over data point {self.datacounter}")
        datapoint = self.dataset[self.datacounter]
        datapoint_s = f"{datapoint}\n".encode('utf-8')
        self.datacounter += 1

        return datapoint_s,
    
    def start_server(self, host, port):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #create a TCP socket
            s.bind((host, port))
            s.listen()
            print(f"SCPI Server listening on {host}:{port}")
            conn, addr = s.accept()
            with conn:
             print(f"Connected by {addr}")


             while True: #main server loop
                    data = conn.recv(1024)
                    if not data:
                       break
                    messages = data.decode('utf-8').splitlines()
                    if not messages:
                       continue
                    command = messages[0].strip()
                    if not command:
                        continue
                    if command:
                        print(f"Received command: {command}")
                        response = scpi.receive_message(command, self.handover())
                        conn.sendall(response.encode('utf-8'))



if __name__ == "__main__":
    HOST = "127.0.0.1" #localhost
    PORT = 5025#standard SCPI port
    server=SCPI_Server()
    server.__init__()
 
    try:
        server.time, server.data = server.data_generator()
    except Exception as e:
        print(f"Error generating data: {e}")
        exit(1)

    scpi = ksc() #create an instance of the keysight commands class
    server.start_server(HOST, PORT) #start the SCPI server
