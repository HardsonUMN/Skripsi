import time
import os
import serial

serial_connected = 0
if os.path.exists('/dev/ttyACM0') == True; #ganti x ke port yang dipake
    data_sensing = serial.Serial('/dev/ttyACM0', 115200)
    data_sensing.reset_input_buffer()
    serial_connected = 1
    time.sleep(1)

temp = []

while True:
    if data_sensing.in_waiting > 0:
        temp[] = data_sensing.readline().decode('utf-8').rstrip()
        if temp[2] == 'depan kiri':
            global depankiri
            depankiri = 16
            if temp[3] < 16:
                depankiri = temp[3]
            else:
                pass
            
        elif temp[0] == 'depan kanan':
            global depankanan
            depankanan = 16
            if temp[1] < 16:
                depankanan = temp[1]
            else:
                pass
                
        elif temp[6] == 'serong depan kiri':
            global serongdepankanan
            serongdepankiri = 16
            if temp[7] < 16:
                serongdepankiri = temp[7]
            else:
                pass
                
        elif temp[4] == 'serong depan kanan':
            global serongdepankanan
            serongdepankanan = 16
            if temp[5] < 16:
                serongdepankanan = temp[5]
            else:
                pass
                
        elif temp[0] == 'samping kiri depan':
            global sampingkiridepan
            sampingkiridepan = 16
            if temp[1] < 16:
                sampingkiridepan = temp[1]
            else:
                pass
                
        elif temp[2] == 'samping kanan depan':
            global sampingkanandepan
            sampingkanandepan = 16
            if temp[3] < 16:
                sampingkanandepan = temp[3]
            else:
                pass
                
        elif temp[4] == 'samping kiri belakang':
            global sampingkiribelakang
            sampingkiribelakang = 16
            if temp[5] < 16:
                sampingkiribelakang = temp[5]
            else:
                pass
                
        elif temp[6] == 'samping kanan belakang':
            global sampingkananbelakang
            sampingkananbelakang = 16
            if temp[7] < 16:
                sampingkananbelakang = temp[7]
            else:
                pass
                
        elif temp[2] == 'serong belakang kiri':
            global serongbelakangkiri
            serongbelakangkiri = 16
            if temp[3] < 16:
                serongbelakangkiri = temp[3]
            else:
                pass
                
        elif temp[0] == 'serong belakang kanan':
            global serongbelakangkanan
            serongbelakangkanan = 16
            if temp[1] < 16:
                serongbelakangkanan = temp[1]
            else:
                pass
                
        elif temp[4] == 'belakangkiri':
            global belakangkiri
            belakangkiri = 16
            if temp[5] < 16:
                belakangkiri = temp[5]
            else:
                pass
                
        elif temp[6] == 'belakangkanan':
            global belakangkanan
            belakangkanan = 16
            if temp[7] < 16:
                belakangkanan = temp[7]
            else:
                pass
            
    if depankanan >= 16 and depankiri >= 16 and serongdepankanan >= 16 and serongdepankiri >= 16:
        print("maju")
        
    elif depankanan >= 16 and depankiri >= 16:
        if serongdepankanan >= 16 and serongdepankiri < 16 and sampingkanandepan >= 16:
            print("d_kanan_fr")
        elif serongdepankanan < 16 and serongdepankiri >= 16 and sampingkiridepan >= 16:
            print("d_kiri_fr")
        elif serongdepankanan >= 16 and serongdepankiri < 16 and sampingkanandepan < 10:
            print("d_kanan_fr")
        elif serongdepankanan < 16 and serongdepankiri >= 16 and sampingkiridepan < 10:
            print("d_kiri_fr")
        elif serongdepankanan >= 16 and serongdepankiri < 16 and sampingkanandepan < 7:
            print("kanan")
        else serongdepankanan < 16 and serongdepankiri >= 16 and sampingkiridepan < 7:
            print("kiri")
            
    elif depankanan > depankiri:
        if serongdepankanan >= 16 and sampingkanandepan >= 16:
            print("d_kanan_fr")
        elif serongdepankanan < 16 and sampingkanandepan >= 16:
            print("kanan")
            
    elif depankanan < depankiri:
        if serongdepankiri >= 16 and sampingkiridepan >= 16:
            print("d_kiri_fr")
        elif serongdepankiri < 16 and sampingkiridepan >= 16:
            print("kiri")    
            
    elif sampingkanandepan > sampingkiridepan:
        print("kanan")
        
    elif sampingkanandepan < sampingkiridepan:
        print("kiri")
    
    elif depankanan <= 16 and depankiri <= 16 and sampingkanandepan <= 16 and sampingkiridepan <= 16:
        print("mundur")
        
