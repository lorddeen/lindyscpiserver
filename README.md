# SCPI Multimeter Simulator

This project is a digital multimeter simulator that communicates via standardized SCPI commands over a TCP/IP network. It generates a realistic discharge curve for a 12V AGM battery and allows users to "measure" this voltage through network queries, simulating a Keysight-style instrument.

## Key Features

Battery Discharge Simulation: Generates a voltage curve based on an exponential decay model for a standard 12V AGM battery.SCPI Server: Listens on port 5025 (the standard SCPI port) and processes incoming text commands via TCP.Data Visualization: Automatically plots the generated discharge curve using matplotlib upon startup.Sequential Measurement: Each voltage query (MEAS:VOLT?) returns the next data point in the pre-generated time series.

# Installation & Requirements

The project requires Python 3 and several libraries for mathematical calculations and plotting.Clone the repository:Bashgit clone https://github.com/your-username/multimeter-simulator.git
cd multimeter-simulator

* Install dependencies:Bashpip install numpy matplotlib

# Usage

Start the Server:Run the main script to initialize the data and start the listener:Bashpython __main__.py
The program will first display a graph of the discharge curve.Once the graph window is closed, the SCPI server starts listening on 127.0.0.1:5025.Connecting to the Simulator:You can connect using any TCP client (e.g., Telnet, Putty, or a custom Python script).Example Interaction:PlaintextSent: *IDN?
Response: LINDY TECHNOLOGIES,AABBCC,!!ONLY VOLTAGE MEASUREMENTS NOW!!

Sent: MEAS:VOLT?
Response: 12.854... (current voltage value)

## Supported SCPI Commands
CommandDescription *IDN? Returns the device identification string.MEAS:VOLT?Returns the current simulated voltage measurement.MEAS:CURR?Returns an error message (current measurement not supported).MEAS:RES?Returns an error message (resistance measurement not supported).

## Project Structure
* __main__.py: The entry point that manages the TCP socket and coordinates between the generator and the SCPI parser.

* generators/batt_dis_gen.py: Contains the AGM12VGeneric class for calculating the battery model using numpy

* drivers/keysight_commands_module.py: Implements the KeysightGenericCommands class to parse SCPI strings and return appropriate responses.

## imulation Configuration
You can modify the simulation behavior in batt_dis_gen.py by adjusting these parameters:
* chargedbattvolt: The starting voltage of the battery (default 13V)
* timeoffset: The total duration of the simulation in seconds (default 3600s)
* exponent: The rate of voltage decay.

## License
This project is licensed under the MIT License: