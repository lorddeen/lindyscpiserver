# Lindy SCPI Server - Mock Instrument simulator

This project is a measurement instrument simulator (e.g., digital multimeters) communicating via the **SCPI** (Standard Commands for Programmable Instruments) protocol. It allows for testing data acquisition software without the need for physical hardware connectivity.

The simulator generates real-time voltage data corresponding to the **discharge curve of a 12V AGM battery** and responds to queries over a TCP/IP socket.

## 🚀 Key Features

* **SCPI Server**: Communication via TCP/IP (default port 5025).
* **Dynamic Data**: Instead of static values, it simulates a realistic battery voltage drop over time using a mathematical model.
* **GUI Interface**: A Tkinter window to monitor server status and configure connection settings.
* **Parser Selection**: Supports different response formats based on the selected device driver.

## 🛠️ Parser Architecture

The application allows switching between two types of parsers (drivers) directly in the configuration:

1.  **Keysight Parser (`keysight`)**: Emulates the specific behavior of a Keysight 34461A multimeter, including its precise Identification String (IDN).
2.  **Generic Parser (`generic`)**: A basic implementation for general-purpose measurement devices.

The parser selection is managed in the `config.json` file using the `"DRIVER"` key.

## 📁 Project Structure

* `__main__.py`: The main entry point, managing threads for the GUI and the network server.
* `drivers.py`: Contains the `KeysightGenericCommands` and `GenericCommands` classes for processing SCPI commands.
* `batt_dis_gen.py`: Logic for the discharge curve generator (`AGM12VGeneric`) based on exponential decay.
* `config.json`: Configuration for host, port, and active driver.

## 🔌 Supported SCPI Commands

The server responds to the following standardized commands:

| Command | Description | Example Response |
| :--- | :--- | :--- |
| `*IDN?` | Identification Query | `LINDY TECHNOLOGIES,34461A,...` |
| `MEAS:VOLT?` | Measure current voltage | `1.28543E+01` (Scientific notation) |
| `MEAS:CURR?` | Measure current | "NICE TRY, NO CURRENT MEASUREMENT" |

## 📊 Battery Discharge Model

Discharge is simulated using an exponential function that calculates voltage based on the elapsed time since the server started:

$$V(t) = V_{charged} - V_{discharge} \cdot e^{k \cdot (t - t_{offset})}$$
*(Where $k$ is the discharge exponent and $t$ is the time since start)*

## ⚙️ Installation and Setup

1.  **Install dependencies:**
    ```bash
    pip install numpy matplotlib
    ```

2.  **Configuration:**
    Edit `config/config.json` to set your desired parser (`keysight` or `generic`).

3.  **Run the application:**
    ```bash
    python __main__.py
    ```
