import serial 

ComPort = serial.Serial('COM3') # open COM4
ComPort.baudrate = 9600         # set Baud rate to 9600
ComPort.bytesize = 8            # Number of data bits = 8
ComPort.parity   = 'N'          # No parity
ComPort.stopbits = 1            # Number of Stop bits = 1

def get_data(command): #command = 90-98
    address = 4
    extra = '00 00 00 00 00 00 00 00'
    message = "a5%i0%s08%s" % (address, command, extra)
    message = message.ljust(24, "0")
    message_bytes = bytearray.fromhex(message)
    message_bytes += bytes([sum(message_bytes) & 0xFF])

    No = ComPort.write(message_bytes)
    dataIn = ComPort.read(13)                       # Wait and read data
    dataOut = []
    for i in  range (0,len(dataIn)):
        dataOut.append(dataIn[i:i+1].hex())

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


def get_cell_voltage():
    command ='95'
    address = 4
    extra = '00 00 00 00 00 00 00 00'
    message = "a5%i0%s08%s" % (address, command, extra)
    message = message.ljust(24, "0")
    message_bytes = bytearray.fromhex(message)
    message_bytes += bytes([sum(message_bytes) & 0xFF])

    No = ComPort.write(message_bytes)
    CELL = []
    for j in range(1,9):
        dataIn = ComPort.read(13)                       # Wait and read data
        dataOut = []
        for i in  range (0,len(dataIn)):
            dataOut.append(dataIn[i:i+1].hex())
        #print(dataOut)
        
        CELL.append(int((str(dataOut[5])+str(dataOut[6])),16))
        CELL.append(int((str(dataOut[7])+str(dataOut[8])),16))
        CELL.append(int((str(dataOut[9])+str(dataOut[10])),16))

    return CELL

def get_cell_temp():
    command ='96'
    address = 4
    extra = '00 00 00 00 00 00 00 00'
    message = "a5%i0%s08%s" % (address, command, extra)
    message = message.ljust(24, "0")
    message_bytes = bytearray.fromhex(message)
    message_bytes += bytes([sum(message_bytes) & 0xFF])

    No = ComPort.write(message_bytes)
    CELL = []
    for j in range(1,2):
        dataIn = ComPort.read(13)                       # Wait and read data
        dataOut = []
        for i in  range (0,len(dataIn)):
            dataOut.append(dataIn[i:i+1].hex())
        #print(dataOut)
        
        CELL.append(int(str(dataOut[5]),16))
        CELL.append(int(str(dataOut[6]),16))
        CELL.append(int(str(dataOut[7]),16))
        CELL.append(int(str(dataOut[8]),16))
        CELL.append(int(str(dataOut[9]),16))
        CELL.append(int(str(dataOut[10]),16))
        CELL.append(int(str(dataOut[11]),16))
        
    return CELL

def cell_blance_state():
    pass

