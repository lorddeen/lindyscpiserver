#import numpy #for algorithms
import pyvisa #for scpi commands
#import matplotlib as plt #for display
#import argparse #for command line arguments
from keysight_commands_module import KeysightScpiCommands as ksc #importing the keysight commands class
from batt_dis_gen import BattDisGen as bdg #importing the battery discharge generator class
import socket


def data_generator(self, timestep, exponent, chargedbattvolt, dischargecurve, timeoffset):
    curve = bdg()
    curve.generate(timestep, exponent, chargedbattvolt, dischargecurve, timeoffset)
    return batt.time, batt.discurve

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
                response = scpi.receive_message(command)
                conn.sendall(response.encode('utf-8'))


if __name__ == "__main__":
    HOST = "127.0.0.1" #localhost
    PORT = 5025#standard SCPI port
    batt = bdg()
    curve.timestep = 1 #seconds
    curve.exponent = 0.005
    curve.chargedbattvolt = 13 #volts
    curve.dischargecurve = 4
    curve.timeoffset = 3600 #seconds
    print("inicialization complete")

    time, data = data_generator()
    batt.display(time, data)
    scpi = ksc() #create an instance of the keysight commands class
    start_server(scpi, HOST, PORT) #start the SCPI server
