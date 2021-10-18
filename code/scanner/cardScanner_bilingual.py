"""

"""

import board
import busio
import binascii
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B##from sense_hat import SenseHat from flask import Flask import threading, webbrowser


from time import sleep
import random
import csv
import os
import re
import sys
import urllib.parse
import csv
import time
import textwrap
from github3 import login
import config
import github3

#language selection variables:
langPrefix=['EN','IT','DE','UR']
lang=0

#git variables:
gh = login(token=configc.password)
gituser = gh.me()
repo = gh.repository(gituser.login, 'iotgo-io')
gitfilepath='/webapp/iotgo.py'
#print(repo)

#csvGen variables:
csvfilename='schools2021sept.csv'
cardtype="0"
##input_name="noInput"
##output_name="noOutput"
input_name= ["noInput"  ,"noInput"  ,"noInput"]
output_name=["noOutput" ,"noOutput" ,"noOutput"]
userNum=0 #converts to str before saving
ideaNum=1 #converts to str before saving
thing_name="noThing"
mission_name="noMission"
persona_name="noPersona"
count=1
with open(csvfilename, mode='a') as save_file:
    csv_writer = csv.writer(save_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['timestamp', 'userNum', 'ideaNum', 'mission', 'persona', 'thing','input1', 'outpu1','input2', 'outpu2','input3', 'output3','url'])



##num_tCards=0
##num_iCards=0
##num_oCards=0
##num_pCards=0
##num_mCards=0
##num_xCards=0

#urlGen variables:
codetitle=""##codetitle="%23%20"
codesubtitle=""

#cardreader variables
data = bytearray(16)# Set 16 bytes of block to 0xFEEDBEEF
data[0:16] = list(b'\xCC\xCC\xCC\xCC\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
key = b'\xFF\xFF\xFF\xFF\xFF\xFF'
prevUid=b'\xFF\xFF\xFF\xFF'





    
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
 	str(b'20'):"lightOff",
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
    str(b'01'):"myself",
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
    str(b'11'):"loadidea1",#wings
    str(b'12'):"loadidea2",#gallery
    str(b'13'):"loadidea3a",#passport 
    str(b'14'):"loadidea3b",#tweet
    str(b'15'):"loadidea4",#zenframe
    str(b'16'):"loadidea5",#winchime
    str(b'09'):"generate_code",
    
    }


def genURL (*args):#input_name, output_name):#here i am collecting chunks of code, encoding them, and concatenating them into a URL:
     #----------on-start-code---------
    on_start_code=[]
    jscode=""
    for eachIOpair in args:
        #print(eachIOpair)
        for eachItem in eachIOpair:
            #print(eachItem)
            if eachItem != "noInput" and eachItem != "noOutput": 
                if eachItem in on_start:
                    on_start_code.append(on_start[eachItem]+ '\n')
    print("onstart:",on_start_code)
    on_start_code_noDup= list( dict.fromkeys(on_start_code) )
    print("onstart_noDup:",on_start_code_noDup)    
    for eachline in on_start_code_noDup:
        jscode= jscode + eachline
    jscode= jscode + 'basic.forever(function () {' + '\n' 
    #-----------if-else-code---------
    for eachIOpair in args: #in,out
        if eachIOpair[0] != "noInput" and eachIOpair[1] != "noOuput":
            if eachIOpair[1] in output_else_code:
                else_code = output_else_code[eachIOpair[1]]+ '\n'
            else:
                else_code="basic.pause(100)"
            if eachIOpair[0] in output_else_code:#special cases for forecast: get_temp
                    else_code = output_else_code[eachIOpair[0]]+ '\n'

            jscode= jscode  \
                + '    ' + 'if (' +  input_code[eachIOpair[0]]+'){\n'  \
                + '    ' + '    ' + output_code[eachIOpair[1]]+'\n'  \
                + '    ' + '    ' + 'basic.pause(100)' +'\n' \
                + '    ' + ' } else {\n' \
                + '    ' + '    ' + else_code +'\n' \
                + '    ' + '}\n'
    #-----------on_end_code---------
    jscode=jscode+'})'
    print(jscode)
    
    #------enclose jscode in URL:---    
    url='https://makecode.microbit.org/--docs?md='+codetitle+codesubtitle+'%0A%0A%60%60%60%20blocks%0A'
    for eachline in jscode:
        url=url+urllib.parse.quote(eachline) 
    url=url+'%0A%60%60%60%0A%0A'
    #-----------add-extensions-code---------
    on_end_code=[]
    for eachIOpair in args:
        for eachItem in eachIOpair: 
            if eachItem != "noInput" and eachItem != "noOutput":
                if eachItem in package_suffix:
                    on_end_code.append(package_suffix[eachItem])
                #url=url+package_suffix[eachItem]
    print(on_end_code)
    on_end_code_noDup= list( dict.fromkeys(on_end_code) )
    print(on_end_code_noDup)
    for eachline in on_end_code_noDup:
        url=url+eachline
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


