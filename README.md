# Pico-2G-Expansion

<img src= "https://github.com/sbcshop/Pico-2G-Expansion/blob/main/img.png" />

Raspberry Pi Pico 2G Expansion is a QUAD-Band GSM/GPRS/GNSS Expansion designed dedicatedly for Raspberry Pi Pico with UART, USB 2.0 Interface, 850/900/1800/1900 MHz, Bluetooth 3.0 based on SIM868 module to perform easy and efficient communication. Pico 2G Expansion works on the embedded TCP/UDP Protocols with Multi-constellation GNSS receiver support.

Pico 2G Expansion also includes a 1.14-inch display with a resolution of 240 x 135 pixels, 65K RGB colors, and a sharp and vivid exhibiting effect, designed primarily for user engagement via SPI connection by incorporating a GPIO header. The 1.14-inch LCD includes the ST7789 Driver and SPI Interface, decreasing the amount of IO pins required.

## Code
* Now open the below examples code as per their function to test the pico 2G Expansion in Thonny Ide.
  * SIM868.py: This file contain the library of the module, you need to add this file to pico.
  * pico_2g_exp.py: This is the main file that you need to run.
  * Lcd1_14driver.py : This library is of lcd 1.14 inch
* To make a call, you need to uncomment this line Call = SIM868.call(Mobile_number,10) in pico_2g_exp.py file
* To make a message, you need to uncomment this line Message = SIM868.message(Mobile_number,Write_message) in pico_2g_exp.py file
* To turn on GPS, you need to uncomment this line Gps = SIM868.gps() in pico_2g_exp.py file
* To scan Bluetooth devices, you need to uncomment this line Bluetooth = SIM868.bluetooth() in pico_2g_exp.py file
* You need to enter your mobile number in the code pico_2g_exp.py to make call and send the message

For step by step tutorial visit: [Pico 2G Expansion Wiki](https://learn.sb-components.co.uk/Pico-2g-expansion)
