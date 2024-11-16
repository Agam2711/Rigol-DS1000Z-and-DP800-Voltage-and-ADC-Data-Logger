# Rigol DS1000Z and DP800 Voltage and ADC Data Logger

## Overview

This project is a data logger designed to capture and record voltage measurements using a **Rigol DS1000Z oscilloscope** and **Rigol DP800 power supply**, as well as DAC and external ADC values from an nRF board. The recorded data includes various voltage channels, DAC output, calculated current, and ADC readings. All recorded data is saved in a CSV file with a unique filename generated each time the script is run.

## Features

- **Rigol DS1000Z Oscilloscope**: Capture voltage values from up to four channels.
- **Rigol DP800 Power Supply**: Read DAC output values.
- **NRF Board**: Measure external ADC values.
- **Dynamic CSV Output**: Logs all data into a CSV file, generating unique filenames such as `voltage_readings_1.csv`, `voltage_readings_2.csv`, and so on.
- **Timestamp**: Log the time of each measurement.

## Data Collected

The data logger records the following values:

- `'Timestamp'`: The time when the data was recorded.
- `'Va'`: Voltage from channel 1.
- `'Vb'`: Voltage from channel 2.
- `'Vc'`: Voltage from channel 3.
- `'Vd'`: Voltage from channel 4.
- `"DAC Output"`: Output voltage from the DAC.
- `"Calculated Current"`: Current calculated based on measurements.
- `"DM Current"`: Current measured by a digital multimeter.
- `"External_ADC_0"`: Value from external ADC channel 0.
- `"External_ADC_1"`: Value from external ADC channel 1.
- `"External_ADC_2"`: Value from external ADC channel 2.
- `"External_ADC_3"`: Value from external ADC channel 3.

## Installation

To set up the project, you'll need Python and the necessary libraries. It is recommended to use a Python virtual environment to avoid dependency conflicts. Follow these steps:

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create and activate a Python virtual environment:
    ```bash
    # On Windows
    python -m venv venv
    venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

4. **Download and Install NI-VISA for Windows for DM Current**

    NI-VISA is required for interfacing with the DM3058E digital multimeter to measure current. It is free and available for **Windows only**.  
    Download NI-VISA from the [NI website](https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html?srsltid=AfmBOooXD4fyJhTH6-xv9QaH9YscXMzQhNZJmX1KQ85K_iZKBZEXBv1I#544206).  

    - **For macOS/Linux Users**: NI-VISA is not available. To proceed without the DM3058E current measurements, comment out the following lines in `main.py`:  
      - Line **22**  
      - Lines **78–83**  
      - Line **107**  
      - Line **122**

## Usage

1. Connect your Rigol DS1000Z oscilloscope, Rigol DP800 power supply, and nRF board as required.
2. Run the data logger script:
    ```bash
    python main.py
    ```

3. Explore additional functionality in `instruments.py` and `test.py` for the DP800 and DS1000Z devices.

4. Each run of the script generates a uniquely named CSV file to avoid overwriting previous data. The filenames follow the format `voltage_readings_X.csv`, where `X` is incremented automatically (e.g., `voltage_readings_1.csv`, `voltage_readings_2.csv`, etc.).

5. The external ADC values are recorded using an ADS1115 chip connected to an nRF52833 board.

6. To disable any instrument, comment out its corresponding lines in `main.py`.

### **Note for Users Without a Microcontroller**

If you do not have a microcontroller and only want to log data from the Rigol oscilloscope and power supply, comment out the ADC-related lines in `main.py`. Specifically, comment out the following lines:  
- Lines **86–91**  
- Line **108**  
- Lines **123–126**  

## Output

The logged data is saved in uniquely named CSV files (`voltage_readings_X.csv`), with each row containing a timestamp and all measured values for that time.

## Credits

This project builds on tools provided by [NathanKjer's Instruments](https://github.com/nathankjer/instruments).