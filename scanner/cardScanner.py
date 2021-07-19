"""

"""

import board
import busio
import binascii
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
from time import sleep
##from sense_hat import SenseHat from flask import Flask import threading, webbrowser
import random
import csv
import os
import re
import sys
import urllib.parse
import csv
import time
import textwrap

num_tCards=0
num_iCards=0
num_oCards=0
num_pCards=0
num_mCards=0
num_xCards=0

#flask variables:
##ip="127.0.0.1"#ip="192.168.1.4"
##port="5000"
##width_makecode="1000" 
##height_makecode="800"

#urlGen variables:
codetitle=""##codetitle="%23%20"
codesubtitle=""

#cardreader variables
data = bytearray(16)# Set 16 bytes of block to 0xFEEDBEEF
data[0:16] = list(b'\xCC\xCC\xCC\xCC\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
key = b'\xFF\xFF\xFF\xFF\xFF\xFF'
prevUid=b'\xFF\xFF\xFF\xFF'



#csvGen variables:
cardtype="0"
input_name="noInput"
output_name="noOutput"
userNum=0 #converts to str before saving
ideaNum=1 #converts to str before saving
thing_name="noThing"
mission_name="noMission"
persona_name="noPersona"
count=1
csvfilename='data.csv'
with open(csvfilename, mode='a') as save_file:
    csv_writer = csv.writer(save_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['timestamp', 'userNum', 'ideaNum', 'mission', 'persona', 'thing','input', 'output','url'])



    
in_type2name= {
  	str(b'10'):"buttonNotPress",
 	str(b'11'):"buttonPress",
  	str(b'20'):"accelLow" , 
  	str(b'21'):"accelHigh"  , 
  	str(b'31'):"compassE"  , 
  	str(b'32'):"compassW"  , 
	str(b'33'):"compassN"  , 
	str(b'34'):"compassS"  , 
	str(b'41'):"gestureShake"  , 
	str(b'42'):"gestureTilt"  , 
	str(b'51'):"movementPresent"  , 
	str(b'50'):"movementNotPresent"  , 
	str(b'60'):"noiseLow"  , 
	str(b'61'):"noiseHigh"  ,
	str(b'70'):"sliderLow"  , 
	str(b'71'):"sliderHigh"  , 
	str(b'80'):"tempLow"  , 
	str(b'81'):"tempHigh"  ,
	str(b'90'):"lightlevelLow",
	str(b'91'):"lightlevelHigh",
 	str(b'01'):"touchYes" ,#v2 #card not used 
 	str(b'00'):"touchNo"  , #v2 #card not used  
	str(b'a1'):"forecastTempHigh",
	str(b'a0'):"forecastTempLow",
	str(b'b1'):"forecastHumidityHigh",
	str(b'b0'):"forecastHumidityLow",
	str(b'c1'):"forecastWindHigh",
	str(b'c0'):"forecastWindLow",
	str(b'd1'):"forecastprecipHigh",
	str(b'd0'):"forecastprecipLow",
	str(b'e1'):"todayStartOfMonth",
	str(b'e2'):"todayWeekday",
	str(b'e3'):"todayWeekend",
	str(b'e4'):"todaySummerMonth",
	str(b'e5'):"todayNewYear",
	str(b'e6'):"timeForSchool",
# 	str(b'e7'):"timeSunrise",
# 	str(b'e8'):"timeSunset",
    }
    
out_type2name= {
    str(b'11'):"iconHappy",
    str(b'12'):"iconSad",
    str(b'10'):"iconNone",
  	str(b'21'):"lightOn",
 	str(b'22'):"lightOff",
  	str(b'31'):"musicHappy" , 
  	str(b'32'):"musicSad"  , 
	str(b'30'):"musicNone"  , 
# 	str(b'41'):"speakText"  , not supported yet
# 	str(b'42'):"speakInput"  ,not supported yet
# 	str(b'40'):"speakNone"  , not supported yet
	str(b'51'):"displayText"  , 
	str(b'52'):"displayInput"  , 
	str(b'50'):"displayNone"  , 
	str(b'61'):"showStripRainbow"  , 
	str(b'60'):"showStripBlack", 
	str(b'71'):"fanOn"  , 
	str(b'70'):"fanOff"  ,
	str(b'80'):"rotateMin"  , #card not used  
	str(b'85'):"rotateMid"  , #card not used 
	str(b'81'):"rotateMax"  , #card not used  
	str(b'a1'):"tweetText"  , 
	str(b'a2'):"tweetInput"  , 
	str(b'b1'):"logInput"  ,  

    }

thing_type2name= {
    str(b'01'):"pictoral",
    str(b'02'):"sculpture",
    str(b'03'):"decor",    
    str(b'04'):"model",
    str(b'05'):"ceramic",
    str(b'06'):"textile",    
    str(b'07'):"jewellery",
    str(b'08'):"book",
    str(b'09'):"informative",    
    str(b'10'):"blank",
    }

mission_type2name= {
    str(b'01'):"engagePeople",
    str(b'02'):"makePeopleUnderstand",
    str(b'03'):"inspirePeople",    
    str(b'04'):"addUtility",
    str(b'05'):"addDimension",
    str(b'06'):"connectEmotionally",    
    str(b'07'):"connectMemories",
    str(b'08'):"getToKnowPeople",
    str(b'10'):"blank",    
    }

persona_type2name= {
    str(b'01'):"myslef",
    str(b'02'):"elderly",
    str(b'03'):"teenager",    
    str(b'04'):"child",
    str(b'05'):"minority",
    str(b'06'):"physciallyChallenged",    
    str(b'07'):"immigrant",
    str(b'08'):"pet",
    str(b'09'):"anyone",    
    str(b'10'):"blank",
    }


control_type2name= {
    str(b'01'):"new_user",
    str(b'02'):"new_idea",
    str(b'10'):"modify_idea",
    str(b'11'):"loadidea1",
    str(b'12'):"loadidea2",
    str(b'13'):"loadidea3a",
    str(b'14'):"loadidea3b",
    str(b'15'):"loadidea4",
    str(b'16'):"loadidea5",
    
    }


def genURL (input_name, output_name):#here i am collecting chunks of code, encoding them, and concatenating them into a URL:
    on_start_code=""
    if input_name in on_start:
        on_start_code = on_start[input_name]+ '\n'
    elif output_name in on_start:
        on_start_code = on_start_code +  on_start[output_name]+ '\n'
    else:
        on_start_code=""
    print("onstart:",on_start_code)
    if output_name in output_else_code:
        else_output_code = output_else_code[output_name]+ '\n'
    else:
        else_output_code="basic.pause(100)"
    #    
    if input_name in output_else_code:#special cases for forecast: get_temp
        else_output_code = output_else_code[input_name]+ '\n'
    #      
    jscode= on_start_code  + 'basic.forever(function () {' + '\n' + '    ' + 'if (' + input_code[input_name]+'){\n'  + '    '*2 + output_code[output_name]+'\n'  + '    '*2 + 'basic.pause(100)' +'\n' +  '    ' + ' } else {\n'+'    '*2 + else_output_code +'\n' + '    '+'}\n})'    #jscode= on_start_code  + 'basic.forever(function () {' + '\n' + '    ' + 'if (' + input_code[input_name]+'){\n'  + '    '*2 + output_code[output_name]+'\n'  + '    '*2 + 'basic.pause(100)' +'\n' +  '    ' + ' } else {\n'+'    '*2 + else_output_code +'\n' + '    '*2 +'basic.pause(100)'+'\n'+'    '+'}\n})'
    #print(jscode)
    url='https://makecode.microbit.org/--docs?md='+codetitle+codesubtitle+'%0A%0A%60%60%60%20blocks%0A'
    for eachline in jscode:
        url=url+urllib.parse.quote(eachline) 
    url=url+'%0A%60%60%60%0A%0A'
    if output_name in package_suffix:
    	url=url+package_suffix[output_name]
    elif input_name in package_suffix:
        url=url+package_suffix[input_name]# to confirm if TWO packages can be added at the same time.   	
    return url




filepath = "/home/pi/Documents/sharedfiles"  #os.getcwd()
filename="iotgo.py"
#urlis=          "https://makecode.microbit.org/--docs?md=%23%23%0A%0A%60%60%60%20blocks%0Abasic.pause%281000%29%0Abasic.forever%28function%20%28%29%20%7B%0A%20%20%20%20if%20%28input.temperature%28%29%20%3E%2028%29%7B%0A%20%20%20%20%20%20%20%20basic.showIcon%28IconNames.Sad%29%0A%20%20%20%20%20%20%20%20basic.pause%28100%29%0A%20%20%20%20%20%7D%20else%20%7Bbasic.clearScreen%28%29%0A%20%20%20%20%20%20%20%20basic.pause%28100%29%0A%20%20%20%20%7D%0A%7D%29%0A%60%60%60%0A%0A%0A"
##missionpath=    "https://snap.inf.unibz.it/img/mission/mission1.jpg"
##personapath=    "https://static.streamlit.io/examples/dog.jpg"
##inputpath=      "https://snap.inf.unibz.it/img/input/button.jpg"
##thingpath=      "https://snap.inf.unibz.it/img/environment/tree.jpg"
##outputpath=     "https://snap.inf.unibz.it/img/output/icon.jpg"
urlis=""


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
	"forecastTempHigh":     "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"forecastTempLow":      "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"forecastHumidityHigh": "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"forecastHumidityLow":  "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"forecastWindHigh":     "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"forecastWindLow":      "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"forecastprecipHigh":   "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"forecastprecipLow":    "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"todayStartOfMonth":    "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"todayWeekday":         "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"todayWeekend":         "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"todaySummerMonth":     "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"todayNewYear":         "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
	"timeForSchool":         "radio.setGroup(313)\nradio.onReceivedValue(function (name, value) {\n forecastName = name\nforecastValue = value\n})\nlet forecastValue = 0\nlet forecastName = \"none\" ",
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
##	"movementNotPresent":"pins.digitalReadPin(DigitalPin.P0) == 1"  ,
##	"movementPresent" :"pins.digitalReadPin(DigitalPin.P0) >= 1000" , 
	"movementNotPresent":"pins.digitalReadPin(DigitalPin.P0) == 0"  ,
	"movementPresent" :"pins.digitalReadPin(DigitalPin.P0) >= 1" , 
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
	"none" :"none",
	"noInput" :"noInput",
	"noOutput" :"noOutput",
        
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
 	"iconHappy":"basic.clearScreen()\nbasic.pause(100)\n",
    "iconSad":  "basic.clearScreen()\nbasic.pause(100)\n",
    "iconNone":  "basic.showIcon(IconNames.Happy)\nbasic.pause(100)\n",
  	"lightOn": "pins.digitalWritePin(DigitalPin.P1,0)\nbasic.pause(100)\n",
 	"lightOff": "pins.digitalWritePin(DigitalPin.P1,1)\nbasic.pause(100)\n",
  	"musicHappy": "music.stopMelody(MelodyStopOptions.All)\nbasic.pause(100)\n",  
  	"musicSad" 	: "music.stopMelody(MelodyStopOptions.All)\nbasic.pause(100)\n", 
  	"musicNone" :  "music.startMelody(music.builtInMelody(Melodies.Birthday), MelodyOptions.Forever)\nbasic.pause(100)\n", 
#   "speakText"  : "", 
#   "speakInput" : "" , 
#   "speakNone" : "" , 
	"displayText" : "basic.clearScreen()\nbasic.pause(100)\n" , 
	"displayInput": "basic.clearScreen()\nbasic.pause(100)\n"  , 
 	"displayNone" : "basic.showString(\"hello\")\nbasic.pause(100)\n" , 
#  	"displayNone" : "basic.showString(\""+input_name+"\")\nbasic.pause(100)\n" , 
	"showStripRainbow":  "strip.showColor(neopixel.colors(NeoPixelColors.Black))\nbasic.pause(100)\n", 
	"showStripBlack" :"strip.showRainbow(1, 360)\nstrip.show()\nbasic.pause(100)\n",  
	"fanOn" :  	"pins.digitalWritePin(DigitalPin.P1,0)\nbasic.pause(100)\n", 
	"fanOff"  : "pins.digitalWritePin(DigitalPin.P1,1)\nbasic.pause(100)\n", 
 	"rotateMin" :"servos.P1.setAngle(180)\nbasic.pause(100)\n",#card not used 
 	"rotateMid" :"servos.P1.setAngle(0)\nbasic.pause(100)\n" , #card not used 
 	"rotateMax" :"servos.P1.setAngle(0)\nbasic.pause(100)\n" , #card not used    
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


baseURL="https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/cards/"

grabURL = {
    "pictoral":"EN-thing-art-1.png",
    "sculpture":"EN-thing-art-2.png",
    "decor":"EN-thing-art-3.png",    
    "model":"EN-thing-art-4.png",
    "ceramic":"EN-thing-art-5.png",
    "textile":"EN-thing-art-6.png" ,   
    "jewellery":"EN-thing-art-7.png",
    "book":"EN-thing-art-8.png",
    "informative":"EN-thing-art-9.png",    
    "blank":"EN-thing-art-0.png",
    "engagePeople":"EN-mission-1.png",
    "makePeopleUnderstand":"EN-mission-2.png",
    "inspirePeople":"EN-mission-3.png",    
    "addUtility":"EN-mission-4.png",
    "addDimension":"EN-mission-5.png",
    "connectEmotionally":"EN-mission-6.png",    
    "connectMemories":"EN-mission-7.png",
    "getToKnowPeople":"EN-mission-8.png",
    "blank":"EN-mission-0.png",    

    "myslef":"EN-persona-1.png",
    "elderly":"EN-persona-2.png",
    "teenager":"EN-persona-3.png",
    "child":"EN-persona-4.png",
    "minority":"EN-persona-5.png",
    "physciallyChallenged":"EN-persona-6.png",
    "immigrant":"EN-persona-7.png",
    "pet":"EN-persona-8.png",
    "anyone":"EN-persona-9.png",
    "blank":"EN-persona-0.png",
    "new_user":"EN-control-1.png",
    "new_idea":"EN-control-2.png",
  	
    "noMission"     :"noMission.png",  
    "noThing"       :"noThing.png",  
    "noPersona"     :"noPersona.png",  
    "noInput"       :"noInput.png",  
    "noOutput"      :"noOutput.png",
    "none"          :"",
    
    "buttonNotPress":"EN-inputPhy-buttonNotpressed.png",
    "buttonPress":"EN-inputPhy-buttonPress.png",
    "accelLow":"EN-inputPhy-AccelerationLow.png",
    "accelHigh" :"EN-inputPhy-AccelerationHigh.png",
    "compassN" :"EN-inputPhy-CompassNorth.png",
    "compassE" :"EN-inputPhy-CompassEast.png",
    "compassS" :"EN-inputPhy-CompassSouth.png",
    "compassW" :"EN-inputPhy-CompassWest.png",
    "gestureShake":"EN-inputPhy-GestureShake.png",
    "gestureTilt" :"EN-inputPhy-GestureTilt.png",
    "movementNotPresent":"EN-inputPhy-MovementNotPresent.png",
    "movementPresent" :"EN-inputPhy-MovementPresent.png",
    "noiseLow"  :"EN-inputPhy-NoiseLow.png",
    "noiseHigh"	:"EN-inputPhy-NoiseHigh.png",
    "touchYes" 	:"EN-inputPhy-LogoTouched.png",
    "touchNo"	:"EN-inputPhy-LogoNotTouched.png",
    "sliderLow":"EN-inputPhy-SliderMaximum.png",#toFIX
    "sliderMid":"EN-inputPhy-SliderMinimum.png",
    "sliderHigh":"EN-inputPhy-SliderMaximum.png",
    "tempLow"  :"EN-inputPhy-TemperatureLow.png",
    "tempHigh" :"EN-inputPhy-TemperatureHigh.png",
    "lightlevelLow" :"EN-inputPhy-LightlevelLow.png",
    "lightlevelHigh":"EN-inputPhy-LightlevelHigh.png",
    
        
    "forecastTempHigh" :"EN-inputCloud-ForecastTempreatureHigh.png",
    "forecastTempLow" :"EN-inputCloud-ForecastTempreatureLow.png",
    "forecastHumidityHigh" :"EN-inputCloud-ForecastHumidityHigh.png",
    "forecastHumidityLow" :"EN-inputCloud-ForecastHumidityLow.png",
    "forecastWindHigh" :"EN-inputCloud-ForecastWindHigh.png",
    "forecastWindLow" :"EN-inputCloud-ForecastWindLow.png",
    "forecastprecipHigh" :"EN-inputCloud-ForecastPercipitationHigh.png",
    "forecastprecipLow" :"EN-inputCloud-ForecastPercipitationLow.png",
    "todayStartOfMonth" :"EN-inputCloud-TodayMonthStart.png",
    "todayWeekday" :"EN-inputCloud-TodayWeekday.png",
    "todayWeekend":"EN-inputCloud-TodayWeekend.png",
    "todaySummerMonth":"EN-inputCloud-TodaySummerMonth.png",
    "todayNewYear":"EN-inputCloud-TodayNewYearDay.png",
    "timeForSchool" :"EN-inputCloud-TimeForSchool.png",     
    
    
    "iconHappy":"EN-outputPhy-ShowHappyIcon.png",
    "iconSad":"EN-outputPhy-ShowSadIcon.png",
     "iconNone":"EN-outputPhy-StopShowIcon.png",
    "lightOn":"EN-outputPhy-TurnOnLight.png",
    "lightOff":"EN-outputPhy-TurnOffLight.png",
    "musicHappy":"EN-outputPhy-PlayHappyMusic.png",
    "musicSad" :"EN-outputPhy-PlaySadMusic.png",
    "musicNone" :"EN-outputPhy-TurnOffMusic.png", 
    "displayText" :"EN-outputPhy-ShowText.png",  
    "displayInput":"EN-outputPhy-ShowInputValue.png",
    "displayNone" :"EN-outputPhy-StopShowText.png", 
    "showStripRainbow" :"EN-outputPhy-TurnRainbowLight.png",
    "showStripBlack" :"EN-outputPhy-TurnOffRainbowLight.png",
    "fanOn" :"EN-outputPhy-TurnOnFan.png",	 
    "fanOff"  :"EN-outputPhy-TurnOffFan.png",
    "rotateMin": "EN-inputPhy-RotateMin.png",
    "rotateMid": "EN-inputPhy-RotateMid.png",
    "rotateMax": "EN-inputPhy-RotateMax.png",
    
    "tweetText"  :"EN-outputCloud-TweetText.png", 
    "tweetInput" :"EN-outputCloud-TweetValue.png",   
    "logInput"   :"EN-inputCloud-LogValue.png",
	
}



def updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis):
    with open(csvfilename, mode='a') as save_file:
        csv_writer = csv.writer(save_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([str(time.time()), str(userNum), str(ideaNum), mission_name, persona_name, thing_name,input_name, output_name,urlis])
        #print(str(time.time()), str(userNum), str(ideaNum), mission_name, persona_name, thing_name,input_name, output_name,urlis)
        print("csv file updated")

def updatePyFile(mission_name, persona_name, thing_name,input_name, output_name,url):
    #temp_path = filepath + file_name
    temp_path=os.path.join(filepath,filename)
    thingpath=  baseURL+grabURL[thing_name]
    missionpath=baseURL+grabURL[mission_name]
    personapath=baseURL+grabURL[persona_name]
    inputpath=  baseURL+grabURL[input_name]
    outputpath= baseURL+grabURL[output_name]
    print(temp_path)
    gitloadpath="http://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/"
    with open(temp_path, 'w') as f:
        f.write(textwrap.dedent('''\
            import streamlit as st
            import streamlit.components.v1 as components
            st.set_page_config(page_title="IoTgo",page_icon=None,layout="wide")
            #streamlit.components.v1.html(html, width=None, height=None, scrolling=False)
            urlis="'''
            +url+
            '''"
            # embed streamlit docs in a streamlit app
            st.image("http://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/applogo.png",width=250)
            st.header("My cards are:")

            col1,  col3, col4, col5, col6 ,emptycol3,emptycol2,emptycol1 = st.beta_columns(8)

            with col1:
                st.write("Mission:")
                st.image("'''
            +missionpath+
            '''", width=200)
            with col3:
                st.write("Persona:")
                st.image("'''
            +personapath+
            '''", width=175)
            with col4:
                st.write("Thing:")
                st.image("'''
            +thingpath+
            '''", width=175)
            with col5:
                st.write("Input:")
                st.image("'''
            +inputpath+
            '''", width=175)
            with col6:
                st.write("Output:")
                st.image("'''
            +outputpath+
            '''", width=175)
            with emptycol1:
                st.button("refresh (r)")
            st.header("My code is:")
            components.iframe(urlis,width=900, height=700)#, scrolling=False)
            link ="[Click here to edit/download this code.]('''
            +url+
            ''')"
            st.markdown(link, unsafe_allow_html=True)
            '''))
    print('py file updated.')
##
##            st.write("'''
##            +url+
##            '''")


# SPI connection:
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
leftBot_gpio26 = DigitalInOut(board.D5)
print('Discovering card-readers')
print('card-reader: leftBot_gpio26')

#try:
pn532_leftBot  = PN532_SPI(spi, leftBot_gpio26, debug=False)
ic, ver, rev, support = pn532_leftBot.firmware_version

print('Found pn532_leftBot with firmware version: {0}.{1}'.format(ver, rev))
pn532_leftBot.SAM_configuration()
#except:
##    input_name=input("input_state: ")
##    output_name=input("output: ")



prev_input='noInput'
inputChanged=False
prev_output='noOutput'
outputChanged=False

updatePyFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)

