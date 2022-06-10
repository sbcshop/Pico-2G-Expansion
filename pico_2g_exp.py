import machine
import os
import utime
import time
import Lcd1_14driver
import SIM868

LCD = Lcd1_14driver.Lcd1_14()#driver of lcd display

APN = "airtelgprs.com" # write your APN address

###############GET your channel details from thingspeak ####
get_server = "https://api.thingspeak.com/channels/1739661/status.json?api_key=01ANTAK4QMK9A7MQ"
####################################################

#################### POST data to thingspeak ###
post_data = 'api_key=2HWL5NUT0FEA8I57&field1=26.44' #  write your API keys
content_type = 'application/x-www-form-urlencoded' 
post_server = "http://api.thingspeak.com/update"
################################################

##################################TCP########
tcp_ip = "write tcp server ip or address" # or for thingspeak ip is 184.106.153.149
port = "80" # write the port
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

#data = "Hello World!!"or send data to thing speak - "GET https://api.thingspeak.com/update?api_key=01ANTAK4QMK9A7MQ&field1=0"
#Tcp = EG25_4G.tcp(tcp_ip,port,APN,data) # data send to server

#Get = SIM868.get_http(get_server,APN)
#Post = EG25_4G.post_http(post_data,APN,content_type,post_server)
