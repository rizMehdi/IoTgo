"""

"""

##import board
##import busio
##import binascii
##from digitalio import DigitalInOut
##from adafruit_pn532.spi import PN532_SPI
####from sense_hat import SenseHat
##from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
##from flask import Flask
##import random, threading, webbrowser
import csv
import os
import re
import sys
import urllib.parse
from time import sleep


num_eCards=0
num_iCards=0
num_oCards=0

# eCards_row=0
# iCards_row=0
# oCards_row=0 
# eCards_col=7 
# iCards_col=4 
# oCards_col=1  
# maxCards=16

#flask variables:
ip="127.0.0.1"#ip="192.168.1.4"
port="5000"
width_makecode="1000" 
height_makecode="800"

#urlGen variables:
codetitle=""##codetitle="%23%20"
codesubtitle=""


in_type2name= {
  	str(b'010'):"buttonNotPress",
 	str(b'011'):"buttonPress",
  	str(b'020'):"accelLow" , 
  	str(b'021'):"accelHigh"  , 
  	str(b'031'):"compassE"  , 
  	str(b'032'):"compassW"  , 
	str(b'033'):"compassN"  , 
	str(b'034'):"compassS"  , 
	str(b'041'):"gestureShake"  , 
	str(b'042'):"gestureTilt"  , 
	str(b'051'):"movementPresent"  , 
#	str(b'050'):"movementNotPresent"  , 
	str(b'060'):"noiseLow"  , 
	str(b'061'):"noiseHigh"  ,
	str(b'070'):"sliderLow"  , 
	str(b'071'):"sliderHigh"  , 
	str(b'080'):"tempLow"  , 
	str(b'081'):"tempHigh"  ,
	str(b'090'):"lightlevelLow",
	str(b'091'):"lightlevelHigh",
 	str(b'001'):"touchYes" ,#v2 #card not used 
 	str(b'000'):"touchNo"  , #v2 #card not used  
	str(b'111'):"forecastTempHigh",
	str(b'110'):"forecastTempLow",
	str(b'221'):"forecastHumidityHigh",
	str(b'220'):"forecastHumidityLow",
	str(b'331'):"forecastWindHigh",
	str(b'330'):"forecastWindLow",
	str(b'441'):"forecastprecipHigh",
	str(b'440'):"forecastprecipLow",
	str(b'551'):"todayStartOfMonth",
	str(b'552'):"todayWeekday",
	str(b'553'):"todayWeekend",
	str(b'554'):"todaySummerMonth",
	str(b'555'):"todayNewYear",
	str(b'556'):"timeForSchool",
# 	str(b'557'):"timeSunrise",
# 	str(b'558'):"timeSunset",
    }
    
out_type2name= {
    str(b'011'):"iconHappy",
    str(b'012'):"iconSad",
#    str(b'010'):"iconNone",
  	str(b'021'):"lightOn",
 	str(b'022'):"lightOff",
  	str(b'031'):"musicHappy" , 
  	str(b'032'):"musicSad"  , 
#	str(b'030'):"musicNone"  , 
# 	str(b'041'):"speakText"  , not supported yet
# 	str(b'042'):"speakInput"  ,not supported yet
# 	str(b'040'):"speakNone"  , not supported yet
	str(b'051'):"displayText"  , 
	str(b'052'):"displayInput"  , 
#	str(b'050'):"displayNone"  , 
	str(b'061'):"showStripRainbow"  , 
	str(b'060'):"showStripBlack", 
	str(b'071'):"fanOn"  , 
	str(b'070'):"fanOff"  ,
##	str(b'080'):"rotateMin"  , #card not used  
##	str(b'085'):"rotateMid"  , #card not used 
##	str(b'081'):"rotateMax"  , #card not used  
	str(b'111'):"tweetText"  , 
	str(b'112'):"tweetInput"  , 
	str(b'221'):"logInput"  ,  

    }
    



def genURL (input_name, output_name):
##    input_name=input("input_state: ")
##    output_name=input("output: ")
        #here i am collecting chunks of code, encoding them, and concatenating them into a URL:
    if output_name in on_start:
        on_start_code = on_start[output_name]+ '\n'
    elif input_name in on_start:
        on_start_code = on_start[input_name]+ '\n'
    else:
        on_start_code=""
        
    if output_name in output_else_code:
        else_output_code = output_else_code[output_name]+ '\n'
    else:
        else_output_code="basic.pause(100)"
        
    if input_name in output_else_code:#special cases for forecast: get_temp
        else_output_code = output_else_code[input_name]+ '\n'