#defining a dictionary for any additional extension/package needed for each output: %60%60%60package%0Aservo%0A%60%60%60  wrong="%60%60%%0Aservo%0A%60%60%60"
package_suffix = {
	"rotateMin"         : "%60%60%60package%0Aservo%0A%60%60%60", 
	"rotateMid"         : "%60%60%60package%0Aservo%0A%60%60%60",
	"rotateMax"         : "%60%60%60package%0Aservo%0A%60%60%60",
	"showStripRainbow"  : "%60%60%60package%0Aneopixel%3Dgithub%3Amicrosoft%2Fpxt-neopixel%0A%0A%60%60%60", 
	"showStripBlack"    : "%60%60%60package%0Aneopixel%3Dgithub%3Amicrosoft%2Fpxt-neopixel%0A%0A%60%60%60", 
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
	"displayText" : "basic.showString(\"Ciao from Bari\")" , 
	"displayInput": "basic.showString(\""+input_name[2]+"\")"  , 
 	"displayNone" :"basic.clearScreen()" , 
	"showStripRainbow" : "strip.showRainbow(1, 360)\nstrip.show()", 
	"showStripBlack" : "strip.showColor(neopixel.colors(NeoPixelColors.Black))", 
	"fanOn" :  	"pins.digitalWritePin(DigitalPin.P1,1)", 
	"fanOff"  : "pins.digitalWritePin(DigitalPin.P1,0)", 
 	"rotateMin" :"servos.P1.setAngle(0)" ,   #card not used 
 	"rotateMid" :"servos.P1.setAngle(90)" ,  #card not used 
 	"rotateMax" :"servos.P1.setAngle(180)" , #card not used    
	"tweetText"  : "radio.sendString(\"#CiaoFromBari\")" , 
	"tweetInput" : "radio.sendString(\"#"+input_name[2]+"\")" , #add input name and value directly???use variable
	"logInput"   : "radio.sendValue(\"&value\","+input_sensorValue[input_name[2]]+")",  #add input name and value directly???use variable
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


grabURL =    {
    "pictoral":     "-thing-art-1.png",
    "sculpture":    "-thing-art-2.png",
    "decor":        "-thing-art-3.png",    
    "model":        "-thing-art-4.png",
    "ceramic":      "-thing-art-5.png",
    "textile":      "-thing-art-6.png" ,   
    "jewellery":    "-thing-art-7.png",
    "book":         "-thing-art-8.png",
    "informative":  "-thing-art-9.png",    
    "blank":        "-thing-art-0.png",
    
    "engagePeople":     "-mission-1.png",
    "makePeopleUnderstand":"-mission-2.png",
    "inspirePeople":    "-mission-3.png",    
    "addUtility":       "-mission-4.png",
    "addDimension":     "-mission-5.png",
    "connectEmotionally":"-mission-6.png",    
    "connectMemories":  "-mission-7.png",
    "getToKnowPeople":  "-mission-8.png",
    "blank":            "-mission-0.png",    

    "myslef":           "-persona-1.png",
    "elderly":          "-persona-2.png",
    "teenager":         "-persona-3.png",
    "child":            "-persona-4.png",
    "minority":         "-persona-5.png",
    "physciallyChallenged":"-persona-6.png",
    "immigrant":        "-persona-7.png",
    "pet":              "-persona-8.png",
    "anyone":           "-persona-9.png",
    "blank":            "-persona-0.png",
    "new_user":         "-control-1.png",
    "new_idea":         "-control-2.png",
  	
    "noMission"     :   "-noMission.png",  
    "noThing"       :   "-noThing.png",  
    "noPersona"     :   "-noPersona.png",  
    "noInput"       :   "-noInput.png",  
    "noOutput"      :   "-noOutput.png",
    "none"          :   "",
    "blanckCard"    :   "-blankcard.png",

    "codeCard"    :   "-codecard.png",
    "playerCard"    :   "-playercard.png",#not used in app

    
    "buttonNotPress":   "-inputPhy-buttonNotpressed.png",
    "buttonPress":      "-inputPhy-buttonPress.png",
    "accelLow":         "-inputPhy-AccelerationLow.png",
    "accelHigh" :       "-inputPhy-AccelerationHigh.png",
    "compassN" :        "-inputPhy-CompassNorth.png",
    "compassE" :        "-inputPhy-CompassEast.png",
    "compassS" :        "-inputPhy-CompassSouth.png",
    "compassW" :        "-inputPhy-CompassWest.png",
    "gestureShake":     "-inputPhy-GestureShake.png",
    "gestureTilt" :     "-inputPhy-GestureTilt.png",
    "movementNotPresent":"-inputPhy-MovementNotPresent.png",
    "movementPresent" : "-inputPhy-MovementPresent.png",
    "noiseLow"  :       "-inputPhy-NoiseLow.png",
    "noiseHigh"	:       "-inputPhy-NoiseHigh.png",
    "touchYes" 	:       "-inputPhy-LogoTouched.png",
    "touchNo"	:       "-inputPhy-LogoNotTouched.png",
    "sliderLow":        "-inputPhy-SliderMinimum.png",
    "sliderMid":        "-inputPhy-SliderMaximum.png",#not used. 
    "sliderHigh":       "-inputPhy-SliderMaximum.png",
    "tempLow"  :        "-inputPhy-TemperatureLow.png",
    "tempHigh" :        "-inputPhy-TemperatureHigh.png",
    "lightlevelLow" :   "-inputPhy-LightlevelLow.png",
    "lightlevelHigh":   "-inputPhy-LightlevelHigh.png",
    
        
    "forecastTempHigh" :    "-inputCloud-ForecastTempreatureHigh.png",
    "forecastTempLow" :     "-inputCloud-ForecastTempreatureLow.png",
    "forecastHumidityHigh" :"-inputCloud-ForecastHumidityHigh.png",
    "forecastHumidityLow" : "-inputCloud-ForecastHumidityLow.png",
    "forecastWindHigh" :    "-inputCloud-ForecastWindHigh.png",
    "forecastWindLow" :     "-inputCloud-ForecastWindLow.png",
    "forecastprecipHigh" :  "-inputCloud-ForecastPercipitationHigh.png",
    "forecastprecipLow" :   "-inputCloud-ForecastPercipitationLow.png",
    "todayStartOfMonth" :   "-inputCloud-TodayMonthStart.png",
    "todayWeekday" :        "-inputCloud-TodayWeekday.png",
    "todayWeekend":         "-inputCloud-TodayWeekend.png",
    "todaySummerMonth":     "-inputCloud-TodaySummerMonth.png",
    "todayNewYear":         "-inputCloud-TodayNewYearDay.png",
    "timeForSchool" :       "-inputCloud-TimeForSchool.png",     
    
    
    "iconHappy":    "-outputPhy-ShowHappyIcon.png",
    "iconSad":      "-outputPhy-ShowSadIcon.png",
     "iconNone":    "-outputPhy-StopShowIcon.png",
    "lightOn":      "-outputPhy-TurnOnLight.png",
    "lightOff":     "-outputPhy-TurnOffLight.png",
    "musicHappy":   "-outputPhy-PlayHappyMusic.png",
    "musicSad" :    "-outputPhy-PlaySadMusic.png",
    "musicNone" :   "-outputPhy-TurnOffMusic.png", 
    "displayText" : "-outputPhy-ShowText.png",  
    "displayInput": "-outputPhy-ShowInputValue.png",
    "displayNone" : "-outputPhy-StopShowText.png", 
    "showStripRainbow" :"-outputPhy-TurnRainbowLight.png",
    "showStripBlack" :"-outputPhy-TurnOffRainbowLight.png",
    "fanOn" :       "-outputPhy-TurnOnFan.png",	 
    "fanOff"  :     "-outputPhy-TurnOffFan.png",
    "rotateMin":    "-ouputPhy-RotateMin.png", 
    "rotateMid":    "-ouputPhy-RotateMax.png",#not used. 
    "rotateMax":    "-ouputPhy-RotateMax.png",
    
    "tweetText"  :  "-outputCloud-TweetText.png", 
    "tweetInput" :  "-outputCloud-TweetValue.png",   
    "logInput"   :  "-outputCloud-LogValue.png", #fixed

    
}



def updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis):
    with open(csvfilename, mode='a') as save_file:
        csv_writer = csv.writer(save_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([str(time.time()), str(userNum), str(ideaNum), mission_name, persona_name, thing_name,input_name[0], output_name[0],input_name[1],output_name[1],input_name[2],output_name[2],urlis])
        #print(str(time.time()), str(userNum), str(ideaNum), mission_name, persona_name, thing_name,input_name, output_name,....,urlis)
        print("csv file updated")

def updatePyFile(mission_name, persona_name, thing_name,input_name, output_name,url):
    #temp_path = filepath + file_name
    temp_path=os.path.join(filepath,filename)
    thingpath=   baseURL+langPrefix[lang]+grabURL[thing_name]
    missionpath= baseURL+langPrefix[lang]+grabURL[mission_name]
    personapath= baseURL+langPrefix[lang]+grabURL[persona_name]
    input0path=  baseURL+langPrefix[lang]+grabURL[ input_name[0]]
    output0path= baseURL+langPrefix[lang]+grabURL[output_name[0]]
    input1path=  baseURL+langPrefix[lang]+grabURL[ input_name[1]]
    output1path= baseURL+langPrefix[lang]+grabURL[output_name[1]]
    input2path=  baseURL+langPrefix[lang]+grabURL[ input_name[2]]
    output2path= baseURL+langPrefix[lang]+grabURL[output_name[2]]

    #langPrefix=['EN','IT','DE','UR']

    langlable=langPrefix[lang]
    print("selected language is ",langlable)
    whenText= {'EN':'if',  'IT':'se',    'DE':'when','UR':'jbb',}
    thenText= {'EN':'then','IT':'allora','DE':'then','UR':'tbb',}
    editText= {'EN':'Edit','IT':'Modificare','DE':'Edit','UR':'Edit karain',}
    codeisText= {'EN':'My code is:','IT':'Il mio codice è:','DE':'My code is:','UR':'Mera code hey:',}

    pyfilecontents=textwrap.dedent('''\
            #this file was updated on '''+time.ctime()+'''
            import streamlit as st
            import streamlit.components.v1 as components
            st.set_page_config(page_title="IoTgo",page_icon=None,layout="wide")
            urlis="'''+url+'''"

            cardWidth=100
            pluscardwidht=100
            missionCardWidth=160
            vertiPaddingWidth=35

            # st.markdown("""""")
            applogo, empty1, empty2, mission,empty3, persona, thing, empty4,edit  = st.beta_columns(9)

            with applogo:
                st.image("http://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/applogo3.png",width=500)
            with mission:
                st.image("'''+missionpath+'''", width=missionCardWidth)
            with persona:
                st.image("'''+personapath+'''", width=cardWidth)
            with thing:
                st.image("'''+thingpath+'''", width=cardWidth)
            with edit:
                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/blankcard.png", width=60)
                st.markdown("['''+editText[langlable]+''']("+urlis+")", unsafe_allow_html=True)

            input_col, plus_col, output_col,  code_col, emptycol , emptycol , emptycol, emptycol,emptycol,emptycol,emptycol = st.beta_columns(11)

            with input_col:    
                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/blankcard.png", width=vertiPaddingWidth)
                st.write("'''+whenText[langlable]+'''...")
                # ("Input1:")
                st.image("'''+input0path+'''", width=cardWidth)
                # ("Input2:")
                st.image("'''+input1path+'''", width=cardWidth)
                # ("Input3:")
                st.image("'''+input2path+'''", width=cardWidth)

            with plus_col:    
                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/blankcard.png", width=vertiPaddingWidth*2)
                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/plus.png", width=pluscardwidht)
                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/plus.png", width=pluscardwidht)
                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/plus.png", width=pluscardwidht)    

            with output_col:    
                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/blankcard.png", width=vertiPaddingWidth)
                st.write("'''+thenText[langlable]+'''...")
                # ("Output1:")
                st.image("'''+output0path+'''", width=cardWidth)
                # ("Output2:")
                st.image("'''+output1path+'''", width=cardWidth)
                # ("Output3:")
                st.image("'''+output2path+'''", width=cardWidth)
                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/blankcard.png", width=vertiPaddingWidth)

            with code_col:
                # st.header("'''+codeisText[langlable]+'''")
                components.iframe(urlis,width=900, height=1500, scrolling=True)


            st.button("Refresh")
            ''')

    print(temp_path)
    gitloadpath="http://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/"
    with open(temp_path, 'w') as f:    
        f.write(pyfilecontents)        
    print('local-py file updated.')
    print('git-py file-updated on '+time.ctime())
    repo.file_contents(gitfilepath).update('file-updated on '+time.ctime(),pyfilecontents.encode('utf-8') ) #repo.file_contents(gitfilepath).update('commit message', 'file contentwww'.encode('utf-8'))

    


##        f.write(textwrap.dedent('''\
##            #this file was updated on '''+time.ctime()+'''
##            import streamlit as st
##            import streamlit.components.v1 as components
##            st.set_page_config(page_title="IoTgo",page_icon=None,layout="wide")
##            urlis="'''+url+'''"
##            
##            cardWidth=140
##            pluscardwidht=140
##            missionCardWidth=175
##            vertiPaddingWidth=50
##
##            # st.markdown("""""")
##            applogo, empty1, empty2, mission, persona, empty3, thing, empty4,empty5  = st.beta_columns(9)
##
##            with applogo:
##                st.image("http://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/applogo3.png",width=500)
##            with mission:
##                st.image("'''+missionpath+'''", width=missionCardWidth)
##            with persona:
##                st.image("'''+personapath+'''", width=cardWidth)
##            with thing:
##                st.image("'''+thingpath+'''", width=cardWidth)
##
##            input_col, plus_col, output_col,  code_col, emptycol , emptycol2 , emptycol3, emptycol4,emptycol5,emptycol6 = st.beta_columns(10)
##
##
##            with input_col:    
##                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/blankcard.png", width=vertiPaddingWidth)
##                st.write("'''+whenText[langlable]+'''...")
##                # ("Input1:")
##                st.image("'''+input0path+'''", width=cardWidth)
##                # ("Input2:")
##                st.image("'''+input1path+'''", width=cardWidth)
##                # ("Input3:")
##                st.image("'''+input2path+'''", width=cardWidth)
##
##            with plus_col:    
##                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/blankcard.png", width=vertiPaddingWidth)
##                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/plus.png", width=pluscardwidht)
##                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/plus.png", width=pluscardwidht)
##                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/plus.png", width=pluscardwidht)    
##            with output_col:    
##                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/blankcard.png", width=vertiPaddingWidth)
##                st.write("'''+thenText[langlable]+'''...")
##                # ("Output1:")
##                st.image("'''+output0path+'''", width=cardWidth)
##                # ("Output2:")
##                st.image("'''+output1path+'''", width=cardWidth)
##                # ("Output3:")
##                st.image("'''+output2path+'''", width=cardWidth)
##                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/blankcard.png", width=vertiPaddingWidth)
##
##
##            with code_col:
##                # st.header("'''+codeisText[langlable]+'''")
##                components.iframe(urlis,width=1100, height=1500, scrolling=True)
##                
##            with emptycol5:
##                st.button("Refresh (r)")
##            with emptycol6:
##                st.image("https://raw.githubusercontent.com/rizMehdi/IoTgo/main/images/blankcard.png", width=32)
##                st.markdown("['''+editText[langlable]+''']("+urlis+")", unsafe_allow_html=True)
##            '''))
#Uncoment for testing URL manually:
#urlis=genURL(['buttonPress','lightOn'],['tempHigh','tweetText'],['lightlevelLow','showStripRainbow'])
#urlis=genURL(['buttonPress','showStripRainbow'],['tempHigh','showStripRainbow'],['lightlevelLow','showStripRainbow'])
#urlis=genURL(['buttonPress','showStripRainbow'],['tempHigh','showStripRainbow'],['lightlevelLow','showStripRainbow'],['lightlevelLow','showStripRainbow'])
##urlis=genURL(['buttonPress','showStripRainbow'],['tempHigh','rotateMax'],['lightlevelLow','tweetText'])
##print(urlis)
##input()

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
gamelevel=0
updatePyFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
urlis="https://makecode.microbit.org/--docs?md=Not%20Enough%20cards%20to%20generate%20code"

#urlis=genURL(['buttonPress','showStripRainbow'],['tempHigh','rotateMax'],['lightlevelLow','tweetText'])

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
        print("--found thing card # 0x{0}: ".format(thing_type),thing_name),"during gamelevel ",gamelevel#cardtype="t"
        updatePyFile( mission_name, persona_name, thing_name,input_name, output_name,urlis)
        updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)

    elif (data[:2]==b'\xC1\x1C'): 
        input_type=binascii.hexlify(data[2:3])
        input_name[gamelevel]=     in_type2name[str(input_type)]
        print("--found input card # 0x{0}: ".format(input_type),input_name[gamelevel],"during gamelevel ",gamelevel)#cardtype="t"
        updatePyFile( mission_name, persona_name, thing_name,input_name, output_name,urlis)
        updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
        if prev_input!=input_name[gamelevel]:
            inputChanged=True
            #print('inputChanged=True')
        prev_input=input_name[gamelevel]
    elif (data[:2]==b'\xC0\x0C'): 
        output_type=binascii.hexlify(data[2:3])
        output_name[gamelevel]=    out_type2name[str(output_type)]
        print("--found output card # 0x{0}: ".format(output_type),output_name[gamelevel],"during gamelevel ",gamelevel)#cardtype="t"
        updatePyFile( mission_name, persona_name, thing_name,input_name, output_name,urlis)
        updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
        if prev_output!=output_name[gamelevel]:
            outputChanged=True
            #print('outputChanged=True')
        prev_output=output_name[gamelevel]
    elif (data[:2]==b'\xC2\x2C'): 
        mission_type=binascii.hexlify(data[2:3])
        mission_name=   mission_type2name[str(mission_type)]
        print("--found mission card # 0x{0}: ".format(mission_type),mission_name,"during gamelevel ",gamelevel)#cardtype="t"
        updatePyFile( mission_name, persona_name, thing_name,input_name, output_name,urlis)
        updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
    elif (data[:2]==b'\xC4\x4C'): 
        persona_type=binascii.hexlify(data[2:3])
        persona_name=     persona_type2name[str(persona_type)]
        print("--found persona card # 0x{0}: ".format(persona_type),persona_name,"during gamelevel ",gamelevel)#cardtype="t"
        updatePyFile( mission_name, persona_name, thing_name,input_name, output_name,urlis)
        updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
    elif (data[:2]==b'\xC5\x5C'): 
        control_type=binascii.hexlify(data[2:3])
        control_name=     control_type2name[str(control_type)]
        print("--found control card # 0x{0}: ".format(control_type),control_name,"during gamelevel ",gamelevel)#cardtype="t"
        if control_name == 'new_idea':
            gamelevel=0
            updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
            ideaNum=ideaNum+1
        elif control_name== 'new_user':
            gamelevel=0
            updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
            userNum=userNum+1
            ideaNum=0
            input_name= ["noInput"  ,"noInput"  ,"noInput"]
            output_name=["noOutput" ,"noOutput" ,"noOutput"]
            thing_name="noThing"
            mission_name="noMission"
            persona_name="noPersona"
            urlis="https://makecode.microbit.org/--docs?md=Not%20Enough%20cards%20to%20generate%20code"
            updatePyFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
        elif control_name== 'loadidea1':
            ideaNum=-1
            thing_name="sculpture"
            mission_name="engagePeople"
            persona_name="child"
            input_name= ["movementPresent"  ,"noInput"  ,"noInput"]
            output_name=["rotateMax" ,"noOutput" ,"noOutput"]
            updatePyFile( mission_name, persona_name, thing_name,input_name, output_name,urlis)
            updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
