import machine
import os
import utime
import Lcd1_14driver
import time
import binascii


pwr_enable = 22  # SIM868 Power key connected on GP22
uart_port = 0
uart_baud = 9600

# Initialize UART0 
uart = machine.UART(uart_port, uart_baud)
print(os.uname())

LCD = Lcd1_14driver.Lcd1_14()#driver of lcd display


def wait_resp_info(timeout=3000):
        prvmills = utime.ticks_ms()
        info = b""
        while (utime.ticks_ms()-prvmills) < timeout:
            if uart.any():
                info = b"".join([info, uart.read(1)])
        print(info.decode())
        return info


 
def Send_command(cmd, back, timeout=2000):  # Send AT command
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


   
def Send_command_wait_resp(cmd, back, timeout=2000): # Send AT command and return response information
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


def Check_and_start(): # Initialize SIM Module 
        while True:
            uart.write(bytearray(b'ATE1\r\n'))
            utime.sleep(2)
            uart.write(bytearray(b'AT\r\n'))
            rec_temp = wait_resp_info()
            if 'OK' in rec_temp.decode():
                print('Pico 2G is ready\r\n' + rec_temp.decode())
                LCD.fill(LCD.black) 
                LCD.text("Pico 2G is ready",40,40,LCD.white) 
                LCD.lcd_show()
                break
            else:
                power = machine.Pin(pwr_enable, machine.Pin.OUT)
                power.value(1)
                utime.sleep(2)
                power.value(0)
                print('Pico 2G is starting up, please wait...\r\n')
                LCD.fill(LCD.black) 
                LCD.text("Pico 2G is starting up",40,40,LCD.white)
                LCD.text("Please wait...",40,60,LCD.white) 
                LCD.lcd_show()
                utime.sleep(4)


def Network_checking():# Network connectivity check
        for i in range(1, 3):
            if Send_command("AT+CGREG?", "0,1") == 1:
                print('SIM868 is online\r\n')
                break
            else:
                print('SIM868 is offline, please wait...\r\n')
                utime.sleep(2)
                continue

def gps():
        Check_and_start()
        count = 0
        print('Start GPS...')
        Send_command('AT+CGNSPWR=1', 'OK')
        LCD.fill(LCD.black) 
        LCD.lcd_show()

        LCD.text("GPS POWER ON",40,40,LCD.white) 
        LCD.lcd_show()
        utime.sleep(2)
        for i in range(1, 10):
            uart.write(bytearray(b'AT+CGNSINF\r\n'))
            rec_buff = wait_resp_info()
            if ',,,,' in rec_buff.decode():
                print('GPS is not ready')
                LCD.fill(LCD.black) 
                LCD.lcd_show()
                LCD.text("GPS is not ready",40,60,LCD.white) 
                LCD.lcd_show()
                utime.sleep(5)
                #print(rec_buff.decode())
                if i >= 9:
                    print('GPS positioning failed, please check the GPS antenna!\r\n')
                    Send_command('AT+CGNSPWR=0', 'OK')
                    LCD.fill(LCD.black) 
                    LCD.lcd_show()

                    LCD.text("GPS positioning failed",40,40,LCD.white)
                    LCD.text("GPS POWER OFF",40,60,LCD.white) 
                    LCD.lcd_show()
                    utime.sleep(4)
                else:
                    utime.sleep(2)
                    continue
            else:
                if count <= 3:
                    count += 1
                    print('GPS info:')
                    print(rec_buff.decode())
                else:
                    Send_command('AT+CGNSPWR=0', 'OK')
                    LCD.fill(LCD.black) 
                    LCD.lcd_show()
                    LCD.text("GPS POWER OFF",40,60,LCD.white) 
                    LCD.lcd_show()
                    utime.sleep(4)
                    break



def call(mobile_number,time):
        Check_and_start() # Initialize SIM Module 
        Network_checking() # Network connectivity check
        
        Send_command('AT+CHFA=1', 'OK')
        Send_command("ATD"+mobile_number+";", 'OK')
        utime.sleep(time)
        Send_command('AT+CHUP;', 'OK')


def message(phone_num, sms_text):
    def Hex_str_to_str(hex_str):
        hex_data = hex_str.encode('utf-8')
        str_bin = binascii.unhexlify(hex_data)
        return str_bin.decode('utf-8')


    def Str_to_hex_str(string):
        str_bin = string.encode('utf-8')
        return binascii.hexlify(str_bin).decode('utf-8')


    # Send SMS function
    def send_sms(phone_num, sms_text):
        Send_command('AT+CMGF=1', 'OK')
        if Send_command('AT+CMGS=\"'+phone_num+'\"', '>'):
            uart.write(bytearray(sms_text))
            utime.sleep(0.5)
            uart.write(bytearray(Hex_str_to_str("1A")))

    Check_and_start() 
    Network_checking() 
    send_sms(phone_num, sms_text)



def bluetooth(): 
        Check_and_start() 
        Send_command('AT+BTPOWER=1', 'OK', 3000)
        LCD.fill(LCD.black) 
        LCD.lcd_show()
        LCD.text("BT power on",40,40,LCD.white) 
        LCD.lcd_show()
        
        Send_command('AT+BTHOST?', 'OK', 3000)
        Send_command('AT+BTSTATUS?', 'OK', 3000)
        Send_command('AT+BTSCAN=1,10', 'OK', 8000)
        LCD.fill(LCD.black) 
        LCD.lcd_show()
        LCD.text("Scan BT Devices",40,40,LCD.white) 
        LCD.lcd_show()
        
        utime.sleep(5)
        Send_command('AT+BTPOWER=0', 'OK')
        LCD.fill(LCD.black) 
        LCD.lcd_show()
        LCD.text("BT power off",40,40,LCD.white) 
        LCD.lcd_show()