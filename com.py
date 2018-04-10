import os
# pip3 install pyserial
import serial
from serial import *

class com():

    message='' 

    def __init__(self):
        '''
           init serial, send recive data
        '''
        self.message = []

    def init_com(self,com_port):
        # 创建一个com_com
        self.com_port = com_port
        self.ser = serial.Serial(port=self.com_port, baudrate=115200, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS) 
        if not self.ser.isOpen():  
            self.ser.open()  

    def port_is_open(self):
        return  self.ser.isOpen()

    def port_open(self):  
        if not self.ser.isOpen():  
            self.ser.open()  

    def port_close(self):  
        self.ser.close()


    def send_data(self,data):  
        number=self.ser.write(data)  
        return number 

    def read_data(self):  
        #while True:  
        data=self.ser.read_all()
        self.message.extend(data)

    '''
        68H	Addr	SubAddr	07H	07H	CUR_MOD	Freq	TotalS	CS	16H
    test:  FE FE FE FE 68 01 FF 07 07 00 E8 03 05 00 00 00 66 16
    '''
    def make_packet(self,board_num,board_port,ctl_code,data_len,data):
    
        checksum = 0
        pkt = [] 

        # head
        pkt.append(0xFE)
        pkt.append(0xFE)
        pkt.append(0xFE)
        pkt.append(0xFE)
        pkt.append(0x68)
        pkt.append(int(board_num))
        pkt.append(int(board_port))
        pkt.append(ctl_code)
        pkt.append(data_len)

        # data
        pkt.extend(data)       

        # udpate checksum
        if(len(pkt) > 0):
            for i in range(0,len(pkt)):
                checksum = checksum + int(pkt[i])

        pkt.append(checksum%256)
        pkt.append(0x16)
        return pkt



    def cmd_send_recv(self,board_num,board_port,ctl_code,data_len,data,exp_code):
     
     
        if(self.ser.is_open):

            cmd = self.make_packet(board_num, board_port, ctl_code, data_len, data)
            
            # cmd = [0x01, 0x05, 0x91, 0xF5, 0x00, 0x00, 0xF1, 0x04]
            print(cmd)

            self.send_data(cmd)
            self.read_data()

            recv_data = self.message[0:7]       

            barr = bytearray(recv_data)

            if(barr[4] == exp_code):
                return 1
            else:
                return 0