def cell_failure_state():
    address = 4
    command = '98'
    extra = '00 00 00 00 00 00 00 00'
    message = "a5%i0%s08%s" % (address, command, extra)
    message = message.ljust(24, "0")
    message_bytes = bytearray.fromhex(message)
    message_bytes += bytes([sum(message_bytes) & 0xFF])

    No = ComPort.write(message_bytes)
    dataIn = ComPort.read(13)                       # Wait and read data
    dataOut = []
    for i in  range (0,len(dataIn)):
        dataOut.append(dataIn[i:i+1].hex())

    print(dataOut)
    lst=[]
    for i in range(4,12):
        data = str("{0:08b}".format(int(str(dataOut[i]), 16)))
        lst.append(data)
    #byte0
    print('Cell volt high lv1 = ', lst[0][0])
    print('Cell volt high lv2 = ', lst[0][1])
    print('Cell volt low lv1 = ', lst[0][2])
    print('Cell volt low lv2 = ', lst[0][3])
    print('Sum volt high lv1 = ',lst[0][4])
    print('Sum volt high lv2 = ',lst[0][5])
    print('Sum volt low lv1 = ',lst[0][6])
    print('Sum volt low lv2 = ',lst[0][7])
    #byte1
    print('Chg temp high lv1 = ', lst[1][0])
    print('Chg temp high lv2 = ', lst[1][1])
    print('Chg temp low lv1 = ', lst[1][2])
    print('Chg temp low lv2 = ', lst[1][3])
    print('DisChg temp high lv1 = ', lst[1][4])
    print('DisChg temp high lv2 = ', lst[1][5])
    print('DisChg temp low lv1 = ', lst[1][6])
    print('DisChg temp low lv2 = ', lst[1][7])
    #byte2
    print('Chg over-current lv1: ', lst[2][0])
    print('Chg over-current lv2: ', lst[2][1])
    print('DisChg over-current lv1: ', lst[2][2])
    print('DisChg over-current lv2: ', lst[2][3])
    print('SOC high lv1:', lst[2][4])
    print('SOC high lv2: ', lst[2][5])
    print('SOC low lv1: ', lst[2][6])
    print('SOC low lv2: ', lst[2][7])
    #byte3
    print('Diff vol lv1: ', lst[3][0])
    print('Diff vol lv2: ', lst[3][1])
    print('Diff temp lv1: ', lst[3][2])
    print('Diff temp lv2: ', lst[3][3])
    #byte4
    print('Chg MOS temp high alarm: ', lst[4][0])
    print('DisChg MOS temp high alarm: ', lst[4][1])
    print('Chg MOS temp sensor error: ', lst[4][2])
    print('DisChg MOS temp sensor error: ', lst[4][3])
    print('Chg MOS adhesion err: ', lst[4][4])
    print('DisChg MOS adhesion err: ', lst[4][5])
    print('Chg MOS open circuit err: ', lst[4][6])
    print('DisChg MOS open circuit err: ', lst[4][7])
    #byte5
    print('AFE collect chip err: ', lst[5][0])
    print('Voltage collect drop: ', lst[5][1])
    print('cell temp sensor error: ', lst[5][2])
    print('EEPROM error: ', lst[5][3])
    print('RTC error: ', lst[4][4])
    print('precharge failure: ', lst[4][5])
    print('Communication failure: ', lst[4][6])
    print('Internal communication failure: ', lst[4][7])
    #byte6
    print('Current module fault: ', lst[6][0])
    print('Sum voltage detect fault: ', lst[6][1])
    print('short circuit protect fault: ', lst[6][2])
    print('Low volt fordidden chg fault: ', lst[6][3])
    #byte7
    print('Fault code: ',dataOut[11])

    return lst

