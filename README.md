# Data Logger for Voltage and ADC Measurements

## Overview

This project is a data logger designed to capture and record voltage measurements from a Rigol DS1000Z oscilloscope and DP800 power supply, as well as DAC and external ADC values from an NRF board. The recorded data includes various voltage channels, DAC output, calculated current, and ADC readings.

## Features

- **Rigol DS1000Z Oscilloscope**: Capture voltage values from up to four channels.
- **Rigol DP800 Power Supply**: Read DAC output values.
- **NRF Board**: Measure external ADC values.
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

To set up the project, you'll need Python and the necessary libraries. Follow these steps:

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Download and Install NI-VISA for Windows for DM current**

    NI-VISA is needed for the DM current and is free for Windows ONLY.
    NI-VISA is required to interface with the DM3058E multimeter.
    Download NI-VISA from the [NI website](https://www.ni.com/en/support/downloads/drivers/download.ni-visa.html?srsltid=AfmBOooXD4fyJhTH6-xv9QaH9YscXMzQhNZJmX1KQ85K_iZKBZEXBv1I#544206).

## Usage

1. Connect your Rigol DS1000Z oscilloscope, Rigol DP800 power supply, and nrf board as required.
2. Run the data logger script:
    ```bash
    python main.py
    ```

3. For using different functions, You can look into instuments.py and test.py for DP800 and DS1000Z.

4. The script will log the data into a file. You can specify the file path and name in the script configuration.

5. The external ADC values are recorded using a ADS1115 chip connected to a nrf52833 board.

6. To disable any instrument, comment out the lines which are written for the instrument.

## Credits
https://github.com/nathankjer/instruments









