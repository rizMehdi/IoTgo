"""

"""

import board
import busio
import binascii
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
from time import sleep
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B

# SPI connection:
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)


cs_gpio5 = DigitalInOut(board.D5)
print('Discovering card-reader')
pn532_left  = PN532_SPI(spi, cs_gpio5, debug=False)
ic, ver, rev, support = pn532_left.firmware_version
print('Found PN532_left with firmware version: {0}.{1}'.format(ver, rev))
pn532_left.SAM_configuration()


# Set 16 bytes of block to 0xFEEDBEEF
data = bytearray(16)
data[0:16] = list(b'\xFE\xED\xBE\xEF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
key = b'\xFF\xFF\xFF\xFF\xFF\xFF'


bytechart={
    "1": b'\x01',
    "2": b'\x02',
    "3": b'\x03',
    "4": b'\x04',
    "5": b'\x05',
    "6": b'\x06',
    "7": b'\x07',
    "8": b'\x08',
    "9": b'\x09',
    "13": b'\x13',
    "14": b'\x14',
    "15": b'\x15',
    "16": b'\x16',
    "17": b'\x17',
    "18": b'\x18',
    "19": b'\x19',
    "0": b'\x00',
    "11": b'\x11',
    "10": b'\x10',
    "12": b'\x12',
    "21": b'\x21',
    "20": b'\x20',
    "31": b'\x31',
    "30": b'\x30',
    "32": b'\x32',
    "33": b'\x33',
    "34": b'\x34',
    "41": b'\x41',
    "42": b'\x42',
    "40": b'\x40',
    "51": b'\x51',
    "50": b'\x50',
    "52": b'\x22',
    "61": b'\x61',
    "60": b'\x60',
    "71": b'\x71',
    "70": b'\x70',
    "81": b'\x81',
    "80": b'\x80',
    "91": b'\x91',
    "90": b'\x90',

    
    "111": b'\xA1',
    "110": b'\xA0',
    "112": b'\xA2',
    "221": b'\xB1',
    "220": b'\xB0',
    "331": b'\xC1',
    "330": b'\xC0',
    "441": b'\xD1',
    "440": b'\xD0',
    "550": b'\xE0',
    "551": b'\xE1',
    "552": b'\xE2',
    "553": b'\xE3',
    "554": b'\xE4',
    "555": b'\xE5',
    "556": b'\xE6',
    "557": b'\xE7',
    "558": b'\xE8',}
    
# Main loop to detect cards and read a block.
print('Waiting for MiFare card...')
while True:
    # Check if a card is available to read.
    uid_left = pn532_left.read_passive_target()
    # Try again if no card is available.
    if uid_left is None:
        continue
    print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid_left)))
    # Authenticate block 4 for reading with default key (0xFFFFFFFFFFFF).
    if not pn532_left.mifare_classic_authenticate_block(uid_left, 4, MIFARE_CMD_AUTH_B,
                                                   [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
        print('Failed to authenticate block 4!')
        continue
    # Read block 4 data.
    data = pn532_left.mifare_classic_read_block(4)
    if data is None:
        print('Failed to read block 4!')
        continue
    # Note that 16 bytes are returned, so only show the first 4 bytes for the block.
    print('Read block 4: 0x{0}'.format(binascii.hexlify(data[:4])))
    if data[:2]==b'\xC3\x3C':
        print("found a thing Card, number: 0x{0}".format(binascii.hexlify(data[2:3])))
    elif (data[:2]==b'\xC1\x1C'):
        print("found a ouput Card, number: 0x{0}".format(binascii.hexlify(data[2:3])))
    elif (data[:2]==b'\xC0\x0C'):
        print("found a input Card, number: 0x{0}".format(binascii.hexlify(data[2:3])))
    elif (data[:2]==b'\xC4\x4C'):
        print("found a persona Card, number: 0x{0}".format(binascii.hexlify(data[2:3])))
    elif (data[:2]==b'\xC2\x2C'):
        print("found a ,mission Card, number: 0x{0}".format(binascii.hexlify(data[2:3])))
    elif (data[:2]==b'\xC5\x5C'):
        print("found a control Card, number: 0x{0}".format(binascii.hexlify(data[2:3])))
    else:
        print("unregistered = 0x{0}".format(binascii.hexlify(data[:4])))

        
    changeCard=input('do you want to change card type? (y) y/n...')
    if changeCard!="n":
        cardtype=input("enter card type: m/p/t/i/o/x :   ")
        print('you said: ', cardtype)
        cardTypedata=data
        if cardtype=="t":
            print("writing thing Card")
            cardTypedata[:2]=b'\xC3\x3C'#\x00\x00'
            #cardTypedata =list(b'\xCC\xEE\x00\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        elif (cardtype=="i"): 
            print("writing input Card")
            cardTypedata[:2]=b'\xC1\x1C'#\x00\x00'
            #cardTypedata =b'\xCC\x11\x00\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        elif (cardtype=="o"): 
            print("writing output Card")
            cardTypedata[:2]=b'\xC0\x0C'#\x00\x00'
            #cardTypedata =b'\xCC\x00\x00\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        elif (cardtype=="m"): 
            print("writing mission Card")
            cardTypedata[:2]=b'\xC2\x2C'#\x00\x00'
        elif (cardtype=="p"): 
            print("writing persona Card")
            cardTypedata[:2]=b'\xC4\x4C'#\x00\x00'
        elif (cardtype=="x"): 
            print("writing control Card ")
            cardTypedata[:2]=b'\xC5\x5C'#\x00\x00'
            #cardTypedata =b'\xCC\x00\x00\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'            
        else:
            print("errorr wrong card type entered.")

        #print(cardTypedata)
        cardNumber=input("what is the card sub-type? (1-999)/Press enter for no change...")
        
        if cardNumber in bytechart:
            cardTypedata[2:3]=bytechart[cardNumber] #"22": b'\x15'
        else:
            print("wrong card number")
        
        # # Write entire 16 byte block.
        writedone=pn532_left.mifare_classic_write_block(4,cardTypedata )
        print('Attempting to write; Success =',writedone)

    input('press any key to write next card...')
    print('--------------------------------\n')




            
        #print('before',cardTypedata)
        #print('2write',bytechart[cardNumber])
        #cardTypedata[2:3]=b'\x15'#this works        #hexNumber=chr((cardNumber))
        #print('hexval',hexNumber)
        #cardTypedata[3]=int(hexNumber[2:])
        #print('wrote',int(hexNumber[2:]))
        #print('after',cardTypedata)
##        if cardNumber.isdigit():
##            intcardNumber=int(cardNumber,16)
##            if intcardNumber <100:
##                print(intcardNumber)
##                cardTypedata[3]=intcardNumber
##            else: # >=100,
##                print(intcardNumber)
##                print(int(intcardNumber/100))
##                print(int(intcardNumber- int(intcardNumber/100)))
##                input()
##                cardTypedata[2]=int(intcardNumber/100)
##                cardTypedata[3]=int(intcardNumber- int(intcardNumber/100)*100)
##                print(cardTypedata)
##                
##                




            
##        cardNumber=input("what is the card number? (01-99)/Press enter for no change...")
##        if cardNumber.isdigit():
##            cardTypedata[3]=int(cardNumber,16)
##        else:
##            print("not changing the card number")
      #  cardNumber=int(input("what is the card number? (01-99)/0 for no change"),16)
      #  if cardNumber!=0:
       #     cardTypedata[3]=cardNumber




        