# Main loop to detect cards and read a block.
print('Waiting for MiFare card...')
while True:

    # Check if a card is available to read:
    uid_left = pn532_leftBot.read_passive_target(timeout=0.5)
    if uid_left is None:# Try again if no card is available.
        continue
    
    if uid_left == prevUid:#Ignore if the same card is there. 
        continue
    #print('New card detected with UID: 0x{0}'.format(binascii.hexlify(uid_left)))
    prevUid = uid_left;
    
    # Authenticate block 4 for reading with default key (0xFFFFFFFFFFFF):
    if not pn532_leftBot.mifare_classic_authenticate_block(uid_left, 4, MIFARE_CMD_AUTH_B, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
        print('Failed to authenticate block 4!')
        continue

    data = pn532_leftBot.mifare_classic_read_block(4) # Reading block 4 data.
    if data is None:
        print('Failed to read block 4!')
        continue
    #print('Read block 4: 0x{0}'.format(binascii.hexlify(data[:4])))    # Note that 16 bytes are returned, so only show the first 4 bytes for the block.

    if data[:2]==b'\xC3\x3C':#num_eCards+=1
        thing_type=binascii.hexlify(data[2:3])
        thing_name=     thing_type2name[str(thing_type)]
        print("--found thing card # 0x{0}: ".format(thing_type),thing_name)#cardtype="t"
        updatePyFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)

    elif (data[:2]==b'\xC1\x1C'): 
        input_type=binascii.hexlify(data[2:3])
        input_name=     in_type2name[str(input_type)]
        print("--found input card # 0x{0}: ".format(input_type),input_name)#cardtype="t"
        updatePyFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
        if prev_input!=input_name:
            inputChanged=True
            #print('inputChanged=True')
        prev_input=input_name
    elif (data[:2]==b'\xC0\x0C'): 
        output_type=binascii.hexlify(data[2:3])
        output_name=    out_type2name[str(output_type)]
        print("--found output card # 0x{0}: ".format(output_type),output_name)#cardtype="t"        
        updatePyFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
        if prev_output!=output_name:
            outputChanged=True
            #print('outputChanged=True')
        prev_output=output_name
    elif (data[:2]==b'\xC2\x2C'): 
        mission_type=binascii.hexlify(data[2:3])
        mission_name=   mission_type2name[str(mission_type)]
        print("--found mission card # 0x{0}: ".format(mission_type),mission_name)#cardtype="t"
        updatePyFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
        
    elif (data[:2]==b'\xC4\x4C'): 
        persona_type=binascii.hexlify(data[2:3])
        persona_name=     persona_type2name[str(persona_type)]
        print("--found persona card # 0x{0}: ".format(persona_type),persona_name)#cardtype="t"
        updatePyFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
        
    elif (data[:2]==b'\xC5\x5C'): 
        control_type=binascii.hexlify(data[2:3])
        control_name=     control_type2name[str(control_type)]
        print("--found control card # 0x{0}: ".format(control_type),control_name)#cardtype="t"
        if control_name == 'new_idea':
            updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
            ideaNum=ideaNum+1
        elif control_name== 'new_user':
            updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
            userNum=userNum+1
            ideaNum=1
            input_name="noInput"
            output_name="noOutput" 
            thing_name="noThing"
            mission_name="noMission"
            persona_name="noPersona"
            urlis="https://makecode.microbit.org/--docs?md=Not%20Enough%20cards%20to%20generate%20code"
            updatePyFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
        elif control_name== 'loadidea1':
            updatePyFile("engagePeople", "child", "sculpture","movementPresent", "rotateMax" ,genURL("movementPresent", "rotateMax"))
            updateCsvFile("engagePeople", "child", "sculpture","movementPresent", "rotateMax" ,genURL("movementPresent", "rotateMax"))
        elif control_name== 'loadidea2':
            updatePyFile("addUtility", "anyone", "model","movementPresent", "lightOn" ,genURL("movementPresent", "lightOn"))    
            updateCsvFile("addUtility", "anyone", "model","movementPresent", "lightOn" ,genURL("movementPresent", "lightOn"))     
        elif control_name== 'loadidea3a':
            updatePyFile("getToKnowPeople", "anyone", "book","gestureTilt", "displayText" ,genURL("gestureTilt", "displayText"))   
            updateCsvFile("getToKnowPeople", "anyone", "book","gestureTilt", "displayText" ,genURL("gestureTilt", "displayText"))       
        elif control_name== 'loadidea3b':
            updatePyFile("getToKnowPeople", "anyone", "book","gestureTilt", "tweetText" ,genURL("gestureTilt", "tweetText"))     
            updateCsvFile("getToKnowPeople", "anyone", "book","gestureTilt", "tweetText" ,genURL("gestureTilt", "tweetText"))       
        elif control_name== 'loadidea4':
            updatePyFile("connectMemories", "elderly", "pictoral","movementPresent", "showStripRainbow" ,genURL("movementPresent", "showStripRainbow"))
            updateCsvFile("connectMemories", "elderly", "pictoral","movementPresent", "showStripRainbow" ,genURL("movementPresent", "showStripRainbow"))
        elif control_name== 'loadidea5':
            updatePyFile("addDimension", "myself", "decor","compassE", "rotateMax" ,genURL("compassE", "rotateMax"))
            updateCsvFile("addDimension", "myself", "decor","compassE", "rotateMax" ,genURL("compassE", "rotateMax"))
        elif control_name== 'modify_idea':
            ideaNum=ideaNum+1

            
            



    else:
        print("--unregistered card detected= 0x{0}".format(binascii.hexlify(data[:4]))) 


    #print(num_iCards)
    #print(num_oCards)
    if input_name!="noInput" and output_name!="noOutput":
        if outputChanged==True or inputChanged==True:
            print("new input-ouput combo")
            urlis=genURL(input_name,output_name)
            print("url updated")
            updatePyFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
        #print('New Javascrpt code is:\n',urlis)
        #if added here, remove in above:
        #updateCsvFile()

















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