def query_setting(command):  #command = 50---
    address = 4
    extra = '00 00 00 00 00 00 00 00'
    message = "a5%i0%s08%s" % (address, command, extra)
    message = message.ljust(24, "0")
    message_bytes = bytearray.fromhex(message)
    message_bytes += bytes([sum(message_bytes) & 0xFF])

    No = ComPort.write(message_bytes)
    dataIn = ComPort.read(13)                       # Wait and read data
    dataOut = []
    for i in  range (0,len(dataIn)):
        dataOut.append(dataIn[i:i+1].hex())

    print(dataOut)
    if str(command) == '50':
        print('Query the rated pack capacity and nominal cell voltage: ')
        data0123 = int( str(dataOut[4]) + str(dataOut[5]) + str(dataOut[6]) + str(dataOut[7]) ,16)
        data4567 = int( str(dataOut[8]) + str(dataOut[9]) + str(dataOut[10]) + str(dataOut[11]) ,16)
        return [data0123,data4567]

    if str(command) == '5f':
        print('Query the voltage thresholds that control balancing: ')
        data01 = int( str(dataOut[4]) + str(dataOut[5])   ,16)
        data23 = int( str(dataOut[6]) + str(dataOut[7])   ,16)

        return [data01,data23]    

    if str(command) == '52':
        print('Query ???: ')
        data23 = int( str(dataOut[6]) + str(dataOut[7])   ,16)
        data67 = int( str(dataOut[10]) + str(dataOut[11]) ,16)
        return [data23,data67]

    if str(command) == '60':
        print('Query the short-circuit shutdown threshold and the current sampling resolution: ')
        print('[short-circuit shutdown threshold A ; Current sampling resistance, in milliohms]')
        data01 = int((str(dataOut[4])+str(dataOut[5])),16)
        data23 = int((str(dataOut[6])+str(dataOut[7])),16)

        return [data01,data23]

    if str(command) == '51':
        print('Query the "Number of acquisition board", "board Cell No 1~3 counts" and "NTC Temp Sensor 1~3 counts": ')
        data0 = int(str(dataOut[4]),16)
        data1 = int(str(dataOut[5]),16)
        data2 = int(str(dataOut[6]),16)
        data3 = int(str(dataOut[7]),16)
        data4 = int(str(dataOut[8]),16)
        data5 = int(str(dataOut[9]),16)
        data6 = int(str(dataOut[10]),16)
        return [data0,data1,data2,data3,data4,data5,data6]

    if str(command) == '53':
        print('Query "Battery operation mode" / "Production Date" / Battery Type" and "Automatic sleep time" ???: ')
        data0 = int(str(dataOut[4]),16)
        data1 = int(str(dataOut[5]),16)
        data2 = int(str(dataOut[6]),16)
        data3 = int(str(dataOut[7]),16)
        data4 = int(str(dataOut[8]),16)
        data56 = int((str(dataOut[9])+str(dataOut[10])),16)
        
        return [data0,data1,data2,data3,data4,data56]

    # if str(command) == '54':
    #     print('??? Query the "Firmware index number": ')
    #     data0 = int(str(dataOut[4]),16)
    #     data1 = int(str(dataOut[5]),16)
    #     data2 = int(str(dataOut[6]),16)
    #     data3 = int(str(dataOut[7]),16)
    #     data4 = int(str(dataOut[8]),16)
    #     data5 = int(str(dataOut[9]),16)
    #     data6 = int(str(dataOut[10]),16)
    #     return [data0,data1,data2,data3,data4,data5,data6]

    if str(command) == '57':
        print('query battery code???')
        return dataOut

    if str(command) == '59':
        print('Query the Level 1 and 2 alarm thresholds for high and low cell voltages')
        print('[cell volt high lv1, cel vol hig lv2, cel vol low 1, cel vol low 2]')
        data01 = int((str(dataOut[4])+str(dataOut[5])),16)/1000
        data23 = int((str(dataOut[6])+str(dataOut[7])),16)/1000
        data45 = int((str(dataOut[8])+str(dataOut[9])),16)/1000
        data67 = int((str(dataOut[10])+str(dataOut[11])),16)/1000
        return [data01,data23,data45,data67]

    if str(command) == '5a':
        print('Query the Level 1 and 2 alarm thresholds for high and low voltages for the pack as a whole')
        print('[sum volt high lv1, sum vol hig lv2, sum vol low 1, sum vol low 2]')
        data01 = int((str(dataOut[4])+str(dataOut[5])),16)/10
        data23 = int((str(dataOut[6])+str(dataOut[7])),16)/10
        data45 = int((str(dataOut[8])+str(dataOut[9])),16)/10
        data67 = int((str(dataOut[10])+str(dataOut[11])),16)/10
        return [data01,data23,data45,data67]

    if str(command) == '5b':
        print('Query the Level 1 and 2 alarm thresholds for charge and discharge current for the pack.')
        print('[cha cur large lv1, cha cur large lv2, discha cur large 1, discha cur large 2]')
        data01 = (30000-int((str(dataOut[4])+str(dataOut[5])),16))/10
        data23 = (30000-int((str(dataOut[6])+str(dataOut[7])),16))/10
        data45 = (int((str(dataOut[8])+str(dataOut[9])),16)-30000)/10
        data67 = (int((str(dataOut[10])+str(dataOut[11])),16)-30000)/10
        return [data01,data23,data45,data67]

    if str(command) == '5e':
        print('Query the Level 1 and 2 alarm thresholds for allowable difference in cell voltage and temperature sensor readings')
        print('[vol diff large lv1, vol dif lar lv2, temp dif lar 1, temp dif lar 2]')
        data01 = int((str(dataOut[4])+str(dataOut[5])),16)/1000
        data23 = int((str(dataOut[6])+str(dataOut[7])),16)/1000
        data4 = int(str(dataOut[8]),16)
        data5 = int(str(dataOut[9]),16)
        return [data01,data23,data4,data5]

    if str(command) == '5d':
        print('Query the Level 1 and 2 alarm thresholds of SOC ')
        print('[SOC high lv1, SOC high lv2, SOC low 1, SOC low 2]')
        data01 = int((str(dataOut[4])+str(dataOut[5])),16)/10
        data23 = int((str(dataOut[6])+str(dataOut[7])),16)/10
        data45 = int((str(dataOut[8])+str(dataOut[9])),16)/10
        data67 = int((str(dataOut[10])+str(dataOut[11])),16)/10
        return [data01,data23,data45,data67]

    if str(command) == '5c':
        print('Query the Level 1 and 2 alarm thresholds for charge/discha temp high/low')
        print('[char temp high lv1, cha tem high lv2, temp dif lar 1, temp dif lar 2]')
        data0 = int(str(dataOut[4]),16)-40
        data1 = int(str(dataOut[5]),16)-40
        data2 = int(str(dataOut[6]),16)-40
        data3 = int(str(dataOut[7]),16)-40
        data4 = int(str(dataOut[8]),16)-40
        data5 = int(str(dataOut[9]),16)-40
        data6 = int(str(dataOut[10]),16)-40
        data7 = int(str(dataOut[11]),16)-40
        return [data0,data1,data2,data3,data4,data5,data6,data7]

