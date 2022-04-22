import serial 

def get_data(pk,command): #command = 90-98
    ComPort = serial.Serial('COM3') # open COM4
    ComPort.baudrate = 9600         # set Baud rate to 9600
    ComPort.bytesize = 8            # Number of data bits = 8
    ComPort.parity   = 'N'          # No parity
    ComPort.stopbits = 1            # Number of Stop bits = 1
    address = 4
    extra = '00 00 00 00 00 00 00 00'
    message = "a5%i0%s08%s" % (address, command, extra)
    message = message.ljust(24, "0")
    message_bytes = bytearray.fromhex(message)
    message_bytes += bytes([sum(message_bytes) & 0xFF])

    No = ComPort.write(message_bytes)
    print("here =================== " , message_bytes)
    dataIn = ComPort.read(13)                       # Wait and read data
    dataOut = []
    for i in  range (0,len(dataIn)):
        dataOut.append(dataIn[i:i+1].hex())
    ComPort.close()
    #print(dataOut)    
    if str(command) == '90':
        # print('Cummulative total voltage, Gather total voltage, Current, SOC: ')
        data01 = int((str(dataOut[4])+str(dataOut[5])),16)/10
        data23 = int((str(dataOut[6])+str(dataOut[7])),16)/10
        data45 = (int((str(dataOut[8])+str(dataOut[9])),16)-30000)/10
        data67 = int((str(dataOut[10])+str(dataOut[11])),16)/10
        return [data01,data23,data45,data67]
    elif str(command) == '91':
        # print('max cell vol, num max cell vol, min cell vol, num min cell vol')
        data01 = int((str(dataOut[4])+str(dataOut[5])),16)
        data2 = int(str(dataOut[6]),16)
        data34 = int((str(dataOut[7])+str(dataOut[8])),16)
        data5 = int(str(dataOut[9]),16)
        return [data01,data2,data34,data5]
    elif str(command) == '92':
        #print('max temp val, num max, min temp val, num min')
        data0 = int(str(dataOut[4]),16)
        data1 = int(str(dataOut[5]),16)
        data2 = int(str(dataOut[6]),16)
        data3 = int(str(dataOut[7]),16)
        return [data0,data1,data2,data3]
    elif str(command) == '93':
        #print('state 0=sta 1=char 2=dischar, charge MOS state, discharge Mos state, BMS life, remain capacity')
        data0 = int(str(dataOut[4]),16)
        data1 = int(str(dataOut[5]),16)
        data2 = int(str(dataOut[6]),16)
        data3 = int(str(dataOut[7]),16)
        data4567 = int((str(dataOut[8])+str(dataOut[9])+str(dataOut[10])+str(dataOut[11])),16)
        return [data0,data1,data2,data3,data4567]  
    elif str(command) == '94':
        #print('no of bat string, no of temp, charger status, load status, DI&DO, ')
        data0 = int(str(dataOut[4]),16)
        data1 = int(str(dataOut[5]),16)
        data2 = int(str(dataOut[6]),16)
        data3 = int(str(dataOut[7]),16)
        data4 = str("{0:08b}".format(int(str(dataOut[8]), 16)))
        # data56 = int((str(dataOut[9])+str(dataOut[10])),16)
        return [data0,data1,data2,data3,data4]

if __name__ == 'main':
    pass
