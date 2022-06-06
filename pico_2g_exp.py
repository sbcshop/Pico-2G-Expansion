import machine
import os
import utime
import time
import Lcd1_14driver
import SIM868

LCD = Lcd1_14driver.Lcd1_14()#driver of lcd display

##################################TCP########
tcp_ip = "write tcp server ip or address"
port = "80" # write the port
APN = "airtelgprs.com" # write your APN address
############################################

def infoDevice():
        LCD.fill(LCD.black) 
        LCD.hline(10,10,220,LCD.white)
        LCD.hline(10,125,220,LCD.white)
        LCD.vline(10,10,115,LCD.white)
        LCD.vline(230,10,115,LCD.white)       
        
        LCD.text("SB-COMPONENTS",70,40,LCD.white)
        LCD.text("PICO 2G",70,60,LCD.white)
        LCD.text("EXPANSION",70,80,LCD.white)  
        LCD.lcd_show()
        time.sleep(2)
        LCD.fill(LCD.black)
        LCD.text("WAITING.....",70,40,LCD.white)
        LCD.lcd_show()
        x = 0
        for y in range(0,1):
                x += 4
                LCD.text(".",125+x,40,LCD.white)
                LCD.lcd_show()
                time.sleep(1)

infoDevice()

Mobile_number = "write_your_phone_number_here" #write your phone number here 
Write_message = "Hello World" #write message you need to send

Message = SIM868.message(Mobile_number,Write_message) #send the message

# Call = SIM868.call(Mobile_number,10) # uncomment this to make call

#Gps = SIM868.gps() #uncomment this to use gps

#Bluetooth = SIM868.bluetooth() #uncomment this to use bluetooth # Scan Bluetooth devices

#data = "Hello World!!"
#Tcp = EG25_4G.tcp(tcp_ip,port,APN,data) # data send to server