##    print("on_start_code:\n ", on_start_code)
##    print("input_code:\n ", input_code[input_name])
##    print("output_code:\n ", output_code[output_name])
##    print("else_output: ", else_output_code) #     print("else_output:\n ", output_else_code[output_name] )

        
    jscode= on_start_code  + 'basic.forever(function () {' + '\n' + '    ' + 'if (' + input_code[input_name]+'){\n'  + '    '*2 + output_code[output_name]+'\n'  + '    '*2 + 'basic.pause(100)' +'\n' +  '    ' + ' } else {\n'+'    '*2 + else_output_code +'\n' + '    '+'}\n})'  
    #jscode= on_start_code  + 'basic.forever(function () {' + '\n' + '    ' + 'if (' + input_code[input_name]+'){\n'  + '    '*2 + output_code[output_name]+'\n'  + '    '*2 + 'basic.pause(100)' +'\n' +  '    ' + ' } else {\n'+'    '*2 + else_output_code +'\n' + '    '*2 +'basic.pause(100)'+'\n'+'    '+'}\n})'
    print(jscode)
    url='https://makecode.microbit.org/--docs?md='+codetitle+codesubtitle+'%0A%0A%60%60%60%20blocks%0A'
    #url='https://makecode.microbit.org/--docs?md=%23%23%20'+codetitle+codesubtitle+'%0A%0A%60%60%60%20blocks%0A'
    for eachline in jscode:
        url=url+urllib.parse.quote(eachline) 
    url=url+'%0A%60%60%60%0A%0A'
    if output_name in package_suffix:
    	url=url+package_suffix[output_name]
    elif input_name in package_suffix:
        url=url+package_suffix[input_name]
   	# to confirm if TWO packages can be added at the same time.

    return url



##
##
### SPI connection:
##spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
##leftBot_gpio26 = DigitalInOut(board.D5)
##
##
##print('Discovering card-readers')
##print('card-reader: leftBot_gpio26')
##
###try:
##pn532_leftBot  = PN532_SPI(spi, leftBot_gpio26, debug=False)
##ic, ver, rev, support = pn532_leftBot.firmware_version
##
##print('Found pn532_leftBot with firmware version: {0}.{1}'.format(ver, rev))
##pn532_leftBot.SAM_configuration()
###except:
####    input_name=input("input_state: ")
####    output_name=input("output: ")
##
##
##
##
### Set 16 bytes of block to 0xFEEDBEEF
##data = bytearray(16)
##data[0:16] = list(b'\xCC\xCC\xCC\xCC\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
##key = b'\xFF\xFF\xFF\xFF\xFF\xFF'
##
##
##cardtype="x"
##input_name=""
##output_name=""
##
##
##prevUid=b'\xFF\xFF\xFF\xFF'
##    
### Main loop to detect cards and read a block.
##print('Waiting for MiFare card...')
##while True:
##    # Check if a card is available to read.
##    uid_left = pn532_leftBot.read_passive_target(timeout=0.5)
##    # Try again if no card is available.
##    if uid_left is None:
##        continue
##    if uid_left == prevUid:
##        continue
##    print('New card detected with UID: 0x{0}'.format(binascii.hexlify(uid_left)))
##    prevUid = uid_left;
##    # Authenticate block 4 for reading with default key (0xFFFFFFFFFFFF).
##    if not pn532_leftBot.mifare_classic_authenticate_block(uid_left, 4, MIFARE_CMD_AUTH_B,
##                                                   [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
##        print('Failed to authenticate block 4!')
##        continue
##    # Read block 4 data.
##    data = pn532_leftBot.mifare_classic_read_block(4)
##    if data is None:
##        print('Failed to read block 4!')
##        continue
##    # Note that 16 bytes are returned, so only show the first 4 bytes for the block.
##    print('Read block 4: 0x{0}'.format(binascii.hexlify(data[:4])))
##    if data[:2]==b'\xC3\x3C':
##        num_eCards+=1
##        print("detected card type: eCard, subtype: 0x{0}".format(binascii.hexlify(data[2:3])))
##        cardtype="e"
##    elif (data[:2]==b'\xC1\x1C'):
##        num_iCards+=1
##        print("detected card type: iCard, card subtype: 0x{0}".format(binascii.hexlify(data[2:3])))
##        cardtype="i"
##        input_type=binascii.hexlify(data[2:3])
##    elif (data[:2]==b'\xC0\x0C'):
##        num_oCards+=1
##        print("detected card type: oCard, card subtype: 0x{0}".format(binascii.hexlify(data[2:3])))
##        cardtype="o"
##        output_type=binascii.hexlify(data[2:3])
##    else:
##        print("unregistered card detected= 0x{0}".format(binascii.hexlify(data[:4])))
##        cardtype="x"
##    print(num_iCards)
##    print(num_oCards)
##    if num_iCards==1 and num_oCards==1:
##        print("one in one out found")
##        break
##
####print(output_type)
####print(input_type)



