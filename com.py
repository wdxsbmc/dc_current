import os
#pip3 install pyserial
import serial
from serial import *

class com():

    message='' 

    def __init__(self):
        '''
           init serial, send recive data
        '''
        self.message=''

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
        while True:  
            data=self.ser.readline()  
            self.message+=data  

    '''
        68H	Addr	SubAddr	07H	07H	CUR_MOD	Freq	TotalS	CS	16H
    test:  68  1    1          07 07  0       1      1       n   16h
    '''
    def make_packet(self,board_num,board_port,ctl_code,data_len,data):
        #pkt = bytearray([0xf0,0x14,0x09,0xe0,0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x28,0x00,0x00,0x00,0x00,0x00,0x00,0x00])

        checksum = 0
        pkt = [] 
        #bytearray()
        #make cmd pkt
        #head
        pkt.append(0x68)
        pkt.append(board_num)
        pkt.append(board_port)
        pkt.append(ctl_code)
        pkt.append(data_len)

        #data
        pkt.extend(data)       

        #udpate checksum
        if(len(pkt) > 0):
            for i in range(0,len(pkt)):
                checksum = checksum + pkt[i]

        pkt.append(checksum%256)
        pkt.append(0x16)
        return pkt



    def cmd_send_recv(self,board_num,board_port,ctl_code,data_len,data,exp_code):
     
     
        if(self.ser.is_open):

            #data = bytearray([0x00,0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x28,0x00,0x00,0x00,0x00,0x00,0x00,0x00])

            cmd = self.make_packet(self,board_num,board_port,ctl_code,data_len,data)
            
            print(cmd)

            self.ser.send_data(cmd)
            self.ser.read_data()

            recv_data = self.message[0:7]       

            barr = bytearray(recv_data)

            if(barr[4] == exp_code):
                return 1
            else:
                return 0

