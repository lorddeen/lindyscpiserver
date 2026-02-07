
#import argparse #for command line arguments
from ast import While
from drivers.drivers import KeysightGenericCommands as kgc #importing the keysight commands class
from drivers.drivers import GenericCommands as gc #importing the generic commands class
from generators.generators import AGM12VGeneric as generator #importing the battery discharge generator class
import socket
import json
import os
from pathlib import Path
import time
import threading
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
            self.timer_type = self.config.get("TIMER")
        
      



    def data_generator(self):
         #create an instance of the generator class
        #curve = generator()
        curve.__init__()
        print("Generating data...")
        curve.generate_fullset()
        print("Data generated.")
        #curve.display()
        return curve.time, curve.discurve


    def start_server(self):    
        self.time, self.data = self.data_generator()
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
                        #if self.datacounter >= len(self.data):
                            #self.datacounter = 0
                        
                        current_time = time.time() - timer.start_time
                        print(f"Current Time: {current_time}")
                        response = scpi.receive_message(command, f"{curve.generate(current_time)}")
                        print(f"Sending response: {response} for time {current_time}")
                        #self.datacounter += 1
                        conn.sendall(response.encode('utf-8'))

class TimeManager:
    def __init__(self):
        self.start_time = time.time()
        self.start_time_iso = time.ctime()
        print(f"Timer started at {self.start_time_iso}")
        thread=threading.Thread(target=self.TimeDisplay,daemon=True)
        #thread.start()

    def TimeDisplay(self):
        while True:
            elapsed_time = time.time() - self.start_time
            print(f"Elapsed Time: {elapsed_time:.2f} seconds")
            time.sleep(2)

class GUI:
    def GUI(self):
        self.root = tk.Tk()
        self.root.title("SCPI Server GUI")
        self.root.geometry("1000x1000")
        label = tk.Label(self.root, text="SCPI Server is running...")
        label.grid(column=0, row=0, padx=10, pady=10)
        button = tk.Button(self.root, text="Start Server", command=self.root.quit)
        button.grid(column=0, row=1, padx=10, pady=10)
        HOST_var=tk.StringVar(value=server.HOST)
    
        label_HOST=tk.Label(self.root,text="HOST:").grid(column=0, row=2, padx=10, pady=10)
        HOST_entry=tk.Entry(self.root,textvariable=HOST_var)
        HOST_entry.grid(column=0, row=3, padx=10, pady=10)

        label_PORT=tk.Label(self.root,text="PORT:").grid(column=0, row=4, padx=10, pady=10)
        PORT_var=tk.StringVar(value=str(server.PORT))
        PORT_entry=tk.Entry(self.root,textvariable=PORT_var)
        PORT_entry.grid(column=0, row=5, padx=10, pady=10)
        self.plotting()
        self.root.mainloop()
        

    def plotting(self):
        fig= curve.display()
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(column=0, row=6, padx=10, pady=10)


 

if __name__ == "__main__":
    timer=TimeManager()
    server=SCPI_Server()
    curve = generator()
    display = GUI()
    #GUI_thread = threading.Thread(target=display.GUI, daemon=True)
    #GUI_thread.start()
    
    #generate the data set (for voltage measurements)
    try:
        server_thread = threading.Thread(target=server.start_server, daemon=True)
        try:
            server_thread.start() 
        except Exception as e:
            print(f"Error starting server thread: {e}")
        except KeyboardInterrupt:
            print("Server thread interrupted by user.")
            exit(0)
 

        #print("Data generation complete.")
        display.GUI()
    except Exception as e:
        print(f"Error in main execution: {e}")  


    