
#import argparse #for command line arguments

#main imports
import json
#import os
from pathlib import Path
import threading

# server and data imports
from ast import While
from drivers.drivers import KeysightGenericCommands as kgc #importing the keysight commands class
from drivers.drivers import GenericCommands as gc #importing the generic commands class
from generators.generators import AGM12VGeneric as generator #importing the battery discharge generator class
import socket
import time

#GUI imports
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
        


    def start_server(self):    
        scpi = self.parser() #create an instance of the selected commands class
        self.running = True
        #starting the SCPI server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: #create a TCP socket
            print(f"HOST: {self.HOST}, PORT: {self.PORT}")
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.HOST, self.PORT))
            s.listen()
            s.settimeout(0.5) #set timeout for accepting connections
            print(f"SCPI Server listening on {self.HOST}:{self.PORT}")

            while self.running:
                try:
                    conn, addr = s.accept()
                    break
                except socket.timeout:
                    pass

            with conn:
             print(f"Connected by {addr}")


             while server.running: #main server loop
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

    def stop_server(self):
        print("Stopping server...")
        self.running = False
        # Implement server shutdown logic if needed
        # For example, you could set a flag to exit the main loop in start_server
        # or close the socket to stop accepting new connections.

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
    def __init__(self):
        print("Initializing GUI...")
        self.root = tk.Tk()
        self.curve = curve
        self.server = server
        self.server_thread = None
   
    def GUI(self):
        self.root.title("SCPI Server GUI")
        self.root.geometry("1000x500")
        label = tk.Label(self.root, text="SCPI Server is running...")
        label.grid(column=0, row=0, padx=10, pady=10)
        button_start = tk.Button(self.root, text="Start Server", command=self.start_server).grid(column=1, row=1, padx=10, pady=10)
        button_stop = tk.Button(self.root, text="Stop Server", command=self.stop_server).grid(column=0, row=1, padx=10, pady=10)
    
        #config entries
        self.HOST_var=tk.StringVar(value=server.HOST)
        label_HOST=tk.Label(self.root,text="HOST:").grid(column=0, row=2, padx=10, pady=10)
        HOST_entry=tk.Entry(self.root,textvariable=self.HOST_var)
        HOST_entry.grid(column=1, row=2, padx=10, pady=10)

        label_PORT=tk.Label(self.root,text="PORT:").grid(column=0, row=4, padx=10, pady=10)
        self.PORT_var=tk.IntVar(value=server.PORT)
        PORT_entry=tk.Entry(self.root,textvariable=self.PORT_var)
        PORT_entry.grid(column=1, row=4, padx=10, pady=10)

        #plotting the discharge cuve
        self.plotting()

        # main loop for the GUI
        self.root.mainloop()
        
    def start_server(self):
        self.server.HOST = self.HOST_var.get()
        self.server.PORT = self.PORT_var.get()
  
        if self.server_thread is None or not self.server_thread.is_alive():
            self.server_thread = threading.Thread(target=self.server.start_server, daemon=True)
            try:
                self.server_thread.start() 
            except Exception as e:
                print(f"Error starting server thread: {e}")
            except KeyboardInterrupt:
                print("Server thread interrupted by user.")

    def stop_server(self):
        self.server.stop_server()
        if self.server_thread is not None:
            self.server_thread.join(timeout=5)
            if self.server_thread.is_alive():
                print("Server thread did not terminate within timeout.")
            else:
                print("Server thread terminated successfully.")
            


    def plotting(self):
        fig= curve.display()
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(column=2, row=0, rowspan=10, sticky="nsew", padx=10, pady=10)


 

if __name__ == "__main__":
    timer=TimeManager()
    server=SCPI_Server()
    curve = generator()
    curve.generate_fullset()
    display = GUI()
    
    #generate the data set (for voltage measurements)
    try:

        #print("Data generation complete.")
        display.GUI()
    except Exception as e:
        print(f"Error in main execution: {e}")  
    except KeyboardInterrupt:
        print("Main execution interrupted by user.")
        exit(0)


    