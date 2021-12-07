"""
"""
import machine
import os
import utime
import time
import Lcd1_14driver


led_pin = 25  # Pico onboard Led
pwr_enable = 22  # SIM868 Pwrkey connected on GP22
uart_port = 0
uart_baud = 9600

# Initialize UART0 
uart = machine.UART(uart_port, uart_baud)
print(os.uname())

# Initialize on board led as output
led_onboard = machine.Pin(led_pin, machine.Pin.OUT)

LCD = Lcd1_14driver.Lcd1_14()#driver of lcd display

def blink_led():
    led_onboard(1)
    utime.sleep(1)
    led_onboard(0)
    utime.sleep(1)
    led_onboard(1)
    utime.sleep(1)
    led_onboard(0)

def lcd_border():
        LCD.hline(10,10,220,LCD.white)
        LCD.hline(10,125,220,LCD.white)
        LCD.vline(10,10,115,LCD.white)
        LCD.vline(230,10,115,LCD.white)       
        LCD.lcd_show()
    
def infoDevice():
        LCD.fill(LCD.black) 
        LCD.lcd_show()
        lcd_border()
        
        LCD.text("SB-COMPONENTS",70,40,LCD.white)
        LCD.text("PICO 2G",70,60,LCD.white)
        LCD.text("EXPANSION",70,80,LCD.white)  
        LCD.lcd_show()
        time.sleep(2)
        LCD.fill(LCD.black)
        lcd_border()
        LCD.text("WAITING.....",70,40,LCD.white)
        LCD.lcd_show()
        x = 0
        for y in range(0,1):
             x += 4
             LCD.text("......",125+x,40,LCD.white)
             LCD.lcd_show()
             time.sleep(1)
# power on/off the module
def power_on_off():
    pwr_key = machine.Pin(pwr_enable, machine.Pin.OUT)
    pwr_key.value(1)
    utime.sleep(2)
    pwr_key.value(0)


def wait_resp_info(timeout=2000):
    prvmills = utime.ticks_ms()
    info = b""
    while (utime.ticks_ms()-prvmills) < timeout:
        if uart.any():
            info = b"".join([info, uart.read(1)])
    print(info.decode())
    return info


# Send AT command
def send_cmd(cmd, back, timeout=2000):
    rec_buff = b''
    uart.write((cmd+'\r\n').encode())
    prvmills = utime.ticks_ms()
    while (utime.ticks_ms()-prvmills) < timeout:
        if uart.any():
            rec_buff = b"".join([rec_buff, uart.read(1)])
    if rec_buff != '':
        if back not in rec_buff.decode():
            print(cmd + ' back:\t' + rec_buff.decode())
            return 0
        else:
            print(rec_buff.decode())
            return 1
    else:
        print(cmd + ' no responce')


# Send AT command and return response information
def send_cmd_wait_resp(cmd, back, timeout=2000):
    rec_buff = b''
    uart.write((cmd + '\r\n').encode())
    prvmills = utime.ticks_ms()
    while (utime.ticks_ms() - prvmills) < timeout:
        if uart.any():
            rec_buff = b"".join([rec_buff, uart.read(1)])
    if rec_buff != '':
        if back not in rec_buff.decode():
            print(cmd + ' back:\t' + rec_buff.decode())
        else:
            print(rec_buff.decode())
    else:
        print(cmd + ' no responce')
    # print("Response information is: ", rec_buff)
    return rec_buff


# Module startup detection
def check_start():
    while True:
        # simcom module uart may be fool,so it is better to send much times when it starts.
        uart.write(bytearray(b'ATE1\r\n'))
        utime.sleep(2)
        uart.write(bytearray(b'AT\r\n'))
        rec_temp = wait_resp_info()
        if 'OK' in rec_temp.decode():
            print('Pico 2G is ready\r\n' + rec_temp.decode())
            LCD.fill(LCD.black) 
            LCD.lcd_show()
            lcd_border()

            LCD.text("Pico 2G is ready",40,40,LCD.white) 
            LCD.lcd_show()
            break
        else:
            power_on_off()
            print('Pico 2G is starting up, please wait...\r\n')
            LCD.fill(LCD.black) 
            LCD.lcd_show()
            lcd_border()

            LCD.text("Pico 2G is starting up",40,40,LCD.white)
            LCD.text("Please wait...",40,60,LCD.white) 
            LCD.lcd_show()
            utime.sleep(8)


# Check the network status
def network_check():
    for i in range(1, 3):
        if send_cmd("AT+CGREG?", "0,1") == 1:
            print('SIM868 is online\r\n')
            break
        else:
            print('SIM868 is offline, please wait...\r\n')
            utime.sleep(5)
            continue


# Scan Bluetooth devices
def bt_scan():
    send_cmd('AT+BTPOWER=1', 'OK', 3000)
    LCD.fill(LCD.black) 
    LCD.lcd_show()
    lcd_border()
    LCD.text("BT power on",40,40,LCD.white) 
    LCD.lcd_show()
    
    send_cmd('AT+BTHOST?', 'OK', 3000)
    send_cmd('AT+BTSTATUS?', 'OK', 3000)
    send_cmd('AT+BTSCAN=1,10', 'OK', 8000)
    LCD.fill(LCD.black) 
    LCD.lcd_show()
    lcd_border()
    LCD.text("Scan BT Devices",40,40,LCD.white) 
    LCD.lcd_show()
    
    utime.sleep(4)
    send_cmd('AT+BTPOWER=0', 'OK')
    LCD.fill(LCD.black) 
    LCD.lcd_show()
    lcd_border()
    LCD.text("BT power off",40,40,LCD.white) 
    LCD.lcd_show()



# main function call
infoDevice()
blink_led()  # Test Led
check_start() # Initialize SIM Module 
bt_scan() # Scan for nearby discoverable bluetooth devices

