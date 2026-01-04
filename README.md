# Lindys SCPI Server (lindyscpiserver)
MOCK server purposed to simulate measurement tool like osciloscope or Multimeter. It simulates measurement data and can be started from CLI. 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## SCPI Commands
At this moment it simulates Keysight SCPI general commands for DMM via LXI. test it with RAW Data on 127.0.0.1:5025

**Supported commands**
*IDN? - Identification of device
MEAS:VOLT? - Autorange Voltage measurement
MEAS:CURR? - Autorange Current measurement

## Simulated device
At this moment it simulates only Voltage measurement of 12 Volt AGM Lead battery by DMM. 