'''open charge MOS. A5 40 DA 08 00 00 00 00 00 00 00 00 C7
close charge MOS. A5 40 DA 08 01 00 00 00 00 00 00 00 C8
open discharge MOS. A5 40 D9 08 00 00 00 00 00 00 00 00 C6
close discharge MOS. A5 40 D9 08 01 00 00 00 00 00 00 00 C7'''

def MOS_control_open(command):
    #command =''
    address = 4
    extra = '00 00 00 00 00 00 00 00'
    message = "a5%i0%s08%s" % (address, command, extra)
    message = message.ljust(24, "0")
    message_bytes = bytearray.fromhex(message)
    message_bytes += bytes([sum(message_bytes) & 0xFF])

    No = ComPort.write(message_bytes)
    CELL = []
    for j in range(1,2):
        dataIn = ComPort.read(13)                       # Wait and read data
        dataOut = []
        for i in  range (0,len(dataIn)):
            dataOut.append(dataIn[i:i+1].hex())
        #print(dataOut)
    if str(command) == 'DA':
        print('Open charge MOS')
    if str(command) == 'D9':
        print('Open discharge MOS')
    
def MOS_control_close(command):
    #command =''
    address = 4
    extra = '01 00 00 00 00 00 00 00'
    message = "a5%i0%s08%s" % (address, command, extra)
    message = message.ljust(24, "0")
    message_bytes = bytearray.fromhex(message)
    message_bytes += bytes([sum(message_bytes) & 0xFF])

    No = ComPort.write(message_bytes)
    CELL = []
    for j in range(1,2):
        dataIn = ComPort.read(13)                       # Wait and read data
        dataOut = []
        for i in  range (0,len(dataIn)):
            dataOut.append(dataIn[i:i+1].hex())
        #print(dataOut)
    if str(command) == 'DA':
        print('Close charge MOS')
    if str(command) == 'D9':
        print('Close discharge MOS')


def set_parameter():
    pass

def set_capacity_and_nominal_cell_voltage(capacity,voltage):
    capacity = str(hex(capacity)).replace("0x","",1)
    while (len(capacity) < 8):
        capacity = '0' + capacity

    voltage = str(hex(voltage)).replace("0x","",1)
    while (len(voltage) < 8):
        voltage = '0' + voltage

    address = 4
    command = '10'
    extra = capacity + voltage
    message = "a5%i0%s08%s" % (address, command, extra)
    message = message.ljust(24, "0")
    message_bytes = bytearray.fromhex(message)
    message_bytes += bytes([sum(message_bytes) & 0xFF])

    No = ComPort.write(message_bytes)
    dataIn = ComPort.read(13)                       # Wait and read data
    dataOut = []
    for i in  range (0,len(dataIn)):
        dataOut.append(dataIn[i:i+1].hex())

    print(dataOut)

