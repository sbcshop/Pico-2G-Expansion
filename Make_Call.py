"""

"""
import machine
import os
import utime


led_pin = 25  # Pico onboard Led
pwr_en = 22  # SIM868 Pwrkey connected on GP22
uart_port = 0
uart_baute = 9600

# Initialize UART0 
uart = machine.UART(uart_port, uart_baute)
print(os.uname())

# Initialize on board led as output
led_onboard = machine.Pin(led_pin, machine.Pin.OUT)


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
    pwr_key = machine.Pin(pwr_en, machine.Pin.OUT)
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
            print('SIM868 is online\r\n')
            break
        else:
            print('SIM868 is offline, please wait...\r\n')
            utime.sleep(5)
            continue


# calling function
def make_call(phone_num='10000', keep_time=10):
    send_cmd('AT+CHFA=1', 'OK')
    send_cmd("ATD"+phone_num+";", 'OK')
    utime.sleep(keep_time)
    send_cmd('AT+CHUP;', 'OK')



# main function call
blink_led()  # Test Led
check_start() # Initialize SIM Module 
network_check() # Network connectivity check
make_call("123456" , 15) # Replace "123456" with Mobile number and 15 with timeout to hang call in seconds
