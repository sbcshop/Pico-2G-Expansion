"""
"""
import machine
import os
import utime
import binascii


led_pin = 25  # Pico onboard Led
pwr_enable = 22  # SIM868 Pwrkey connected on GP22
uart_port = 0
uart_baud = 9600

# Initialize UART0 
uart = machine.UART(uart_port, uart_baud)
print(os.uname())

# Initialize on board led as output
led_onboard = machine.Pin(led_pin, machine.Pin.OUT)

def hexstr_to_str(hex_str):
    hex_data = hex_str.encode('utf-8')
    str_bin = binascii.unhexlify(hex_data)
    return str_bin.decode('utf-8')


def str_to_hexstr(string):
    str_bin = string.encode('utf-8')
    return binascii.hexlify(str_bin).decode('utf-8')


def blink_led():
    led_onboard(1)
    utime.sleep(1)
    led_onboard(0)
    utime.sleep(1)
    led_onboard(1)
    utime.sleep(1)
    led_onboard(0)


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
            break
        else:
            power_on_off()
            print('Pico 2G is starting up, please wait...\r\n')
            utime.sleep(8)


# Check the network status
def network_check():
    for i in range(1, 3):
        if send_cmd("AT+CGREG?", "0,1") == 1:
            print('Pico 2G is online\r\n')
            break
        else:
            print('Pico 2G is offline, please wait...\r\n')
            utime.sleep(5)
            continue


# Send SMS function
def send_sms(phone_num='12345', sms_text=""):
    send_cmd('AT+CMGF=1', 'OK')
    if send_cmd('AT+CMGS=\"'+phone_num+'\"', '>'):
        uart.write(bytearray(sms_text))
        utime.sleep(0.5)
        uart.write(bytearray(hexstr_to_str("1A")))



# main function call
blink_led()  # Test Led
check_start() # Initialize SIM Module 
network_check() # Network connectivity check

# SMS test
sms_text ="Hello from Pico 2G."
send_sms("123456", sms_text)
