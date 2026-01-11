
#import argparse #for command line arguments
from drivers.keysight_commands_module import KeysightGenericCommands as kgc #importing the keysight commands class
from generators.batt_dis_gen import AGM12VGeneric as generator #importing the battery discharge generator class
import socket
import json

class SCPI_Server:

    def __init__(self):
        self.datacounter = 0
        self.data = []
        self.time = []

    def data_generator(self):
        curve = generator() #create an instance of the generator class
        curve.__init__()
        print("Generating data...")
        curve.generate()
        print("Data generated.")
        curve.display()
        return curve.time, curve.discurve


    def start_server(self, host, port):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #create a TCP socket
            s.bind((host, port))
            s.listen()
            print(f"SCPI Server listening on {host}:{port}")
            


            while True: #main server loop - waits for new connections
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True: #connection loop - waits for messages from the client
                        try:
                            data = conn.recv(1024)
                            if not data:
                                print(f"Connection with {addr} closed.")
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
                                conn.sendall((response+"\n").encode('utf-8'))
                        except ConnectionResetError:
                            print(f"Connection with {addr} reset.")
                            break
                        except Exception as e:
                            print(f"UnexpectedError: {e}")
                            break
                        except KeyboardInterrupt:
                            print("Server loop stopped by user...")
                            break


if __name__ == "__main__":
    HOST = "127.0.0.1" #localhost
    PORT = 5025#standard SCPI port
    server=SCPI_Server()
    server.__init__()
 
    try:
        server.time, server.data = server.data_generator()
    except Exception as e:
        print(f"Error generating data: {e}")
        input("Press Enter to exit...")
        exit(1)

        

    scpi = kgc() #create an instance of the keysight commands class
    try:
        scpi.__init__() #initialize the keysight commands class
        server.start_server(HOST, PORT) #start the SCPI server
    except KeyboardInterrupt:
        input("Press Enter to exit...")
    finally:
        print("Server stopped.")