##output_name=out_type2name[str(input_type)]
##input_name=in_type2name[str(output_type)]
input_name=input("input_state: ")
output_name=input("output: ")
print(output_name)
print(input_name)



 


#defining a dictionary for any additional extension/package needed for each output:
package_suffix = {
	"rotateMin":"%60%60%%0Aservo%0A%60%60%60", 
	"rotateMid":"%60%60%%0Aservo%0A%60%60%60", 
	"rotateMax":"%60%60%%0Aservo%0A%60%60%60", 
	"showStripRainbow": "%60%60%60package%0Aneopixel%3Dgithub%3Amicrosoft%2Fpxt-neopixel%0A%0A%60%60%60", 
	"showStripBlack": "%60%60%60package%0Aneopixel%3Dgithub%3Amicrosoft%2Fpxt-neopixel%0A%0A%60%60%60", 
} #only where needed


#defining a dictionary for startup-code for each output:
on_start = {
  	"fanOn":   "basic.pause(1000)",
  	"lightOn": "basic.pause(1000)", 
  	"fanOff":   "basic.pause(1000)",
  	"lightOff": "basic.pause(1000)", 
  	"iconHappy":  "basic.pause(1000)", 
  	"iconSad":  "basic.pause(1000)", 
  	"iconNone":  "basic.pause(1000)", 
	"musicHappy": "music.setVolume(127)", 
	"musicSad":  "music.setVolume(127)",  
	"musicNone":  "music.setVolume(127)",   	
# 	"speakText": "",
# 	"speakInput": "",
# 	"speakNone": "",
  	"showStripRainbow": "let strip = neopixel.create(DigitalPin.P1,7,NeoPixelMode.RGB)", 
  	"showStripBlack": "let strip = neopixel.create(DigitalPin.P1,7,NeoPixelMode.RGB)", 
	"rotateMin":"servos.P1.setRange(0,180)", 
	"rotateMid":"servos.P1.setRange(0,180)", 
	"rotateMax":"servos.P1.setRange(0,180)", 
	"tweetText" : "radio.setGroup(313)\nradio.setTransmitSerialNumber(true)\nradio.sendValue(\"b#\", 8903)", 
	"tweetInput": "radio.setGroup(313)\nradio.setTransmitSerialNumber(true)\nradio.sendValue(\"b#\", 8903)", 
	"logInput"  : "radio.setGroup(313)\nradio.setTransmitSerialNumber(true)\nradio.sendValue(\"log4\", 8791)",  
	"forecastTempHigh": "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"forecastTempLow": "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"forecastHumidityHigh": "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"forecastHumidityLow": "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"forecastWindHigh": "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"forecastWindLow": "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"forecastprecipHigh": "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"forecastprecipLow":"radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"todayStartOfMonth": "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"todayWeekday": "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"todayWeekend": "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"todaySummerMonth": "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"todayNewYear": "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"timeForSchool": "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
#	"timeSunrise":"radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
# 	"timeSunset": "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
# 	"compassN" :"input.calibrateCompass()" , 
# 	"compassE" :"input.calibrateCompass()" , 
#   "compassS" :"input.calibrateCompass()" , 
#   "compassW" :"input.calibrateCompass()" , 
}#only where needed 
 

input_code = {
  	"buttonNotPress":"!input.buttonIsPressed(Button.A)",
 	"buttonPress":"input.buttonIsPressed(Button.A)",
  	"accelLow":"input.acceleration(Dimension.X) < 511" , 
  	"accelHigh":"input.acceleration(Dimension.X) >= 511"  , 
	"compassN" :"input.compassHeading() < 45" , 
	"compassE" :"input.compassHeading() >= 45 && input.compassHeading() < 135" , 
  	"compassS" :"input.compassHeading() >= 135 && input.compassHeading() < 225" , 
  	"compassW" :"input.compassHeading() >= 225 && input.compassHeading() < 315" , 
	"gestureShake":"input.isGesture(Gesture.Shake)"  , 
	"gestureTilt"  :"input.isGesture(Gesture.TiltLeft) || input.isGesture(Gesture.TiltRight)", 
	"movementNotPresent":"pins.digitalReadPin(DigitalPin.P0) == 1"  ,
	"movementPresent" :"pins.digitalReadPin(DigitalPin.P0) >= 1000" , 
	"noiseLow"  :"input.soundLevel() < 128" , #v2
	"noiseHigh"	:"input.soundLevel() >= 128"  , #v2
 	"touchYes" 	:"input.logoIsPressed()" ,  #v2
 	"touchNo"	:"!input.logoIsPressed()"  , #v2
	"sliderLow":"pins.analogReadPin(AnalogPin.P0) <= 100"  , 
 	"sliderMid":"pins.analogReadPin(AnalogPin.P0) > 500 && pins.analogReadPin(AnalogPin.P0) <= 700",
	"sliderHigh":"pins.analogReadPin(AnalogPin.P0) >= 1000"  , 
	"tempLow"  :"input.temperature() < 28", 
	"tempHigh" :"input.temperature() >= 28" ,
	"lightlevelLow" :"input.lightLevel() < 127", 
	"lightlevelHigh":"input.lightLevel() >= 127",
	"forecastTempHigh" 		:"forecastName == \"temp\" && forecastValue >= 28",
	"forecastTempLow" 		:"forecastName == \"temp\" && forecastValue < 28",
# 	"forecastCloudsHigh" 		:"forecastName == \"clouds\" && forecastValue >= 28 ",
# 	"forecastCloudsLow" 		:"forecastName == \"clouds\" && forecastValue < 28",
	"forecastHumidityHigh"	:"forecastName == \"humid\" && forecastValue >= 0.5",
	"forecastHumidityLow" 	:"forecastName == \"humid\" && forecastValue < 0.5",
	"forecastWindHigh" 		:"forecastName == \"wind\" && forecastValue >= 0.5",
	"forecastWindLow" 		:"forecastName == \"wind\" && forecastValue < 0.5",
	"forecastprecipHigh" 	:"forecastName == \"precip\" && forecastValue >= 0.5",
	"forecastprecipLow" 	:"forecastName == \"precip\" && forecastValue < 0.5",	
 	"todayStartOfMonth" 	:"forecastName == \"date\" && forecastValue == 1",
	"todayWeekday" 			:"forecastName == \"day\" && forecastValue <= 5",#1,2,3,4,5
	"todayWeekend" 			:"forecastName == \"day\" && forecastValue >= 6",#6,7
	"todaySummerMonth" 		:"forecastName == \"month\" && (forecastValue >= 6 && forecastValue <= 8)",#6,7,8
	"todayNewYear" 			:"forecastName == \"year\" && forecastValue == 2022",
	"timeForSchool" 		:"forecastName == \"time\" && forecastValue >= 0745",
# 	"timeSunrise" 			:"forecastName == \"sunrise\" && forecastValue == 28",
# 	"timeSunset" 			:"forecastName == \"sunset\" && forecastValue == 28",
} 




