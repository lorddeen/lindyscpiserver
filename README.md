# 🔋 Lindy SCPI Server - Mock Instrument Simulator

This project is a measurement instrument simulator (e.g., digital multimeters) communicating via the **SCPI** (Standard Commands for Programmable Instruments) protocol. It allows for testing data acquisition software without the need for physical hardware connectivity.

The simulator generates real-time data corresponding to the **discharge curve of a 12V AGM battery** and responds to queries over a TCP/IP socket.

## 🚀 Key Features

* **SCPI Server**: Communication via TCP/IP (default port 5025) running in a separate background thread.
* **Dynamic Data**: Simulates a realistic battery voltage drop over time using a mathematical model.
* **Integrated GUI**: A Tkinter window with an embedded Matplotlib graph for real-time visualization of the discharge curve.
* **Flexible Architecture**: Support for different command parsers (Keysight, Generic) defined in the configuration.

## 🛠️ Driver Architecture

The application allows switching between different command parsers directly in the `config.json` file:

1.  **Keysight (`keysight`)**: Emulates the specific behavior of a Keysight 34461A multimeter.
2.  **Generic (`generic`)**: A basic implementation for general-purpose measurement devices.

## 📁 Project Structure

* `__main__.py`: The main entry point, managing threads, the GUI (Tkinter), and the `TimeManager`.
* `drivers/drivers.py`: Contains the `KeysightGenericCommands` and `GenericCommands` classes for processing SCPI commands.
* `generators/generators.py`: Logic for the discharge curve generator `AGM12VGeneric`.
* `config/config.json`: Configuration for the host, port, and active driver.

## 🔌 Supported SCPI Commands

The server responds to the following standardized commands:

| Command | Description | Example Response |
| :--- | :--- | :--- |
| `*IDN?` | Identification Query | `LINDY TECHNOLOGIES,34461A,...` |
| `MEAS:VOLT?` | Measure current voltage | `1.28543E+01` |
| `MEAS:CURR?` | Attempt current measurement | `NICE TRY, NO CURRENT MEASUREMENT` |
| `MEAS:RES?` | Attempt resistance measurement | `NICE TRY, NO RESISTANCE MEASUREMENT` |

## 📊 Battery Discharge Model

Discharge is simulated using an exponential function based on the time elapsed since the server started:

$$V(t) = V_{charged} - V_{discharge} \cdot e^{exponent \cdot (t - t_{offset})}$$

## ⚙️ Installation and Setup

1.  **Install dependencies:**
    ```bash
    pip install numpy matplotlib
    ```

2.  **Configuration:**
    Edit `config/config.json` to set your desired server parameters.

3.  **Run the application:**
    ```bash
    python __main__.py
    ```