
#import argparse #for command line arguments
from ast import While
from drivers.drivers import KeysightGenericCommands as kgc #importing the keysight commands class
from drivers.drivers import GenericCommands as gc #importing the generic commands class
from generators.batt_dis_gen import AGM12VGeneric as generator #importing the battery discharge generator class
import socket
import json
import os
from pathlib import Path
import time
import threading

class SCPI_Server:

    def __init__(self):
        #server state variables
        self.datacounter = 0
        self.data = []
        self.time = []

        #config file loading
        with open(Path(__file__).parent / "config/config.json", 'r', encoding="utf-8") as f:
            self.config = json.load(f)
            self.HOST = self.config.get("HOST")
            self.PORT = self.config.get("PORT")
            driver_name = self.config.get("DRIVER")  
            if driver_name == "keysight":
                self.parser = kgc
                print("Using Keysight driver")
            else:
                self.parser = gc
                print("Using Generic driver")

    def data_generator(self):
        curve = generator() #create an instance of the generator class
        curve.__init__()
        print("Generating data...")
        curve.generate()
        print("Data generated.")
        curve.display()
        return curve.time, curve.discurve


    def start_server(self):
        scpi = self.parser() #create an instance of the selected commands class
        
        #starting the SCPI server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #create a TCP socket
            print(f"HOST: {self.HOST}, PORT: {self.PORT}")
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))
            s.listen()
            s.settimeout(0.5) #set timeout for accepting connections
            print(f"SCPI Server listening on {self.HOST}:{self.PORT}")

            while True:
                try:
                    conn, addr = s.accept()
                    break
                except socket.timeout:
                    pass

            with conn:
             print(f"Connected by {addr}")


             while True: #main server loop
                    try:
                        data = conn.recv(1024)
                    except socket.timeout:
                        continue
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
                        if self.datacounter >= len(self.data):
                            self.datacounter = 0
                        response = scpi.receive_message(command, f"{self.data[self.datacounter]}")
                        self.datacounter += 1
                        conn.sendall(response.encode('utf-8'))

class TimeManager:
    def __init__(self):
        self.start_time = time.time()
        thread=threading.Thread(target=self.TimeDisplay,daemon=True)
        thread.start()

    def TimeDisplay(self):
        while True:
            elapsed_time = time.time() - self.start_time
            print(f"Elapsed Time: {elapsed_time:.2f} seconds")
            time.sleep(2)



if __name__ == "__main__":

    server=SCPI_Server()
    timer=TimeManager()

    try:
        server.time, server.data = server.data_generator()
    except Exception as e:
        print(f"Error generating data: {e}")
        exit(1)
    
    while True:
        try:
            server.start_server() #start the SCPI server
        except KeyboardInterrupt:
            print("Server stopped by user.")
            break