#only for tweeting, logging paired physical sensorValues:
input_sensorValue = {
  	"buttonNotPress":"input.buttonIsPressed(Button.A)",
 	"buttonPress":"input.buttonIsPressed(Button.A)",
  	"accelLow":"input.acceleration(Dimension.X)" , 
  	"accelHigh":"input.acceleration(Dimension.X)"  , 
	"compassN" :"input.compassHeading()" , 
	"compassE" :"input.compassHeading()" , 
  	"compassS" :"input.compassHeading()" , 
  	"compassW" :"input.compassHeading()" , 
	"gestureShake":"input.isGesture(Gesture.Shake)"  , 
	"gestureTilt"  :"input.isGesture(Gesture.TiltLeft) || input.isGesture(Gesture.TiltRight)", 
	"movementNotPresent":"pins.digitalReadPin(DigitalPin.P0)"  ,
	"movementPresent" :"pins.digitalReadPin(DigitalPin.P0)" , 
	"noiseLow"  :"input.soundLevel()" , #v2
	"noiseHigh"	:"input.soundLevel()"  , #v2
 	"touchYes" 	:"input.logoIsPressed()" ,  #v2
 	"touchNo"	:"input.logoIsPressed()"  , #v2
	"sliderLow":"pins.analogReadPin(AnalogPin.P0)"  , 
 	"sliderMid":"pins.analogReadPin(AnalogPin.P0)",
	"sliderHigh":"pins.analogReadPin(AnalogPin.P0)"  , 
	"tempLow"  :"input.temperature()", 
	"tempHigh" :"input.temperature()" ,
	"lightlevelLow" :"input.lightLevel()", 
	"lightlevelHigh":"input.lightLevel()",
	"forecastTempHigh" :"forecastValue",
	"forecastTempLow" :"forecastValue",
	"forecastHumidityHigh" :"forecastValue",
	"forecastHumidityLow" :"forecastValue",
	"forecastWindHigh" :"forecastValue",
	"forecastWindLow" :"forecastValue",
	"forecastprecipHigh" :"forecastValue",
	"forecastprecipLow" :"forecastValue",
	"todayStartOfMonth" :"forecastValue",
	"todayWeekday" :"forecastValue",
	"todayWeekend" :"forecastValue",
	"todaySummerMonth" :"forecastValue",
	"todayNewYear" :"forecastValue",
	"timeForSchool" :"forecastValue",
# 	"timeSunrise"  :"forecastValue",
# 	"timeSunset" :"forecastValue",
}


output_code = {
 	"iconHappy":"basic.showIcon(IconNames.Happy)",
    "iconSad":  "basic.showIcon(IconNames.Sad)",
    "iconNone":  "basic.clearScreen()",
  	"lightOn": "pins.digitalWritePin(DigitalPin.P1,1)",
 	"lightOff": "pins.digitalWritePin(DigitalPin.P1,0)",
  	"musicHappy" : "music.startMelody(music.builtInMelody(Melodies.Birthday), MelodyOptions.Forever)", 
  	"musicSad" : "music.startMelody(music.builtInMelody(Melodies.Funeral), MelodyOptions.Forever)", 
  	"musicNone" : "music.stopMelody(MelodyStopOptions.All)" , 
#   "speakText"  : "", 
#   "speakInput" : "" , 
#   "speakNone" : "" , 
	"displayText" : "basic.showString(\"Ciao from CHItaly21\")" , 
	"displayInput": "basic.showString(\""+input_name+"\")"  , 
 	"displayNone" :"basic.clearScreen()" , 
	"showStripRainbow" : "strip.showRainbow(1, 360)\nstrip.show()", 
	"showStripBlack" : "strip.showColor(neopixel.colors(NeoPixelColors.Black))", 
	"fanOn" :  	"pins.digitalWritePin(DigitalPin.P1,1)", 
	"fanOff"  : "pins.digitalWritePin(DigitalPin.P1,0)", 
 	"rotateMin" :"servos.P1.setAngle(0)" ,   #card not used 
 	"rotateMid" :"servos.P1.setAngle(90)" ,  #card not used 
 	"rotateMax" :"servos.P1.setAngle(180)" , #card not used    
	"tweetText"  : "radio.sendString(\"#CiaoFromCHItaly\")" , 
	"tweetInput" : "radio.sendString(\"#"+input_name+"\")" , #add input name and value directly???use variable
	"logInput"   : "radio.sendValue(\"&temp\","+input_sensorValue[input_name]+")",  #add input name and value directly???use variable
# 	"logInput"   : "radio.sendValue(\"&value\", 0)",  #add input name and value directly??? use variable
}# 
#confirm displayInput, tweetInput, logInput