def Set_the_Level_1_and_2_alarm_thresholds_for_high_and_low_cell_voltages(cell_volt_high_lv1, cel_vol_hig_lv2, cel_vol_low_1, cel_vol_low_2):
    cell_volt_high_lv1 = str(hex(cell_volt_high_lv1)).replace("0x","",1)
    while (len(cell_volt_high_lv1) < 4):
        cell_volt_high_lv1 = '0' + cell_volt_high_lv1

    cel_vol_hig_lv2 = str(hex(cel_vol_hig_lv2)).replace("0x","",1)
    while (len(cel_vol_hig_lv2) < 4):
        cel_vol_hig_lv2 = '0' + cel_vol_hig_lv2

    cel_vol_low_1 = str(hex(cel_vol_low_1)).replace("0x","",1)
    while (len(cel_vol_low_1) < 4):
        cel_vol_low_1 = '0' + cel_vol_low_1

    cel_vol_low_2 = str(hex(cel_vol_low_2)).replace("0x","",1)
    while (len(cel_vol_low_2) < 4):
        cel_vol_low_2 = '0' + cel_vol_low_2

    address = 4
    command = '19'
    extra = cell_volt_high_lv1 + cel_vol_hig_lv2 + cel_vol_low_1 + cel_vol_low_2
    message = "a5%i0%s08%s" % (address, command, extra)
    message = message.ljust(24, "0")
    message_bytes = bytearray.fromhex(message)
    message_bytes += bytes([sum(message_bytes) & 0xFF])

    No = ComPort.write(message_bytes)
    dataIn = ComPort.read(13)                       # Wait and read data
    dataOut = []
    for i in  range (0,len(dataIn)):
        dataOut.append(dataIn[i:i+1].hex())

    print(dataOut)
    print('Set successful!')   

def Set_the_Level_1_and_2_alarm_thresholds_for_high_and_low_voltages_for_the_pack_as_a_whole(sum_volt_high_lv1, sum_vol_hig_lv2, sum_vol_low_1, sum_vol_low_2):
    sum_volt_high_lv1 = str(hex(sum_volt_high_lv1)).replace("0x","",1)
    while (len(sum_volt_high_lv1) < 4):
        sum_volt_high_lv1 = '0' + sum_volt_high_lv1

    sum_vol_hig_lv2 = str(hex(sum_vol_hig_lv2)).replace("0x","",1)
    while (len(sum_vol_hig_lv2) < 4):
        sum_vol_hig_lv2 = '0' + sum_vol_hig_lv2

    sum_vol_low_1 = str(hex(sum_vol_low_1)).replace("0x","",1)
    while (len(sum_vol_low_1) < 4):
        sum_vol_low_1 = '0' + sum_vol_low_1

    sum_vol_low_2 = str(hex(sum_vol_low_2)).replace("0x","",1)
    while (len(sum_vol_low_2) < 4):
        sum_vol_low_2 = '0' + sum_vol_low_2

    address = 4
    command = '1a'
    extra = sum_volt_high_lv1 + sum_vol_hig_lv2 + sum_vol_low_1 + sum_vol_low_2
    message = "a5%i0%s08%s" % (address, command, extra)
    message = message.ljust(24, "0")
    message_bytes = bytearray.fromhex(message)
    message_bytes += bytes([sum(message_bytes) & 0xFF])

    No = ComPort.write(message_bytes)
    dataIn = ComPort.read(13)                       # Wait and read data
    dataOut = []
    for i in  range (0,len(dataIn)):
        dataOut.append(dataIn[i:i+1].hex())

    print(dataOut)
    print('Set successful!')    

