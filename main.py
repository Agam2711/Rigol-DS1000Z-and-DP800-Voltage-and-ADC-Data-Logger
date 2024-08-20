import serial
import pyvisa as visa
import pandas as pd
from datetime import datetime
from time import sleep
from instruments import DS1000Z, DP800
import os

serial_port = 'COM3'
baud_rate = 115200

ser = serial.Serial(serial_port, baud_rate)

time_interval = 3  # unit is seconds    
minimum_voltage = 0.2  # unit is volts
maximum_voltage = 1.0  # unit is volts
step_size = 0.001  # unit is volts
instrument = DS1000Z("192.168.0.100")
power = DP800("192.168.0.151")

#The address for DM multimeter
instrument_address = 'USB0::0x1AB1::0x09C4::DM3R204402544::INSTR'


# Initializing the instrument
def DSinit():
    # Defining the specs for channels
    instrument.show_channel(1)
    instrument.set_probe_ratio(1, 1)
    instrument.set_channel_scale(5, 1)

    instrument.show_channel(2)
    instrument.set_probe_ratio(1, 2)
    instrument.set_channel_scale(10, 2)

    instrument.show_channel(3)
    instrument.set_probe_ratio(1, 3)
    instrument.set_channel_scale(5, 3)

    instrument.show_channel(4)
    instrument.set_probe_ratio(1, 4)
    instrument.set_channel_scale(10, 4)

def get_unique_filename(base_name='voltage_readings', extension='.csv'):
    i = 1
    while os.path.exists(f"{base_name}_{i}{extension}"):
        i += 1
    return f"{base_name}_{i}{extension}"

def read_voltage_from_channels():
    global minimum_voltage, maximum_voltage
    
    df = pd.DataFrame(columns=['Timestamp', 'Va', 'Vb', 'Vc', 'Vd', 'DAC Output', 'Calculated Current'])
    
    # Get a unique filename
    filename = get_unique_filename()

    voltage_check = minimum_voltage
    increasing = True
    power.set_channel( voltage = minimum_voltage, current=1, channel=1)

    while True:
        # Read voltage from channel 1
        voltage_ch1 = instrument.get_measurement("VAVG", "CURR", 1)
        # Read voltage from channel 2
        voltage_ch2 = instrument.get_measurement("VAVG", "CURR", 2)
        # Read voltage from channel 3
        voltage_ch3 = instrument.get_measurement("VAVG", "CURR", 3)
        # Read voltage from channel 4
        voltage_ch4 = instrument.get_measurement("VAVG", "CURR", 4)

        #power.set_channel(voltage=voltage, current=1, channel=1)

        power.set_channel( voltage = voltage_check , current=1, channel=1)
        rm = visa.ResourceManager()
        
        
        #Comment out to disable DM3058E Multimeter
        dmm = rm.open_resource(instrument_address)
        dmm_current = (dmm.query("MEAS:CURR:DC?")) 
        # Converting the dmm current into the correct format
        dmm_current = dmm_current.strip().strip('"')
        dmm_current = dmm_current.split('+',1)[-1]

        #ADC values from nrf board
        line = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
        adc_values = line.split('|') 
        adc_0 = float(adc_values[0].split(':')[1].strip())
        adc_1 = float(adc_values[1].split(':')[1].strip())
        adc_2 = float(adc_values[2].split(':')[1].strip())
        adc_3 = float(adc_values[3].split(':')[1].strip())

      
        
        calculated_Ib = (voltage_ch3 / 100) * 1000   # Shunt resistance is 100 ohms
        #Finding Current by doing voltage/resistance and then converting it into milliamps

        # Print the voltage readings
        print(f"Voltage reading from Channel 1: {voltage_ch1} V")
        print(f"Voltage reading from Channel 2: {voltage_ch2} V")
        print(f"Voltage reading from Channel 3: {voltage_ch3} V")
        print(f"Voltage reading from Channel 4: {voltage_ch4} V")

        print(f"DAC Output: {minimum_voltage} V")

        print(f"Calculated Current: {calculated_Ib} mAmp")
        print(f"DM Current: {dmm_current} mAmp")
        print(f"ADC Values: ADC_0: {adc_0}, ADC_1: {adc_1}, ADC_2: {adc_2}, ADC_3: {adc_3}")
        
        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Append the readings to the DataFrame
        new_row = pd.DataFrame({
            'Timestamp': [timestamp],
            'Va': [voltage_ch1],
            'Vb': [voltage_ch2],
            'Vc': [voltage_ch3],
            'Vd': [voltage_ch4],
            "DAC Output": [minimum_voltage],
            "Calculated Current": [calculated_Ib],
            "DM Current": [dmm_current],
            "External_ADC_0": [adc_0],
            "External_ADC_1": [adc_1],
            "External_ADC_2": [adc_2],
            "External_ADC_3": [adc_3]
        })
        
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Write the DataFrame to a CSV file
        if not os.path.exists(filename):
            df.to_csv(filename, index=False)
        else:
            new_row.to_csv(filename, mode='a', header=False, index=False)
        
        sleep(time_interval)
        if increasing:
            voltage_check += step_size
            if voltage_check >= maximum_voltage:
                increasing = False
        else:
            voltag_check -= step_size
            if voltage_check <= minimum_voltage:
                break
    

if __name__ == "__main__":
    DSinit()
    read_voltage_from_channels()
    