#defining a dictionary for inverse code for each output: 
output_else_code={
 	"iconHappy":"basic.clearScreen()",
    "iconSad":  "basic.clearScreen()",
    "iconNone":  "basic.showIcon(IconNames.Happy)",
  	"lightOn": "pins.digitalWritePin(DigitalPin.P1,0)",
 	"lightOff": "pins.digitalWritePin(DigitalPin.P1,1)",
  	"musicHappy": "music.stopMelody(MelodyStopOptions.All)",  
  	"musicSad" 	: "music.stopMelody(MelodyStopOptions.All)", 
  	"musicNone" :  "music.startMelody(music.builtInMelody(Melodies.Birthday), MelodyOptions.Forever)", 
#   "speakText"  : "", 
#   "speakInput" : "" , 
#   "speakNone" : "" , 
	"displayText" : "basic.clearScreen()" , 
	"displayInput": "basic.clearScreen()"  , 
 	"displayNone" : "basic.showString(\"hello\")" , 
#  	"displayNone" : "basic.showString(\""+input_name+"\")" , 
	"showStripRainbow":  "strip.showColor(neopixel.colors(NeoPixelColors.Black))", 
	"showStripBlack" :"strip.showRainbow(1, 360)\nstrip.show()",  
	"fanOn" :  	"pins.digitalWritePin(DigitalPin.P1,0)", 
	"fanOff"  : "pins.digitalWritePin(DigitalPin.P1,1)", 
 	"rotateMin" :"servos.P1.setAngle(180)",#card not used 
 	"rotateMid" :"servos.P1.setAngle(0)" , #card not used 
 	"rotateMax" :"servos.P1.setAngle(0)" , #card not used    
	"tweetText"  : "basic.pause(100)" , #not needed for cloud cards, can else statement remains empty??
	"tweetInput" : "basic.pause(100)" , #not needed for cloud cards, can else statement remains empty??
	"logInput"   : "basic.pause(100)",  #not needed for cloud cards, can else statement remains empty??
	"forecastTempHigh" 		:"radio.sendString(\"get_temp\")\nbasic.pause(2000)",
	"forecastTempLow" 		:"radio.sendString(\"get_temp\")\nbasic.pause(2000)",
	"forecastHumidityHigh"	:"radio.sendString(\"get_humid\")\nbasic.pause(2000)",
	"forecastHumidityLow" 	:"radio.sendString(\"get_humid\")\nbasic.pause(2000)",
	"forecastWindHigh" 		:"radio.sendString(\"get_wind\")\nbasic.pause(2000)",
	"forecastWindLow" 		:"radio.sendString(\"get_wind\")\nbasic.pause(2000)",
	"forecastprecipHigh" 	:"radio.sendString(\"get_precip\")\nbasic.pause(2000)",
	"forecastprecipLow" 	:"radio.sendString(\"get_precip\")\nbasic.pause(2000)",
	"todayStartOfMonth" 	:"radio.sendString(\"get_date\")\nbasic.pause(2000)",
	"todayWeekday" 			:"radio.sendString(\"get_day\")\nbasic.pause(2000)",
	"todayWeekend" 			:"radio.sendString(\"get_day\")\nbasic.pause(2000)",
	"todaySummerMonth" 		:"radio.sendString(\"get_month\")\nbasic.pause(2000)",
	"todayNewYear" 			:"radio.sendString(\"get_year\")\nbasic.pause(2000)",
	"timeForSchool" 		:"radio.sendString(\"get_time\")\nbasic.pause(2000)",
}




codetitle="%23%20Input card = "+input_name+", Ouput card = "+output_name
urlis=genURL(input_name,output_name)    
print(urlis)

thing_name="none"
mission_name="none"
persona_name="none"
count=1
##for eachkey in in_type2name:
##    for otherkey in out_type2name:
##        #print(in_type2name[eachkey] +'_'+out_type2name[otherkey])
##        count=count+1
##print(count)

    
##import csv
##import time
##timestamp=time.time()
##
####output_name=out_type2name[str(input_type)]
####input_name=in_type2name[str(output_type)]
##
##
##for eachkey in in_type2name:
##    urlis=genURL(in_type2name[eachkey],'iconHappy') 
##    print(in_type2name[eachkey] +'_iconHappy')
##    with open('test_IO.csv', mode='w') as save_file:
##        csv_writer = csv.writer(save_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
##        csv_writer.writerow([timestamp, mission_name, persona_name, thing_name,input_name, output_name,urlis])
##
##for otherkey in out_type2name:
##    urlis=genURL('buttonPress',out_type2name[otherkey])
##    print('buttonPress_'+out_type2name[otherkey])
##    with open('test_IO.csv', mode='w') as save_file:
##        csv_writer = csv.writer(save_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
##        csv_writer.writerow([timestamp, mission_name, persona_name, thing_name,input_name, output_name,urlis])
## 
##
####
##with open('test_IO.csv', mode='w') as save_file:
##    csv_writer = csv.writer(save_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
##    csv_writer.writerow([timestamp, mission_name, persona_name, thing_name,input_name, input_name, 'November'])
##

    
##filename=input_name+'_'+output_name
##import subprocess
##subprocess.Popen(['wget', '-O', filename+'.png', 'http://images.websnapr.com/?url='+urlis+'&size=s&nocache=82']).wait()
##