def Set_the_Level_1_and_2_alarm_thresholds_for_charge_and_discharge_current_for_the_pack(cha_cur_large_lv1, cha_cur_large_lv2, discha_cur_large_1, discha_cur_large_2):
    cha_cur_large_lv1 = 30000 - int(cha_cur_large_lv1)*10
    cha_cur_large_lv1 = str(hex(cha_cur_large_lv1)).replace("0x","",1)
    while (len(cha_cur_large_lv1) < 4):
        cha_cur_large_lv1 = '0' + cha_cur_large_lv1

    cha_cur_large_lv2 = 30000 - int(cha_cur_large_lv2)*10
    cha_cur_large_lv2 = str(hex(cha_cur_large_lv2)).replace("0x","",1)
    while (len(cha_cur_large_lv2) < 4):
        cha_cur_large_lv2 = '0' + cha_cur_large_lv2

    discha_cur_large_1 = discha_cur_large_1*10 + 30000
    discha_cur_large_1 = str(hex(discha_cur_large_1)).replace("0x","",1)
    while (len(discha_cur_large_1) < 4):
        discha_cur_large_1 = '0' + discha_cur_large_1

    discha_cur_large_2 = discha_cur_large_2*10 + 30000
    discha_cur_large_2 = str(hex(discha_cur_large_2)).replace("0x","",1)
    while (len(discha_cur_large_2) < 4):
        discha_cur_large_2 = '0' + discha_cur_large_2

    address = 4
    command = '1b'
    extra = cha_cur_large_lv1 + cha_cur_large_lv2 + discha_cur_large_1 + discha_cur_large_2
    message = "a5%i0%s08%s" % (address, command, extra)
    message = message.ljust(24, "0")
    message_bytes = bytearray.fromhex(message)
    message_bytes += bytes([sum(message_bytes) & 0xFF])

    No = ComPort.write(message_bytes)
    dataIn = ComPort.read(13)                       # Wait and read data
    dataOut = []
    for i in  range (0,len(dataIn)):
        dataOut.append(dataIn[i:i+1].hex())

    print(dataOut)
    print('Set successful!') 


def Set_the_Level_1_and_2_alarm_thresholds_for_allowable_difference_in_cell_voltage_and_temperature_sensor_readings(vol_diff_large_lv1, vol_dif_lar_lv2, temp_dif_lar_1, temp_dif_lar_2):
    vol_diff_large_lv1 = str(hex(vol_diff_large_lv1)).replace("0x","",1)
    while (len(vol_diff_large_lv1) < 4):
        vol_diff_large_lv1 = '0' + vol_diff_large_lv1

    vol_dif_lar_lv2 = str(hex(vol_dif_lar_lv2)).replace("0x","",1)
    while (len(vol_dif_lar_lv2) < 4):
        vol_dif_lar_lv2 = '0' + vol_dif_lar_lv2

    temp_dif_lar_1 = str(hex(temp_dif_lar_1)).replace("0x","",1)
    while (len(temp_dif_lar_1) < 2):
        temp_dif_lar_1 = '0' + temp_dif_lar_1

    temp_dif_lar_2 = str(hex(temp_dif_lar_2)).replace("0x","",1)
    while (len(temp_dif_lar_2) < 2):
        temp_dif_lar_2 = '0' + temp_dif_lar_2

    address = 4
    command = '1e'
    extra = vol_diff_large_lv1 + vol_dif_lar_lv2 + temp_dif_lar_1 + temp_dif_lar_2 + '0000'
    message = "a5%i0%s08%s" % (address, command, extra)
    message = message.ljust(24, "0")
    message_bytes = bytearray.fromhex(message)
    message_bytes += bytes([sum(message_bytes) & 0xFF])

    No = ComPort.write(message_bytes)
    dataIn = ComPort.read(13)                       # Wait and read data
    dataOut = []
    for i in  range (0,len(dataIn)):
        dataOut.append(dataIn[i:i+1].hex())

    print(dataOut)
    print('Set successful!')


#Set_the_Level_1_and_2_alarm_thresholds_for_high_and_low_cell_voltages(cell_volt_high_lv1=3650, cel_vol_hig_lv2=3750, cel_vol_low_1=2300, cel_vol_low_2=2600)
#Set_the_Level_1_and_2_alarm_thresholds_for_high_and_low_voltages_for_the_pack_as_a_whole(sum_volt_high_lv1 = 876, sum_vol_hig_lv2 = 900, sum_vol_low_1 = 552, sum_vol_low_2 = 528)
#Set_the_Level_1_and_2_alarm_thresholds_for_charge_and_discharge_current_for_the_pack(cha_cur_large_lv1=180, cha_cur_large_lv2=225, discha_cur_large_1=180, discha_cur_large_2=225)
#Set_the_Level_1_and_2_alarm_thresholds_for_allowable_difference_in_cell_voltage_and_temperature_sensor_readings(vol_diff_large_lv1=500, vol_dif_lar_lv2=800, temp_dif_lar_1=10, temp_dif_lar_2=15)
#print(query_setting('5e'))
#MOS_control_close('DA')
for i in range(90,94):
    print(get_data(str(i)))

ComPort.close()