##            updatePyFile("engagePeople", "child", "sculpture","movementPresent", "rotateMax"  ,genURL(["movementPresent", ""]))
##            updateCsvFile("engagePeople", "child", "sculpture","movementPresent", "rotateMax" ,genURL(["movementPresent", "rotateMax"]))
        elif control_name== 'loadidea2':
            ideaNum=-1
            thing_name="model"
            mission_name="addUtility"
            persona_name="anyone"
            input_name= ["movementPresent"  ,"noInput"  ,"noInput"]
            output_name=["lightOn" ,"noOutput" ,"noOutput"]
            updatePyFile( mission_name, persona_name, thing_name,input_name, output_name,urlis)
            updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
            #updatePyFile("addUtility", "anyone", "model","movementPresent", "lightOn"  ,genURL(["movementPresent", "lightOn"]))    
            #updateCsvFile("addUtility", "anyone", "model","movementPresent", "lightOn" ,genURL(["movementPresent", "lightOn"]))     
        elif control_name== 'loadidea3a':
            ideaNum=-1
            thing_name="book"
            mission_name="getToKnowPeople"
            persona_name="anyone"
            input_name= ["gestureTilt"  ,"noInput"  ,"gestureTilt"]
            output_name=["displayText" ,"noOutput" ,"tweetText"]
            updatePyFile( mission_name, persona_name, thing_name,input_name, output_name,urlis)
            updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
            #updatePyFile("getToKnowPeople", "anyone", "book","gestureTilt", "displayText"  ,genURL(["gestureTilt", "displayText"]))   
            #updateCsvFile("getToKnowPeople", "anyone", "book","gestureTilt", "displayText" ,genURL(["gestureTilt", "displayText"]))       
        elif control_name== 'loadidea3b':
            ideaNum=-1
            input_name="gestureTilt"
            output_name="tweetText" 
            thing_name="book"
            mission_name="getToKnowPeople"
            persona_name="anyone"
            input_name= ["gestureTilt"  ,"noInput" ,"gestureTilt"]
            output_name=["displayText" ,"noOutput" ,"tweetText"]
            updatePyFile( mission_name, persona_name, thing_name,input_name, output_name,urlis)
            updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
            #updatePyFile("getToKnowPeople", "anyone", "book","gestureTilt", "tweetText"  ,genURL(["gestureTilt", "tweetText"]))     
            #updateCsvFile("getToKnowPeople", "anyone", "book","gestureTilt", "tweetText" ,genURL(["gestureTilt", "tweetText"]))       
        elif control_name== 'loadidea4':
            ideaNum=-1
            thing_name="pictoral"
            mission_name="connectMemories"
            persona_name="elderly"
            input_name= ["movementPresent"  ,"noInput"  ,"noInput"]
            output_name=["showStripRainbow" ,"noOutput" ,"noOutput"]
            updatePyFile( mission_name, persona_name, thing_name,input_name, output_name,urlis)
            updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
            #updatePyFile("connectMemories", "elderly", "pictoral","movementPresent", "showStripRainbow" ,genURL(["movementPresent", "showStripRainbow"]))
            #updateCsvFile("connectMemories", "elderly", "pictoral","movementPresent", "showStripRainbow" ,genURL(["movementPresent", "showStripRainbow"]))
        elif control_name== 'loadidea5':
            ideaNum=-1
            thing_name="decor"
            mission_name="addDimension"
            persona_name="myself"
            input_name= ["compassE"  ,"noInput"  ,"noInput"]
            output_name=["rotateMax" ,"noOutput" ,"noOutput"]
            updatePyFile( mission_name, persona_name, thing_name,input_name, output_name,urlis)
            updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
            #updatePyFile("addDimension", "myself", "decor","compassE", "rotateMax" , genURL(["compassE", "rotateMax"]))
            #updateCsvFile("addDimension", "myself", "decor","compassE", "rotateMax" ,genURL(["compassE", "rotateMax"]))
        elif control_name== 'modify_idea':
            ideaNum=ideaNum+1
            updateCsvFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
        elif control_name== 'generate_code':
            print("finished gamelevel#",gamelevel)
            if input_name[gamelevel]!="noInput" and output_name[gamelevel]!="noOutput":
                if outputChanged==True or inputChanged==True:
                    print("new input-ouput combo")
                    urlis=genURL([input_name[0],output_name[0]],[input_name[1],output_name[1]],[input_name[2],output_name[2]],)
                    updatePyFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
                    gamelevel+=1
            else:
                urlis="https://makecode.microbit.org/--docs?md=Not%20enough%20cards%20to%20generate%20code"
                updatePyFile(mission_name, persona_name, thing_name,input_name, output_name,urlis)
#urlis=genURL(['buttonPress','showStripRainbow'],['tempHigh','rotateMax'],['lightlevelLow','tweetText'])


    else:
        print("--unregistered card detected= 0x{0}".format(binascii.hexlify(data[:4]))) 