##
##
##app = Flask(__name__)
##
##@app.route('/')
##def homepage():
##    return """
##    <h2 style = "font-family:verdana">
##    My cards are:
##    </h2>
##    <img src="/static/lightLevel.jpeg" alt="inoutput_name" width="100">
##    <img src="/static/icon.jpeg" alt="inoutput_name" width="100">
##    <h2 style = "font-family:verdana">
##    My code is:
##    </h2>
##    <iframe src="
##    """ + urlis + """
##    " width="
##    """ + width_makecode + """
##    " height="
##    """ + height_makecode + """
##    " frameborder="1" allowfullscreen></iframe>
##    """
##if __name__ == '__main__':
####    threading.Timer(1.25, lambda: webbrowser.open("http://127.0.0.1:5000") ).start()
##    threading.Timer(0, lambda: webbrowser.open("http://"+ip+":"+port) ).start()
##    app.run(debug=False)## , use_reloader=True)
##









# import random, threading, webbrowser

# port = 5000 + random.randint(0, 999)
# url = "http://127.0.0.1:{0}".format(port)

# threading.Timer(1.25, lambda: webbrowser.open(url) ).start()

# app.run(port=port, debug=False)



# <p style = "font-family:georgia,garamond,serif;font-size:16px;font-style:italic;">
#          This is demo text
#       </p>



##def homepage():
##    return """
##    <h1 style = "font-family:verdana">
##    IoTgo
##    </h1>
##
##    <iframe src=" https://makecode.microbit.org/--docs?md=%23%23%20My%20Code%0A%0A%60%60%60%20blocks%0Aservos.P1.setRange%280%2C180%29%0Abasic.forever%28function%20%28%29%20%7B%0A%20%20%20%20if%20%28pins.digitalReadPin%28DigitalPin.P2%29%20%3D%3D%201%29%7B%0A%20%20%20%20%20%20%20%20servos.P1.setAngle%2845%29%0A%20%20%20%20%20%20%20%20basic.pause%28100%29%0A%20%20%20%20%20%7D%20else%20%7Bservos.P1.setAngle%280%29%0A%20%20%20%20%20%20%20%20basic.pause%28100%29%0A%20%20%20%20%7D%0A%7D%29%0A%60%60%60%0A%0A%60%60%60package%0Aservo%0A%60%60%60
##" width="1200" height="960" frameborder="1" allowfullscreen></iframe>
##    """

#defining a dictionary for default code for each output: (when output is OFF by default)
# else_output_OFF = {
#   "fan":   "pins.digitalWritePin(DigitalPin.P1,0)",
#   "light": "pins.digitalWritePin(DigitalPin.P1,0)", 
#   "strip": "strip.showColor(neopixel.colors(NeoPixelColors.Black))", 
#   "rotate":"servos.P1.setAngle(0)", 
#   "sound": "music.stopMelody(MelodyStopOptions.All)", 
#   "icon":  "basic.clearScreen()", 
#   "text":  "basic.clearScreen()", 
# }


#defining a dictionary for default code for each output: (when output is ON by default)
# else_output_ON = {
#   "fan":   "pins.digitalWritePin(DigitalPin.P1,1)",
#   "light": "pins.digitalWritePin(DigitalPin.P1,1)",
#   "strip": "strip.showColor(neopixel.colors(NeoPixelColors.Red))", 
#   "rotate":"servos.P1.setAngle(90)", 
#   "sound": "music.startMelody(music.builtInMelody(Melodies.JumpUp), MelodyOptions.Forever)", 
#   "icon":  "basic.showIcon(IconNames.Heart)",  
#   "text":  "basic.showString(\"Hello\!\")", 
# }






# forecast code:
# radio.onReceivedValue(function (name, value) {
#     forecastName = name
#     forecastValue = value
# })
# let forecastValue = 0
# let forecastName = ""
# radio.setGroup(313)

# basic.forever(function () {
#     if (forecastName == "date" && forecastValue >= 28) {
#         basic.pause(100)
#     } else {
#         radio.sendString("get_date")
#         basic.pause(100)
#     }
# })
